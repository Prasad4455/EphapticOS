import os
import pathlib

import EphapticOS
from EphapticOS.api.v1.search import SearchType
from EphapticOS.infrastructure.databases.graph import get_graph_engine
from EphapticOS.infrastructure.engine import Edge
from EphapticOS.low_level import DataPoint


async def main():
    class Activity(DataPoint):
        name: str
        metadata: dict = {"index_fields": ["name"], "identity_fields": ["name"]}

    class Person(DataPoint):
        name: str
        likes: list[Activity] | None = None
        metadata: dict = {"index_fields": ["name"], "identity_fields": ["name"]}

    class PeopleGraph(DataPoint):
        people: list[Person]
        friends_with: list[Edge[Person, Person]]

    data_directory_path = str(
        pathlib.Path(
            os.path.join(
                pathlib.Path(__file__).parent, ".data_storage/test_custom_model_relationships"
            )
        ).resolve()
    )
    EphapticOS.config.data_root_directory(data_directory_path)
    EphapticOS_directory_path = str(
        pathlib.Path(
            os.path.join(
                pathlib.Path(__file__).parent, ".EphapticOS_system/test_custom_model_relationships"
            )
        ).resolve()
    )
    EphapticOS.config.system_root_directory(EphapticOS_directory_path)

    await EphapticOS.prune.prune_data()
    await EphapticOS.prune.prune_system(metadata=True)

    text = (
        "Alice likes biking and swimming. Bob likes playing basketball. "
        "Alice and Bob are friends. "
        "Charlie likes skiing. "
        "Alice and Bob like playing board games together."
    )
    custom_prompt = (
        "Extract all people mentioned in the text. "
        "For each person, extract ALL activities they like, including shared activities. "
        "Also extract friendships between people."
    )

    await EphapticOS.add(text)
    await EphapticOS.Ephaptify(graph_model=PeopleGraph, custom_prompt=custom_prompt)

    graph_engine = await get_graph_engine()
    nodes, edges = await graph_engine.get_graph_data()
    nodes_by_id = {str(node[0]): node[1] for node in nodes}
    friend_pairs = {
        (nodes_by_id[str(edge[0])].get("name"), nodes_by_id[str(edge[1])].get("name"))
        for edge in edges
        if edge[2] == "friends_with"
    }
    assert friend_pairs, f"No friends_with edges in { {edge[2] for edge in edges} }"
    assert ("Alice", "Bob") in friend_pairs or ("Bob", "Alice") in friend_pairs, friend_pairs

    # Written edges must also be retrievable: a graph search's context has to surface
    # the relationship, not just the graph engine's raw dump.
    search_context = await EphapticOS.search(
        query_type=SearchType.GRAPH_COMPLETION,
        query_text="Who is friends with whom?",
        only_context=True,
    )
    context_text = " ".join(str(item) for item in search_context)
    assert "friends_with" in context_text, context_text


if __name__ == "__main__":
    import asyncio

    asyncio.run(main(), debug=True)
