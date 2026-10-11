import importlib.metadata
import os
from contextlib import suppress
from pathlib import Path


def get_EphapticOS_version() -> str:
    """Returns either the version of installed EphapticOS package or the one
    found in nearby pyproject.toml"""
    with (
        suppress(FileNotFoundError, StopIteration),
        open(
            os.path.join(Path(__file__).parent.parent, "pyproject.toml"), encoding="utf-8"
        ) as pyproject_toml,
    ):
        version = (
            next(line for line in pyproject_toml if line.startswith("version"))
            .split("=")[1]
            .strip("'\"\n ")
        )
        # Mark the version as a local EphapticOS library by appending “-dev”
        return f"{version}-local"
    try:
        return importlib.metadata.version("EphapticOS")
    except importlib.metadata.PackageNotFoundError:
        return "unknown"
