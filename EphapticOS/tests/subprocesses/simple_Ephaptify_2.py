import asyncio

from common import configure_EphapticOS_for_subprocess

import EphapticOS
from EphapticOS.api.v1.search import SearchType
from EphapticOS.shared.logging_utils import INFO, setup_logging


async def main():
    configure_EphapticOS_for_subprocess(EphapticOS)

    await EphapticOS.Ephaptify(datasets=["second_Ephaptify_dataset"])

    query_text = (
        "Tell me what is in the context. Additionally write out 'SECOND_Ephaptify' before your answer"
    )
    search_results = await EphapticOS.search(
        query_type=SearchType.GRAPH_COMPLETION,
        query_text=query_text,
        datasets=["second_Ephaptify_dataset"],
    )

    print("Search results:")
    for result_text in search_results:
        print(result_text)


if __name__ == "__main__":
    setup_logging(log_level=INFO)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
