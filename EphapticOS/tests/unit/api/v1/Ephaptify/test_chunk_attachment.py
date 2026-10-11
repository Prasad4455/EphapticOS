"""chunk_attachment validation and plumbing at the Ephaptify() boundary (SDK-163).

Ephaptify() forwards unknown keyword arguments all the way into the LLM call, which
also takes **kwargs, so anything unusable has to raise here rather than vanish.
"""

import importlib
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pydantic import BaseModel

from EphapticOS.infrastructure.engine import DataPoint
from EphapticOS.shared.data_models import KnowledgeGraph

Ephaptify_module = importlib.import_module("EphapticOS.api.v1.Ephaptify.Ephaptify")
serve_state_module = importlib.import_module("EphapticOS.api.v1.serve.state")


class _Person(DataPoint):
    name: str
    metadata: dict = {"index_fields": ["name"]}


class _Directory(DataPoint):
    people: list[_Person]
    metadata: dict = {"index_fields": []}


class _KnowledgeGraphSubclass(KnowledgeGraph):
    pass


class _PlainModel(BaseModel):
    pass


def _no_pipeline_work():
    """Patch everything past validation, so a raise proves it came first."""
    return [
        patch.object(serve_state_module, "get_remote_client", return_value=None),
        patch(
            "EphapticOS.modules.migrations.startup.run_migrations_and_block",
            new_callable=AsyncMock,
            side_effect=AssertionError("migrations ran before validation"),
        ),
        patch.object(
            Ephaptify_module,
            "get_default_tasks",
            new_callable=AsyncMock,
            side_effect=AssertionError("tasks were built before validation"),
        ),
    ]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "kwargs,message",
    [
        ({"graph_model": _Directory, "chunk_attachment": "everything"}, "Invalid chunk_attachment"),
        ({"graph_model": _Directory, "chunk_attachment": False}, "Invalid chunk_attachment"),
        ({"graph_model": KnowledgeGraph, "chunk_attachment": "all"}, "requires a custom DataPoint"),
        (
            {"graph_model": _KnowledgeGraphSubclass, "chunk_attachment": "all"},
            "requires a custom DataPoint",
        ),
        ({"graph_model": _PlainModel, "chunk_attachment": "all"}, "requires a custom DataPoint"),
    ],
)
async def test_invalid_combinations_raise_before_any_pipeline_work(kwargs, message):
    patches = _no_pipeline_work()
    for active in patches:
        active.start()
    try:
        with pytest.raises(ValueError, match=message):
            await Ephaptify_module.Ephaptify(**kwargs)
    finally:
        for active in reversed(patches):
            active.stop()


@pytest.mark.asyncio
async def test_remote_client_raises():
    with (
        patch.object(serve_state_module, "get_remote_client", return_value=MagicMock()),
        pytest.raises(ValueError, match="remote EphapticOS instance"),
    ):
        await Ephaptify_module.Ephaptify(graph_model=_Directory, chunk_attachment="all")


@pytest.mark.asyncio
@patch.object(serve_state_module, "get_remote_client", return_value=None)
@patch("EphapticOS.modules.migrations.startup.run_migrations_and_block", new_callable=AsyncMock)
@patch.object(Ephaptify_module, "get_configured_ontology_resolver", return_value=None)
@patch(
    "EphapticOS.modules.Ephaptify.estimator.estimate_Ephaptify_dry_run",
    new_callable=AsyncMock,
    return_value={"estimate": "stub"},
)
async def test_dry_run_is_permitted(
    mock_estimate,
    mock_get_resolver,
    mock_migrations,
    mock_remote_client,
):
    # dry_run adds no LLM calls and the estimator already excludes embedding cost,
    # so the estimate is correctly unchanged rather than wrongly ignored. Raising
    # here would make Ephaptify(..., chunk_attachment="all", dry_run=True) fail where
    # Ephaptify(..., dry_run=True) succeeds.
    result = await Ephaptify_module.Ephaptify(
        graph_model=_Directory, chunk_attachment="all", dry_run=True
    )

    assert result == {"estimate": "stub"}
    mock_estimate.assert_awaited_once()
    # The estimator covers the two LLM-heavy stages only; attachment is not its business.
    assert "chunk_attachment" not in mock_estimate.await_args.kwargs


@pytest.mark.asyncio
@patch.object(serve_state_module, "get_remote_client", return_value=None)
@patch.object(Ephaptify_module, "get_pipeline_executor")
@patch.object(Ephaptify_module, "get_default_tasks", new_callable=AsyncMock)
@patch("EphapticOS.modules.migrations.startup.run_migrations_and_block", new_callable=AsyncMock)
@patch.object(Ephaptify_module, "get_configured_ontology_resolver", return_value=None)
async def test_valid_value_reaches_get_default_tasks_by_name(
    mock_get_resolver,
    mock_migrations,
    mock_get_default_tasks,
    mock_get_pipeline_executor,
    mock_remote_client,
):
    mock_get_default_tasks.return_value = []
    mock_get_pipeline_executor.return_value = AsyncMock(return_value={})

    await Ephaptify_module.Ephaptify(graph_model=_Directory, chunk_attachment="all")

    assert mock_get_default_tasks.await_args.kwargs["chunk_attachment"] == "all"


@pytest.mark.asyncio
@pytest.mark.parametrize("attachment", [None, "direct", "all"])
async def test_get_default_tasks_binds_chunk_attachment_onto_the_extraction_task(attachment):
    tasks = await Ephaptify_module.get_default_tasks(
        graph_model=_Directory, chunk_size=512, chunk_attachment=attachment
    )

    extraction = next(
        task for task in tasks if task.executable.__name__ == "extract_graph_and_summarize"
    )
    assert extraction.default_params["kwargs"]["chunk_attachment"] == attachment
