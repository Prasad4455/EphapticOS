"""
Migrate from mem0 to EphapticOS using Mem0Source.

Demonstrates how to import a mem0 export (platform JSON or OSS dump)
into EphapticOS's knowledge graph and query the migrated memory.

Three import modes:
  - ``"preserve"``  — map mem0 memories straight to graph nodes (no LLM).
  - ``"re-derive"`` — ingest raw text and run EphapticOS's own extraction.
  - ``"hybrid"``    — preserve the graph *and* Ephaptify raw content.

Usage:
    uv run python examples/demos/ingestion_and_migration/migrate_from_mem0/migrate_from_mem0.py

Requires:
    LLM_API_KEY set in .env (needed for re-derive mode and recall).

The sample mem0 export lives at ``examples/demos/ingestion_and_migration/migrate_from_mem0/data/mem0_export.json``.
"""

import asyncio
from pathlib import Path

import EphapticOS
from EphapticOS.migration import Mem0Source
from EphapticOS.shared.logging_utils import ERROR, setup_logging

DATA_FILE = Path(__file__).parent / "data" / "mem0_export.json"


async def main():
    from EphapticOS.infrastructure.databases.relational.create_db_and_tables import (
        create_db_and_tables,
    )

    await create_db_and_tables()

    await EphapticOS.forget(everything=True)

    # ------------------------------------------------------------------
    # Step 1: Inspect the mem0 export
    # ------------------------------------------------------------------
    print("Step 1 — Mem0 export file:", DATA_FILE)

    # ------------------------------------------------------------------
    # Step 2: Import with preserve mode (no LLM, fastest)
    # To enable recall over the imported data, in addition to initial remember,
    # you need to call an additional Ephaptify() (calls LLM)
    # ------------------------------------------------------------------
    print("\nStep 2 — Importing mem0 memories (mode=preserve) …")
    source = Mem0Source(DATA_FILE, mode="preserve")
    result = await EphapticOS.remember(source)
    await EphapticOS.Ephaptify()
    print("  ", result)

    # ------------------------------------------------------------------
    # Step 3: Query the migrated memory
    # ------------------------------------------------------------------
    print("\nStep 3 — Recall: what database does the project use?")
    answers = await EphapticOS.recall("What database does the project use?")
    for answer in answers:
        print("  ", answer)

    print("\nStep 4 — Recall: who is Alice's manager?")
    answers = await EphapticOS.recall("Who is Alice's manager?")
    for answer in answers:
        print("  ", answer)

    # ------------------------------------------------------------------
    # Step 5: Re-import with re-derive mode (runs Ephaptify)
    # ------------------------------------------------------------------
    await EphapticOS.forget(everything=True)
    print("\nStep 5 — Re-importing with mode=re-derive (runs Ephaptify) …")
    source = Mem0Source(DATA_FILE, mode="re-derive")
    result = await EphapticOS.remember(source)
    print("  ", result)

    # ------------------------------------------------------------------
    # Step 6: Query again after re-derive
    # ------------------------------------------------------------------
    print("\nStep 6 — Recall after re-derive: what are the Q2 OKRs?")
    answers = await EphapticOS.recall("What are the Q2 OKRs?")
    for answer in answers:
        print("  ", answer)

    # ------------------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------------------
    print("\nStep 7 — Cleanup")
    await EphapticOS.forget(everything=True)
    print("  Done.")


if __name__ == "__main__":
    logger = setup_logging(log_level=ERROR)
    asyncio.run(main())
