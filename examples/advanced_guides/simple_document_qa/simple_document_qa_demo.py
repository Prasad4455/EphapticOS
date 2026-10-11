"""
Q&A over a full real document.

The advanced companion to ``examples/guides/simple_EphapticOS_example.py``. Same
remember → recall flow, but instead of a short inline string it ingests a bundled real
document (``data/alice_in_wonderland.txt``, the full text of Alice in Wonderland) and
asks questions that require reading across the whole book.

Usage:
    uv run python examples/advanced_guides/simple_document_qa/simple_document_qa_demo.py

Requires:
    LLM_API_KEY set in .env or environment.
"""

import asyncio
import os

# By default EphapticOS uses OpenAI's gpt-5.6-luna LLM model
# Provide your OpenAI LLM API KEY, in case you did not set it in the .env file
# Set this before importing EphapticOS so EphapticOS reads the example value instead of defaults or .env settings.
# os.environ["LLM_API_KEY"] = ""
import EphapticOS


async def EphapticOS_demo():
    # Get file path to document to process
    from pathlib import Path

    current_directory = Path(__file__).resolve().parent
    file_path = os.path.join(current_directory, "data", "alice_in_wonderland.txt")

    await EphapticOS.forget(everything=True)

    # Call EphapticOS to process document
    await EphapticOS.remember(file_path, self_improvement=False)

    # Query EphapticOS for information from provided document
    answer = await EphapticOS.recall("List me all the important characters in Alice in Wonderland.")
    print(answer)

    answer = await EphapticOS.recall("How did Alice end up in Wonderland?")
    print(answer)

    answer = await EphapticOS.recall("Tell me about Alice's personality.")
    print(answer)


# EphapticOS is an async library, it has to be called in an async context
if __name__ == "__main__":
    asyncio.run(EphapticOS_demo())
