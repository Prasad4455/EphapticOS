import os


def configure_EphapticOS_for_subprocess(EphapticOS):
    data_root_directory = os.getenv("EphapticOS_TEST_DATA_ROOT")
    system_root_directory = os.getenv("EphapticOS_TEST_SYSTEM_ROOT")

    if data_root_directory:
        EphapticOS.config.data_root_directory(data_root_directory)
    if system_root_directory:
        EphapticOS.config.system_root_directory(system_root_directory)


def get_kuzu_db_path() -> str:
    return os.getenv("EphapticOS_TEST_KUZU_DB_PATH", "test.db")
