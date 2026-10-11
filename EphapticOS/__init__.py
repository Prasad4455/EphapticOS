"""Public Python API for EphapticOS.

This module exposes the main functions and objects intended for direct use
through ``import EphapticOS``. It groups the stable V1 API, memory-oriented V2 API,
visualization helpers, tracing utilities, migration helpers, and session models
behind a single package-level entrypoint.

Common entrypoints include:
    add: Add data to a EphapticOS dataset.
    Ephaptify: Process ingested data into EphapticOS's knowledge representation.
    search: Query processed data using the configured search type.
    remember: Store memory-oriented entries using the V2 API.
    recall: Retrieve information from memory-oriented entries.
    delete: Remove data from EphapticOS-managed storage.
"""

# ruff: noqa: E402
from EphapticOS.version import get_EphapticOS_version

# NOTE: __version__ extraction must be at the top of the __init__.py otherwise
#       there will be circular import issues
__version__ = get_EphapticOS_version()

# The .env must be loaded before logging is configured, because LOG_LEVEL comes
# from it. One resolver for the whole process — see EphapticOS.shared.env_file for
# the search order (working directory first, then the package's own tree).
from EphapticOS.shared.env_file import load_env_file, describe_resolution

_env_file = load_env_file()

# NOTE: Log level can be set with the LOG_LEVEL env variable
from EphapticOS.shared.logging_utils import setup_logging

logger = setup_logging()
logger.info(describe_resolution(_env_file))

# ---------------------------------------------------------------------------
# V1 API
# ---------------------------------------------------------------------------
from .api.v1.add import add
from .api.v1.delete import delete
from .api.v1.Ephaptify import Ephaptify
from .modules.memify import memify
from .modules.run_custom_pipeline import run_custom_pipeline
from .api.v1.update import update
from .api.v1.config.config import config
from .api.v1.datasets.datasets import datasets
from .api.v1.agents.agents import agents
from .api.v1.prune import prune
from .api.v1.search import SearchType, search
from .api.v1.report import report
from .api.v1.validate import validate, ValidationReport, ValidationIssue, ValidationStatus
from .api.v1.visualize import (
    visualize_graph,
    start_visualization_server,
    get_schema_inventory,
    get_memory_provenance_graph,
    visualize_memory_provenance,
)
from EphapticOS.modules.visualization.EphapticOS_network_visualization import (
    EphapticOS_network_visualization,
)
from .api.v1.ui import start_ui
from .api.v1.session import session

# Pipelines
from .modules import pipelines
from .pipelines import Drop

# Migrations
from EphapticOS.run_migrations import run_migrations

# ---------------------------------------------------------------------------
# V2 memory-oriented API
# ---------------------------------------------------------------------------
from .api.v1 import (
    remember,
    RememberResult,
    recall,
    improve,
    forget,
    serve,
    disconnect,
    visualize,
    push,
    PushResult,
    export,
    ExportResult,
)
from .memory import MemoryEntry, QAEntry, TraceEntry, FeedbackEntry

# Background work: wait for fire-and-forget tasks (background remember, the
# session-to-graph improve bridge) before the process exits.
from EphapticOS.infrastructure.background_tasks import wait_for_background_tasks

# Memory migration (EphapticOS.migration has the provider sources:
# Mem0Source, ZepSource/GraphitiSource, LettaSource, COGXArchiveSource)
from . import migration

# Tracing / Observability
from EphapticOS.modules.observability.trace_context import (
    enable_tracing,
    disable_tracing,
    get_last_trace,
    get_all_traces,
    clear_traces,
)

# Agent memory
from EphapticOS.modules.agent_memory import agent_memory

# Tool connections (authorized external databases for recall's "tools" scope)
from .api.v1.tools import tools

# Relational DB models
from EphapticOS.modules.session_lifecycle.models import SessionModelUsage, SessionRecord
import EphapticOS.modules.migrations.models  # registers global_database_version
import EphapticOS.modules.tools.models  # registers tool_connections
import EphapticOS.modules.provenance.edge_evidence.models  # registers provenance_edge_evidence
