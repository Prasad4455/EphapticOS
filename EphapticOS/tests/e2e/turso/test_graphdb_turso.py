"""End-to-end graph database test using the Turso (rewrite engine) backend.

Exercises the full add -> Ephaptify -> search pipeline against a local Turso database
file. Requires:
  - LLM_API_KEY set for Ephaptify
  - A working vector database (default LanceDB is fine)
  - the turso extra (pip install EphapticOS"[turso]")

Turso is local and needs no server, so no connection setup is required.
"""

import asyncio

from EphapticOS.tests.e2e.postgres.test_graphdb_shared import run_graph_db_test


async def main():
    await run_graph_db_test("turso")


if __name__ == "__main__":
    asyncio.run(main())
