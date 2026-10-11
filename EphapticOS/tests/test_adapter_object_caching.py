import asyncio

import EphapticOS
from EphapticOS.infrastructure.databases.graph.get_graph_engine import _create_graph_engine
from EphapticOS.infrastructure.databases.vector.create_vector_engine import _create_vector_engine
from EphapticOS.modules.search.types import SearchType


def assert_cache_sizes(stage: str):
    graph_cache_size = _create_graph_engine.cache_info().currsize
    vector_cache_size = _create_vector_engine.cache_info().currsize

    assert graph_cache_size <= 2, f"Graph engine cache size too large {stage}: {graph_cache_size}"
    assert vector_cache_size <= 2, (
        f"Vector engine cache size too large {stage}: {vector_cache_size}"
    )


async def main():
    await EphapticOS.prune.prune_data()
    await EphapticOS.prune.prune_system(metadata=True)

    dataset_name = "simple_add_Ephaptify_search"
    text = "Berlin is the capital of Germany."

    await EphapticOS.add(data=text, dataset_name=dataset_name)
    await EphapticOS.Ephaptify(datasets=[dataset_name])

    results = await EphapticOS.search(
        query_text="What is the capital of Germany?",
        query_type=SearchType.CHUNKS,
        datasets=[dataset_name],
        only_context=True,
    )

    assert_cache_sizes("after search")

    print(results)

    datasets = await EphapticOS.datasets.list_datasets()
    dataset = next(d for d in datasets if d.name == dataset_name)
    await EphapticOS.datasets.empty_dataset(dataset_id=dataset.id)

    assert_cache_sizes("after delete")

    # Re-add the same dataset name: it resolves to the same deterministic dataset id,
    # so any cached engine that survived the delete (stale connection pool, stale
    # collection metadata) would serve the recreated dataset and fail here.
    await EphapticOS.add(data=text, dataset_name=dataset_name)
    await EphapticOS.Ephaptify(datasets=[dataset_name])

    results = await EphapticOS.search(
        query_text="What is the capital of Germany?",
        query_type=SearchType.CHUNKS,
        datasets=[dataset_name],
        only_context=True,
    )
    assert len(results) > 0, "Search returned no results after dataset re-add"

    assert_cache_sizes("after re-add")


if __name__ == "__main__":
    asyncio.run(main())
