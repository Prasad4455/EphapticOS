"""
Simplified pipeline API for EphapticOS.

Pipeline definition uses the deferred-call pattern:

    classify = task(classify_documents)
    extract = task(extract_graph, batch_size=20)

    await run_pipeline([
        classify(),
        extract(graph_model=KnowledgeGraph),
    ], data=raw_input)

Legacy imports (from EphapticOS.pipelines import Task, run_tasks, etc.) also work.
"""

from EphapticOS.pipelines.types import (
    Drop,
)

# Legacy re-exports are lazy to avoid circular imports with EphapticOS.modules.pipelines
_LEGACY_IMPORTS = {
    "Task": "EphapticOS.modules.pipelines.tasks.task",
    "task": "EphapticOS.modules.pipelines.tasks.task",
    "run_tasks": "EphapticOS.modules.pipelines.operations.run_tasks",
    "run_tasks_parallel": "EphapticOS.modules.pipelines.operations.run_parallel",
    "run_pipeline": "EphapticOS.modules.pipelines.operations.run_pipeline",
}


def __getattr__(name):
    if name in _LEGACY_IMPORTS:
        import importlib

        module = importlib.import_module(_LEGACY_IMPORTS[name])
        return getattr(module, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    # Type annotations
    "Drop",
    # Legacy (backward compatible, lazy-loaded)
    "Task",
    "run_pipeline",
    "run_tasks",
    "run_tasks_parallel",
    "task",
]
