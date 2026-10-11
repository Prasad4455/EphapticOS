"""E2E of the stable-manifest-id lifecycle: change one row, never vanish.

The manifest data_id is stable (dlt_source:{dataset}:{source}), so a re-sync
with changed content updates the Data row in place — the source must never be
absent from the relational store between add and Ephaptify. Re-Ephaptify then
purges the source's prior derived artifacts and re-emits current rows: the
updated value becomes searchable and the old value disappears. An unchanged
re-add keeps the fast skip (no reprocessing).

Real add + Ephaptify against local stores; the DLT route is LLM-free, and
embeddings are mocked so the vector store works offline.
"""

import logging
import pathlib
from unittest.mock import patch

import pytest
import pytest_asyncio

import EphapticOS
from EphapticOS.context_global_variables import graph_db_config, vector_db_config
from EphapticOS.infrastructure.databases.vector.embeddings.LiteLLMEmbeddingEngine import (
    LiteLLMEmbeddingEngine,
)
from EphapticOS.modules.data.methods import get_authorized_existing_datasets
from EphapticOS.modules.data.methods.get_dataset_data import get_dataset_data
from EphapticOS.modules.engine.operations.setup import setup as engine_setup
from EphapticOS.modules.users.methods import get_default_user

logger = logging.getLogger(__name__)

DATASET = "gadgets_ds"
# Separate identity for the second test: dlt keeps process-global pipeline
# state keyed by name, so tests in one process must not share dataset names.
DATASET_SKIP = "gizmos_ds"


async def _mock_embed_text(self, texts):
    return [[float(len(t) % 7) / 10.0] * self.dimensions for t in texts]


@pytest_asyncio.fixture
async def clean_env(tmp_path, monkeypatch):
    pytest.importorskip("dlt")
    pytest.importorskip("ladybug")

    monkeypatch.setenv("EphapticOS_SKIP_CONNECTION_TEST", "true")
    monkeypatch.setenv("ENABLE_BACKEND_ACCESS_CONTROL", "false")
    root = pathlib.Path(tmp_path)
    monkeypatch.setenv("DLT_DATA_DIR", str(root / "dlt"))

    from EphapticOS.infrastructure.databases.graph.get_graph_engine import _create_graph_engine
    from EphapticOS.infrastructure.databases.relational.create_relational_engine import (
        create_relational_engine,
    )
    from EphapticOS.infrastructure.databases.vector.create_vector_engine import _create_vector_engine

    _create_graph_engine.cache_clear()
    _create_vector_engine.cache_clear()
    create_relational_engine.cache_clear()
    graph_db_config.set(None)
    vector_db_config.set(None)

    EphapticOS.config.set_relational_db_config({"db_provider": "sqlite"})
    EphapticOS.config.system_root_directory(str(root / "system"))
    EphapticOS.config.data_root_directory(str(root / "data"))
    EphapticOS.config.set_vector_db_url(str(root / "system" / "databases" / "EphapticOS.lancedb"))

    await EphapticOS.prune.prune_data()
    await EphapticOS.prune.prune_system(metadata=True)
    await engine_setup()

    with patch.object(LiteLLMEmbeddingEngine, "embed_text", new=_mock_embed_text):
        yield

    try:
        await EphapticOS.prune.prune_data()
        await EphapticOS.prune.prune_system(metadata=True)
    except Exception:
        logger.debug("Ignoring exception in clean_env", exc_info=True)


def _dlt_source(rows, name="gadgets"):
    import dlt

    @dlt.resource(name=name, primary_key="id", write_disposition="replace")
    def gadgets():
        yield from rows

    return gadgets


async def _manifest_record(user, dataset_name=DATASET):
    dataset = (
        await get_authorized_existing_datasets(
            user=user, permission_type="read", datasets=[dataset_name]
        )
    )[0]
    records = [
        d
        for d in await get_dataset_data(dataset.id)
        if isinstance(d.system_metadata, dict) and d.system_metadata.get("source") == "dlt_source"
    ]
    return dataset, records


