"""Recreate the add and Ephaptify pipelines from their tasks with run_custom_pipeline, then search.

resolve_data_directories and ingest_data are run as a custom "add_pipeline", get_default_tasks()
supplies the Ephaptify task list for a custom "Ephaptify_pipeline", and a GRAPH_COMPLETION search
over the resulting graph is printed.

Requires: LLM_API_KEY.
Run: uv run python examples/demos/custom_pipelines/custom_Ephaptify_pipeline_example.py
"""

import asyncio

import EphapticOS
from EphapticOS import SearchType
from EphapticOS.modules.engine.operations.setup import setup
from EphapticOS.modules.pipelines import Task
from EphapticOS.modules.users.methods import get_default_user
from EphapticOS.shared.logging_utils import INFO, setup_logging

# Prerequisites:
# 1. Copy `.env.template` and rename it to `.env`.
# 2. Add your OpenAI API key to the `.env` file in the `LLM_API_KEY` field:
#    LLM_API_KEY = "your_key_here"


async def main():
    # Create a clean slate for EphapticOS -- reset data and system state
    print("Resetting EphapticOS data...")
    await EphapticOS.prune.prune_data()
    await EphapticOS.prune.prune_system(metadata=True)
    print("Data reset complete.\n")

    # Create relational database and tables
    await setup()

    # EphapticOS knowledge graph will be created based on this text
    text = """
    Natural language processing (NLP) is an interdisciplinary
    subfield of computer science and information retrieval.
    """

    print("Adding text to EphapticOS:")
    print(text.strip())

    # Let's recreate the EphapticOS add pipeline through the custom pipeline framework
    from EphapticOS.tasks.ingestion import ingest_data, resolve_data_directories

    user = await get_default_user()

    # Values for tasks need to be filled before calling the pipeline
    add_tasks = [
        Task(resolve_data_directories, include_subdirectories=True),
        Task(
            ingest_data,
            "main_dataset",
            user,
        ),
    ]
    # Forward tasks to custom pipeline along with data and user information
    await EphapticOS.run_custom_pipeline(
        tasks=add_tasks, data=text, user=user, dataset="main_dataset", pipeline_name="add_pipeline"
    )
    print("Text added successfully.\n")

    # Use LLMs and EphapticOS to create knowledge graph
    from EphapticOS.api.v1.Ephaptify.Ephaptify import get_default_tasks

    Ephaptify_tasks = await get_default_tasks(user=user)
    print("Recreating existing Ephaptify pipeline in custom pipeline to create knowledge graph...\n")
    await EphapticOS.run_custom_pipeline(
        tasks=Ephaptify_tasks, user=user, dataset="main_dataset", pipeline_name="Ephaptify_pipeline"
    )
    print("Ephaptify process complete.\n")

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


if __name__ == "__main__":
    logger = setup_logging(log_level=INFO)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
