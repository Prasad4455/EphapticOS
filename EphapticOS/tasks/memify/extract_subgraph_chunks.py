from EphapticOS.modules.graph.EphapticOS_graph.EphapticOSGraph import EphapticOSGraph


async def extract_subgraph_chunks(subgraphs: list[EphapticOSGraph]):
    """
    Get all Document Chunks from subgraphs and forward to next task in pipeline
    """
    for subgraph in subgraphs:
        for node in subgraph.nodes.values():
            if node.attributes["type"] == "DocumentChunk":
                yield node.attributes["text"]