async def _row_texts():
    from EphapticOS.infrastructure.databases.graph import get_graph_engine

    graph = await get_graph_engine()
    nodes, _ = await graph.get_graph_data()
    return " ".join(
        str(props.get("text", ""))
        for _, props in nodes
        if props.get("type") in ("DltRow", "DocumentChunk")
    )


@pytest.mark.asyncio
async def test_changed_row_reprocesses_without_vanishing(clean_env):
    user = await get_default_user()
    kwargs = {"primary_key": "id", "write_disposition": "replace", "max_rows_per_table": 0}

    await EphapticOS.add(
        _dlt_source(
            [
                {"id": "1", "status": "active"},
                {"id": "2", "status": "pending"},
            ]
        ),
        dataset_name=DATASET,
        **kwargs,
    )
    _dataset, records = await _manifest_record(user)
    assert len(records) == 1
    manifest_id = records[0].id
    first_hash = records[0].content_hash

    await EphapticOS.Ephaptify(datasets=[DATASET])
    texts = await _row_texts()
    assert "pending" in texts

    # Re-sync with one changed row through plain add(): add() is IDEMPOTENT.
    # The completed record keeps the fast skip — same id, same stored hash,
    # graph untouched. Updating an existing source is update()'s job
    # (explicit UUID) or an explicit re-ingest (below).
    changed_rows = [
        {"id": "1", "status": "active"},
        {"id": "2", "status": "shipped"},
    ]
    await EphapticOS.add(_dlt_source(changed_rows), dataset_name=DATASET, **kwargs)
    _, records = await _manifest_record(user)
    assert len(records) == 1, "manifest must never be absent after a re-add"
    assert records[0].id == manifest_id, "stable identity: same Data id across re-adds"
    assert str(records[0].content_hash) == str(first_hash), (
        "plain re-add must not mutate the completed record"
    )
    texts = await _row_texts()
    assert "pending" in texts, "plain re-add must leave the graph untouched"

    # Explicit re-ingest: the completed-skip runs whenever data_cache OR
    # incremental_loading is on, so bypassing it takes both flags off; the
    # record then updates in place and re-Ephaptify purges + re-emits.
    await EphapticOS.add(
        _dlt_source(changed_rows),
        dataset_name=DATASET,
        incremental_loading=False,
        data_cache=False,
        **kwargs,
    )
    _, records = await _manifest_record(user)
    assert len(records) == 1
    assert records[0].id == manifest_id, "stable identity survives the explicit re-ingest"
    assert str(records[0].content_hash) != str(first_hash), "record tracked the change"

    await EphapticOS.Ephaptify(datasets=[DATASET])
    texts = await _row_texts()
    assert "shipped" in texts, "updated row value must be in the graph"
    assert "pending" not in texts, "stale row value must be purged, not linger"


@pytest.mark.asyncio
async def test_unchanged_readd_keeps_the_fast_skip(clean_env):
    user = await get_default_user()
    kwargs = {"primary_key": "id", "write_disposition": "replace", "max_rows_per_table": 0}
    rows = [{"id": "1", "status": "active"}]

    await EphapticOS.add(_dlt_source(rows, name="gizmos"), dataset_name=DATASET_SKIP, **kwargs)
    _, records = await _manifest_record(user, DATASET_SKIP)
    first_hash = records[0].content_hash
    await EphapticOS.Ephaptify(datasets=[DATASET_SKIP])

    # Identical re-add: same id, same hash — and Ephaptify reports the item
    # as already completed rather than reprocessing it.
    await EphapticOS.add(_dlt_source(rows, name="gizmos"), dataset_name=DATASET_SKIP, **kwargs)
    _, records = await _manifest_record(user, DATASET_SKIP)
    assert str(records[0].content_hash) == str(first_hash)

    status = records[0].pipeline_status.get("Ephaptify_pipeline", {})
    assert status, "unchanged re-add must NOT clear Ephaptify status (no reprocess)"
