import asyncio

from EphapticOS.modules.chunking.models.DocumentChunk import DocumentChunk
from EphapticOS.modules.ontology.base_ontology_resolver import BaseOntologyResolver
from EphapticOS.modules.pipelines.tasks.task import task_summary
from EphapticOS.shared.data_models import KnowledgeGraph
from EphapticOS.tasks.graph.cascade_extract.utils.extract_content_nodes_and_relationship_names import (
    extract_content_nodes_and_relationship_names,
)
from EphapticOS.tasks.graph.cascade_extract.utils.extract_edge_triplets import (
    extract_edge_triplets,
)
from EphapticOS.tasks.graph.cascade_extract.utils.extract_nodes import extract_nodes
from EphapticOS.tasks.graph.extract_graph_from_data import integrate_chunk_graphs


@task_summary("Extracted graph from {n} chunk(s)")
async def extract_graph_from_data(
    data_chunks: list[DocumentChunk],
    n_rounds: int = 2,
    ontology_resolver: BaseOntologyResolver = None,
    ctx=None,
) -> list[DocumentChunk]:
    """Extract and update graph data from document chunks using cascade extraction.

    This function performs multi-step graph extraction from document chunks,
    using cascade extraction techniques to build comprehensive knowledge graphs.

    Args:
        data_chunks: List of document chunks to process
        n_rounds: Number of extraction rounds to perform (default: 2)
        ontology_resolver: Resolver for matching and enriching extracted entities
            from the ontology (annotation only by default; ONTOLOGY_MODE=strict drops
            entities with no ontology grounding)

    Returns:
        List of updated DocumentChunk objects with extracted graph data
    """
    chunk_nodes = await asyncio.gather(
        *[extract_nodes(chunk.text, n_rounds) for chunk in data_chunks]
    )

    chunk_results = await asyncio.gather(
        *[
            extract_content_nodes_and_relationship_names(chunk.text, nodes, n_rounds)
            for chunk, nodes in zip(data_chunks, chunk_nodes)
        ]
    )

    updated_nodes, relationships = zip(*chunk_results)

    chunk_graphs = await asyncio.gather(
        *[
            extract_edge_triplets(chunk.text, nodes, rels, n_rounds)
            for chunk, nodes, rels in zip(data_chunks, updated_nodes, relationships)
        ]
    )

    return await integrate_chunk_graphs(
        data_chunks=data_chunks,
        chunk_graphs=chunk_graphs,
        graph_model=KnowledgeGraph,
        ontology_resolver=ontology_resolver,
        ctx=ctx,
    )
