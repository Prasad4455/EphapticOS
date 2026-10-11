"""Compare recall before and after improve() bridges a session's memory into the dataset graph.

One fact is remembered permanently and another only in a session; "What did Bohr work on?" is
recalled from the dataset before and after improve(dataset, session_ids=[...]) so the printed
answers show the session fact becoming part of the graph.

Requires: LLM_API_KEY.
Run: uv run python examples/guides/improve_quickstart.py
"""

import asyncio

import EphapticOS

DATASET = "demo_dataset"
SESSION = "demo_session"


async def main():
    await EphapticOS.forget(everything=True)

    await EphapticOS.remember(
        "Einstein developed general relativity.",
        dataset_name=DATASET,
        self_improvement=False,
    )

    await EphapticOS.remember(
        "Niels Bohr worked on atomic structure.",
        dataset_name=DATASET,
        session_id=SESSION,
        self_improvement=False,
    )

    answer_before_improve = await EphapticOS.recall(
        "What did Bohr work on?",
        datasets=[DATASET],
    )

    await EphapticOS.improve(dataset=DATASET, session_ids=[SESSION])

    answer_after_improve = await EphapticOS.recall(
        "What did Bohr work on?",
        datasets=[DATASET],
    )
    print("Before improve:", answer_before_improve)

    print("After improve:", answer_after_improve)


if __name__ == "__main__":
    asyncio.run(main())
