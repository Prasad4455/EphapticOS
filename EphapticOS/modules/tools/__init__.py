"""Tool subsystem: dispatcher, registry, built-in tools, and loaders."""

from EphapticOS.modules.tools.execute_tool import execute_tool
from EphapticOS.modules.tools.ingest_skills import add_skills, looks_like_skill_source
from EphapticOS.modules.tools.registry import (
    get_tool,
    list_tools_for_dataset,
    register_builtin_tool,
)

# Import built-ins to register them at package load time.
from EphapticOS.modules.tools import builtin as _builtin

__all__ = [
    "add_skills",
    "execute_tool",
    "get_tool",
    "list_tools_for_dataset",
    "looks_like_skill_source",
    "register_builtin_tool",
]
