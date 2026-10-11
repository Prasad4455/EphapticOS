import os
import pathlib

import EphapticOS
from EphapticOS.modules.search.operations import get_history
from EphapticOS.modules.search.types import SearchType
from EphapticOS.modules.users.methods import get_default_user
from EphapticOS.shared.logging_utils import get_logger

logger = get_logger()


async def main():
    data_directory_path = str(
        pathlib.Path(
            os.path.join(pathlib.Path(__file__).parent, ".data_storage/test_library")
        ).resolve()
    )
    EphapticOS.config.data_root_directory(data_directory_path)
    EphapticOS_directory_path = str(
        pathlib.Path(
            os.path.join(pathlib.Path(__file__).parent, ".EphapticOS_system/test_library")
        ).resolve()
    )
    EphapticOS.config.system_root_directory(EphapticOS_directory_path)

    await EphapticOS.prune.prune_data()
    await EphapticOS.prune.prune_system(metadata=True)

    await EphapticOS.add(["TEST1"], "test1")
    await EphapticOS.add(["TEST2"], "test2")

    task_1_config = {
        "vector_db_url": "EphapticOS1.test",
        "vector_db_key": "",
        "vector_db_provider": "lancedb",
        "vector_db_name": "",
    }
    task_2_config = {
        "vector_db_url": "EphapticOS2.test",
        "vector_db_key": "",
        "vector_db_provider": "lancedb",
        "vector_db_name": "",
    }

    task_1_graph_config = {
        "graph_database_provider": "ladybug",
        "graph_file_path": "ladybug1.db",
    }
    task_2_graph_config = {
        "graph_database_provider": "ladybug",
        "graph_file_path": "ladybug2.db",
    }

    # schedule both Ephaptify calls concurrently
    task1 = asyncio.create_task(
        EphapticOS.Ephaptify(
            ["test1"], vector_db_config=task_1_config, graph_db_config=task_1_graph_config
        )
    )
    task2 = asyncio.create_task(
        EphapticOS.Ephaptify(
            ["test2"], vector_db_config=task_2_config, graph_db_config=task_2_graph_config
        )
    )

    # wait until both are done (raises first error if any)
    await asyncio.gather(task1, task2)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main(), debug=True)
