from EphapticOS.modules.graph.EphapticOS_graph.EphapticOSGraph import EphapticOSGraph


async def extract_subgraph(subgraphs: list[EphapticOSGraph]):
    for subgraph in subgraphs:
        for edge in subgraph.edges:
            yield edge
