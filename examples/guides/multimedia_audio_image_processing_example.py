"""Remember a bundled MP3 and PNG, then recall their summaries with SearchType.SUMMARIES.

The audio is transcribed and the image described before graph extraction; the recall prints the
document summaries EphapticOS produced for both files. IMAGE_EXTRACTION_ENABLED and IMAGE_OCR_ENABLED
(needs EphapticOS[rapidocr]) optionally enrich image ingestion.

Requires: LLM_API_KEY.
Run: uv run python examples/guides/multimedia_audio_image_processing_example.py
"""

import asyncio
import os
import pathlib

import EphapticOS
from EphapticOS import SearchType
from EphapticOS.shared.logging_utils import ERROR, setup_logging

# Prerequisites:
# 1. Copy `.env.template` and rename it to `.env`.
# 2. Add your OpenAI API key to the `.env` file in the `LLM_API_KEY` field:
#    LLM_API_KEY = "your_key_here"
#
# Optional richer image ingestion (both default off, see `.env.template`):
#   IMAGE_EXTRACTION_ENABLED — extraction-oriented transcription prompt (entities/values/relations)
#   IMAGE_OCR_ENABLED         — append local OCR text; needs pip install "EphapticOS[rapidocr]"


async def main():
    # Create a clean slate for EphapticOS -- reset data and system state
    await EphapticOS.forget(everything=True)

    # EphapticOS knowledge graph will be created based on the text
    # and description of these files
    mp3_file_path = os.path.join(
        pathlib.Path(__file__).parent,
        "multimedia_audio_image_processing_example_data/text_to_speech.mp3",
    )
    png_file_path = os.path.join(
        pathlib.Path(__file__).parent,
        "multimedia_audio_image_processing_example_data/example.png",
    )

    # Remember the files and create knowledge graph memory
    await EphapticOS.remember([mp3_file_path, png_file_path], self_improvement=False)

    # Query EphapticOS for summaries of the data in the multimedia files
    search_results = await EphapticOS.recall(
        query_type=SearchType.SUMMARIES,
        query_text="What is in the multimedia files?",
    )

    # Display search results
    for result_text in search_results:
        print(result_text)


if __name__ == "__main__":
    logger = setup_logging(log_level=ERROR)
    asyncio.run(main())
