import asyncio

import EphapticOS
from EphapticOS.api.v1.search import SearchType
from EphapticOS.shared.logging_utils import ERROR, setup_logging


async def main():
    # Create a clean slate for EphapticOS -- reset data and system state
    print("Resetting EphapticOS data...")
    await EphapticOS.prune.prune_data()
    await EphapticOS.prune.prune_system(metadata=True)
    print("Data reset complete.\n")

    # EphapticOS knowledge graph will be created based on this text
    text = """
    Natural language processing (NLP) is an interdisciplinary
    subfield of computer science and information retrieval.
    """
    from EphapticOS.tasks.ingestion.data_item import DataItem

    test_item = DataItem(text, "test_item")
    # Add the text, and make it available for Ephaptify
    await EphapticOS.add(test_item)

    # Use LLMs and EphapticOS to create knowledge graph
    ret_val = await EphapticOS.Ephaptify()

    query_text = "Tell me about NLP"
    print(f"Searching EphapticOS for insights with query: '{query_text}'")
    # Query EphapticOS for insights on the added text
    search_results = await EphapticOS.search(
        query_type=SearchType.GRAPH_COMPLETION, query_text=query_text
    )

    print("Search results:")
    # Display results
    for result_text in search_results:
        print(result_text)

    from EphapticOS.modules.data.methods.get_dataset_data import get_dataset_data

    for pipeline in ret_val.values():
        dataset_id = pipeline.dataset_id

    dataset_data = await get_dataset_data(dataset_id=dataset_id)

    from fastapi.encoders import jsonable_encoder

    # Data rows are dataset-scoped: the encoded row carries dataset_id itself.
    data = [jsonable_encoder(data) for data in dataset_data]

    # Check if label is properly added and stored
    assert data[0]["label"] == "test_item"


if __name__ == "__main__":
    logger = setup_logging(log_level=ERROR)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
