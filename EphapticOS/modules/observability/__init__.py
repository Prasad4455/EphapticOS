from contextlib import contextmanager

from .trace_context import (
    enable_tracing,
    disable_tracing,
    is_tracing_enabled,
    get_last_trace,
    get_all_traces,
    clear_traces,
)
from .tracing import (
    EphapticOSTrace,
    redact_secrets,
    get_tracer,
    EphapticOS_DB_SYSTEM,
    EphapticOS_DB_QUERY,
    EphapticOS_DB_ROW_COUNT,
    EphapticOS_LLM_MODEL,
    EphapticOS_LLM_PROVIDER,
    EphapticOS_SEARCH_TYPE,
    EphapticOS_SEARCH_QUERY,
    EphapticOS_PIPELINE_TASK_NAME,
    EphapticOS_VECTOR_COLLECTION,
    EphapticOS_VECTOR_RESULT_COUNT,
    EphapticOS_SPAN_CATEGORY,
    EphapticOS_PIPELINE_NAME,
    EphapticOS_RESULT_SUMMARY,
    EphapticOS_RESULT_COUNT,
    # V2 attributes
    EphapticOS_DATASET_NAME,
    EphapticOS_SESSION_ID,
    EphapticOS_SESSION_ENTRY_COUNT,
    EphapticOS_DATA_SIZE_BYTES,
    EphapticOS_DATA_ITEM_COUNT,
    EphapticOS_OPERATION_MODE,
    EphapticOS_RECALL_ROUTE_RULE,
    EphapticOS_RECALL_SCOPE,
    EphapticOS_RECALL_SOURCE,
    EphapticOS_FORGET_TARGET,
    EphapticOS_IMPROVE_STAGES,
    EphapticOS_GRAPH_EDGES_SYNCED,
)
from .metrics import (
    setup_metrics,
    get_meter,
    shutdown_metrics,
    record_operation_duration,
    increment_items_stored,
    increment_items_retrieved,
    increment_items_deleted,
    record_query_results,
    increment_bytes_stored,
    increment_vector_searches,
    increment_graph_edges,
    increment_graph_nodes,
    increment_operation_errors,
    # metric name constants (memory-semconv v0.1.0)
    MEMORY_OPERATION_DURATION,
    MEMORY_ITEMS_STORED,
    MEMORY_ITEMS_RETRIEVED,
    MEMORY_ITEMS_DELETED,
    MEMORY_QUERY_RESULT_COUNT,
    MEMORY_DATA_BYTES_STORED,
    MEMORY_VECTOR_SEARCHES,
    MEMORY_GRAPH_EDGES_ADDED,
    MEMORY_GRAPH_NODES_ADDED,
    MEMORY_OPERATION_ERRORS,
)
from .logs import setup_log_bridge, shutdown_log_bridge

# memory-semconv v0.1.0 span attribute keys
MEMORY_SYSTEM = "memory.system"
MEMORY_OPERATION = "memory.operation"
MEMORY_QUERY_TEXT = "memory.query.text"
MEMORY_QUERY_TYPE = "memory.query.type"
MEMORY_RESULT_COUNT = "memory.result.count"
MEMORY_DATA_SIZE = "memory.data.size"
MEMORY_ITEM_COUNT = "memory.item.count"
MEMORY_COLLECTION = "memory.collection"
MEMORY_STORE_BACKEND = "memory.store.backend"


try:
    from opentelemetry.trace import StatusCode as OtelStatusCode
except ImportError:

    class _StatusCodeFallback:
        ERROR = "ERROR"
        OK = "OK"
        UNSET = "UNSET"

    OtelStatusCode = _StatusCodeFallback  # type: ignore[misc, assignment]


class _NullSpan:
    """No-op span used when tracing is disabled."""

    def __getattr__(self, name):
        return lambda *args, **kwargs: None


def get_tracer_if_enabled() -> object | None:
    """Return the OTEL tracer if tracing is enabled, None otherwise."""
    if is_tracing_enabled():
        return get_tracer()
    return None


@contextmanager
def new_span(name: str):
    """Context manager that creates an OTEL span if tracing is enabled, or yields None."""
    if is_tracing_enabled():
        tracer = get_tracer()
        if tracer is not None:
            with tracer.start_as_current_span(name) as span:
                yield span
                return
    yield _NullSpan()
