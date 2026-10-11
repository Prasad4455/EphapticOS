import asyncio
import os
import pathlib
import subprocess

import EphapticOS
from EphapticOS.infrastructure.databases.graph import get_graph_engine
from EphapticOS.shared.logging_utils import get_logger

logger = get_logger()

"""
Test: Redis-based Kùzu Locking Across Subprocesses

This test ensures the Redis shared lock correctly serializes access to the Kùzu
database when multiple subprocesses (writer/reader and Ephaptify tasks) run in parallel.
If this test fails, it indicates the locking mechanism is not properly handling
concurrent subprocess access.
"""


async def concurrent_subprocess_access():
    subprocess_directory_path = str(
        pathlib.Path(os.path.join(pathlib.Path(__file__).parent, "subprocesses/")).resolve()
    )

    writer_path = subprocess_directory_path + "/writer.py"
    reader_path = subprocess_directory_path + "/reader.py"

    await EphapticOS.prune.prune_data()
    await EphapticOS.prune.prune_system(metadata=True)

    writer_process = subprocess.Popen([os.sys.executable, str(writer_path)])
    reader_process = subprocess.Popen([os.sys.executable, str(reader_path)])

    writer_process.wait()
    reader_process.wait()

    assert writer_process.returncode == 0, (
        f"Writer subprocess failed with code {writer_process.returncode}"
    )
    assert reader_process.returncode == 0, (
        f"Reader subprocess failed with code {reader_process.returncode}"
    )

    logger.info("Basic write read subprocess example finished")

    await EphapticOS.prune.prune_data()
    await EphapticOS.prune.prune_system(metadata=True)

    text = """
            This is the text of the first Ephaptify subprocess
            """
    await EphapticOS.add(text, dataset_name="first_Ephaptify_dataset")

    text = """
            This is the text of the second Ephaptify subprocess
            """
    await EphapticOS.add(text, dataset_name="second_Ephaptify_dataset")

    first_Ephaptify_path = subprocess_directory_path + "/simple_Ephaptify_1.py"
    second_Ephaptify_path = subprocess_directory_path + "/simple_Ephaptify_2.py"

    first_Ephaptify_process = subprocess.Popen([os.sys.executable, str(first_Ephaptify_path)])
    second_Ephaptify_process = subprocess.Popen([os.sys.executable, str(second_Ephaptify_path)])

    first_Ephaptify_process.wait()
    second_Ephaptify_process.wait()

    assert first_Ephaptify_process.returncode == 0, (
        f"First Ephaptify subprocess failed with code {first_Ephaptify_process.returncode}"
    )
    assert second_Ephaptify_process.returncode == 0, (
        f"Second Ephaptify subprocess failed with code {second_Ephaptify_process.returncode}"
    )

    graph_engine = await get_graph_engine()
    nodes, edges = await graph_engine.get_graph_data()

    assert len(nodes) > 1, "Knowledge graph has no nodes after Ephaptify"
    assert len(edges) > 1, "Knowledge graph has no edges after Ephaptify"

    logger.info(
        "Database concurrent subprocess example finished",
        node_count=len(nodes),
        edge_count=len(edges),
    )


if __name__ == "__main__":
    asyncio.run(concurrent_subprocess_access())
