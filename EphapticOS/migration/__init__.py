"""Public migration API: move memory into and out of EphapticOS.

Importing from other memory systems (pass any source to ``EphapticOS.remember``)::

    from EphapticOS.migration import Mem0Source, ZepSource, LettaSource

    await EphapticOS.remember(Mem0Source("mem0_export.json"))
    await EphapticOS.remember(ZepSource("graphiti_dump.json", mode="hybrid"))

Exporting (``EphapticOS.export``)::

    snapshot = await EphapticOS.export("main_dataset")     # GraphSnapshot: typed
    alice = snapshot.find(name="Alice")[0]             # real DataPoint objects
    result = await EphapticOS.export("main_dataset", format="graphml")

Restoring / EphapticOS-to-EphapticOS migration::

    await EphapticOS.export("main_dataset", format="cogx", destination="backup_cogx")
    await EphapticOS.remember(COGXArchiveSource("backup_cogx"))
"""

from EphapticOS.modules.migration import (
    COGX_VERSION,
    COGXArchiveSource,
    COGXDocument,
    COGXEntity,
    COGXEpisode,
    COGXFact,
    COGXManifest,
    COGXMemory,
    COGXMemoryBlock,
    COGXRawNode,
    COGXRecord,
    COGXScope,
    COGXTurn,
    EXPORT_FORMATS,
    ExportResult,
    GraphEdge,
    GraphSnapshot,
    GraphitiSource,
    IMPORT_MODES,
    LettaSource,
    Mem0Source,
    MemorySource,
    ZepSource,
    build_snapshot,
    datapoint_registry,
    export_dataset,
    read_archive,
    read_manifest,
    rehydrate_node,
)

__all__ = [
    "COGX_VERSION",
    "EXPORT_FORMATS",
    "IMPORT_MODES",
    "COGXArchiveSource",
    "COGXDocument",
    "COGXEntity",
    "COGXEpisode",
    "COGXFact",
    "COGXManifest",
    "COGXMemory",
    "COGXMemoryBlock",
    "COGXRawNode",
    "COGXRecord",
    "COGXScope",
    "COGXTurn",
    "ExportResult",
    "GraphEdge",
    "GraphSnapshot",
    "GraphitiSource",
    "LettaSource",
    "Mem0Source",
    "MemorySource",
    "ZepSource",
    "build_snapshot",
    "datapoint_registry",
    "export_dataset",
    "read_archive",
    "read_manifest",
    "rehydrate_node",
]
