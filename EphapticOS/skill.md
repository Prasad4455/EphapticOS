---
name: EphapticOS
description: >
  Use this skill whenever the user asks about EphapticOS, AI memory, persistent agent memory,
  self-improving agents, agents learning from feedback, knowledge graphs, graph-based RAG,
  long-term memory for agents, short-term memory for agents, personalization, personas,
  temporal search, temporal knowledge graphs, ontology-based extraction, ontology grounding,
  feedback, Cypher search, natural-language graph search, chunk search, RAG search, cross-session memory,
  session feedback, feedback loops, session based memory, redis based memory, knowledge promotion.
  Also use when the user describes the workflow such as:
  "turn documents into a knowledge graph", "build memory from files", "search my graph",
  "extract entities and relations", "sync data into a graph", "update graph memory",
  "store memories for an agent", "help my agent learn over time", "visualize a knowledge
  graph built from documents", "let the agent learn", "adaptive agents", "personalized agents",
  "session based personalization", "find important ontologies", "find custom pydantic models",
  "isolate agentic behaviour", "add permission control to retrieval", "reduce context bloating".
---

# EphapticOS

Use this skill for **EphapticOS-specific Python API help** and for mapping user goals to the right
EphapticOS workflow.

## When to apply this skill

Apply this skill whenever the user wants to do any of the following with EphapticOS:

- ingest text, files, URLs, repos, or datasets
- build or rebuild a knowledge graph
- search documents, chunks, summaries, triplets, or graph context
- choose a `SearchType`
- enrich an existing graph with `improve`
- define custom graph extraction models or `DataPoint` types
- run custom task pipelines
- configure LLM, graph DB, vector DB, or storage settings
- tag and scope memory with `node_set` / NodeSets
- build persistent memory for agents across sessions
- create feedback loops or self-improving agent workflows
- work with temporal extraction, ontologies, Cypher, or natural-language graph queries
- manage datasets, sessions, feedback, deletion, updates, or visualization

If the user's intent is "store information in memory and query it later", prefer EphapticOS's
memory API: **remember -> recall** (plus **improve** to enrich and **forget** to delete).

## Core workflow

```python
import EphapticOS

# Store: ingest + build the graph (+ improve, because self_improvement=True by default)
await EphapticOS.remember(
    "Your text, file path, URL, or list of inputs",
    dataset_name="main",
)

# Query: recall picks a search strategy automatically (rule-based, no LLM call)
results = await EphapticOS.recall("What are the key insights?", datasets=["main"])
for r in results:
    print(r.source, r)  # each result is tagged "graph" / "session" / ...
```

`remember()` runs `add()` + `Ephaptify()` and then `improve()` underneath. `recall()` wraps
`search()` and adds routing, session memory as a source, and `source`-tagged results.

## Default guidance

When helping with EphapticOS:

1. Start with the **simplest working path** unless the user explicitly asks for advanced
   configuration.
2. Prefer the memory API:
   - `remember(...)` to store (ingest + graph build)
   - `recall(...)` to query
   - `improve(...)` to enrich or index an existing graph, and to bridge sessions into it
   - `forget(...)` to delete
3. Treat EphapticOS APIs as **async**.
4. Use `dataset_name` / `datasets` to keep work organized when the user has multiple sources.
5. Use `node_set` when the user wants lightweight tagging, project scoping, per-user memory
   buckets, or subgraph filtering.
6. Pass `query_type=SearchType.X` to `recall()` only when the user needs a specific strategy;
   otherwise let it route.
7. Recommend advanced features only when they match the task:
   - `session_id` for fast short-term memory and conversation continuity
   - `graph_model=` for schema-shaped extraction, `DataPoint` types for direct insertion
   - `extractor="gliner_demo"` for LLM-free graph extraction
   - custom pipelines for non-default task orchestration
   - feedback loops for retrieval improvement
   - visualization tools for graph inspection

## When to drop to the low-level operations

`add()`, `Ephaptify()`, `search()` and `memify()` still ship; the memory API calls them. Reach for
them only when `remember`/`recall` cannot express the job:

- `Ephaptify(datasets=["a", "b"])` or `datasets=None` processes several datasets at once;
  `remember()` always targets exactly one dataset.
- Rebuilding a graph over data already in the DB (after `forget(memory_only=True)`, or with a
  new `graph_model` / ontology) is `Ephaptify()` only; `remember()` always runs `add()` first.
- `search()` takes the agentic extras as first-class parameters (`skills`, `tools`, `max_iter`,
  `code_query`, `node_type`) and returns raw `SearchResult` objects instead of tagged dicts.
- `add()` is a staging area: use it to ingest now and `Ephaptify()` later.
- `prune.prune_system(metadata=True)` also drops the relational DB (users, ACLs, dataset
  registry); `forget()` never touches those. Use prune only for full test teardown.

`memify()` and `improve()` are the same enrichment pipeline; recommend `improve()`.
`EphapticOS.delete()` is deprecated in favour of `forget()`. Full comparison of the two query
functions: `docs/recall-vs-search.md`.

## Common tasks

### Store data

`remember()` accepts text, file paths, URLs, directories, git repository URLs, binary streams,
or lists of these.

```python
await EphapticOS.remember("notes.md", dataset_name="research")
await EphapticOS.remember("https://example.com", dataset_name="research")
await EphapticOS.remember(["paper.pdf", "summary.txt"], dataset_name="research")
```

Use `node_set` when the user wants data grouped into logical memory buckets.

```python
await EphapticOS.remember(
    "Customer prefers concise weekly summaries and Slack delivery.",
    dataset_name="customer_success",
    node_set=["preferences", "customer_123", "weekly_reports"],
)
```

Useful options:

```python
await EphapticOS.remember(
    "...",
    dataset_name="research",
    self_improvement=False,  # skip the improve() stage (faster, no triplet index)
    run_in_background=True,  # return immediately; poll the pipeline status
    chunk_size=1024,
    custom_prompt="Extract companies, products, and partnerships.",
    extractor="gliner_demo",  # LLM-free extraction; needs EphapticOS[gliner]
    dry_run=True,  # estimate LLM tokens/cost without ingesting
)
await EphapticOS.remember("./my_repo", dataset_name="code")  # code graph, no LLM
await EphapticOS.remember("./skills", dataset_name="ops", content_type="skills")  # SKILL.md playbooks
```

### Query memory

```python
from EphapticOS import SearchType

results = await EphapticOS.recall("What changed in Q1 2024?", datasets=["research"], top_k=10)

# Pin a strategy when the user needs one
results = await EphapticOS.recall(
    "What changed in Q1 2024?",
    query_type=SearchType.TEMPORAL,
    datasets=["research"],
)

# Answers with evidence, or validated into a Pydantic model
results = await EphapticOS.recall("...", include_references=True)
results = await EphapticOS.recall("...", response_model=MyAnswerModel)

# Retrieval context only, no LLM completion (pin query_type here)
context = await EphapticOS.recall("...", query_type=SearchType.GRAPH_COMPLETION, only_context=True)
```

### Scope retrieval with NodeSets

Use NodeSets when the user wants to search only a subset of memory such as one project, one
customer, one user, or one workflow.

```python
results = await EphapticOS.recall(
    "What are this customer's reporting preferences?",
    datasets=["customer_success"],
    node_name=["preferences", "customer_123"],
)
```

### Enrich an existing graph

Use `improve()` when the user wants to improve or extend an already-built graph without
re-ingesting. Without `session_ids` it extracts and indexes triplet embeddings; with them it
also applies feedback weights, persists session Q&A, and distills session lessons into the graph.

```python
await EphapticOS.improve(dataset="research")
await EphapticOS.improve(dataset="research", session_ids=["chat_1"])
await EphapticOS.improve(dataset="research", build_global_context_index=True)
```

### Delete data

`forget()` is the single deletion entry point.

```python
await EphapticOS.forget(data_id=data_id, dataset_id=dataset_id)  # one document
await EphapticOS.forget(dataset="research")  # a dataset: raw data + graph + vectors
await EphapticOS.forget(dataset="research", memory_only=True)  # graph + vectors only, keep raw files
await EphapticOS.forget(everything=True)  # everything the current user owns
```

### Update a document in place

```python
await EphapticOS.update(data_id=data_id, data="Updated content", dataset_id=dataset_id)
```

The document keeps its `data_id`; only the chunks the edit touched are re-extracted.

### Create domain-specific structures

Pass a `DataPoint`-derived Pydantic model as `graph_model` and the LLM fills it instead of the
generic knowledge graph:

```python
from EphapticOS.infrastructure.engine import DataPoint


class Person(DataPoint):
    name: str
    role: str
    metadata: dict = {"index_fields": ["name"], "identity_fields": ["name"]}


class Company(DataPoint):
    name: str
    employs: list[Person] = []  # a DataPoint field becomes an edge named after the field
    metadata: dict = {"index_fields": ["name"], "identity_fields": ["name"]}


await EphapticOS.remember("...", dataset_name="org", graph_model=Company)
```

Insert structured Python objects directly, bypassing text extraction:

```python
from EphapticOS.tasks.storage import add_data_points

await add_data_points([Person(name="Ada", role="Engineer")])
```

See `examples/guides/custom_graph_model.py` and `examples/guides/custom_data_models.py`.

### Run custom pipelines

Use `run_custom_pipeline(...)` when the user needs explicit sequential task control.

```python
from EphapticOS.modules.pipelines.tasks.task import Task


async def my_task(data):
    return data


await EphapticOS.run_custom_pipeline(
    tasks=[Task(my_task)],
    data="input",
    dataset="research",
)
```

## DataPoints

A `DataPoint` is the **atomic unit of knowledge** in EphapticOS.

Use this concept whenever the user asks how EphapticOS represents structured data internally or how
to insert graph objects directly.

Key ideas:

- A `DataPoint` is a Pydantic model that represents one meaningful unit of information.
- When inserted, DataPoints become graph nodes; fields holding other DataPoints become edges.
- `metadata = {"index_fields": [...]}` controls which fields are embedded for semantic search.
- `metadata = {"identity_fields": [...]}` makes the node id deterministic so repeated inserts
  merge instead of duplicating.

Use `DataPoint` when the user wants:

- schema-shaped memory
- exact control over graph structure
- programmatic relationship creation
- custom domain entities such as papers, customers, incidents, policies, products, or workflows

Prefer plain `remember(...)` for unstructured documents. Prefer `graph_model=` when the text
should be extracted into a schema. Prefer `DataPoint` models plus `add_data_points(...)` when the
user already has structured Python objects.

## NodeSets

Use NodeSets when the user wants a lightweight way to **tag, group, and scope memory**.

A NodeSet starts as a list of tags passed through `node_set=[...]` to `remember(...)`; after the
graph is built those tags are first-class graph nodes, and `recall(node_name=[...])` restricts
retrieval to them.

### Good NodeSet patterns

- per customer: `["customer_123"]`
- per workflow: `["support_bot", "refund_flow"]`
- per topic: `["contracts", "vendor_risk"]`
- per environment: `["prod", "staging"]`
- per user memory: `["user_42", "preferences"]`

### Example

```python
await EphapticOS.remember(
    [
        "Alice prefers terse answers and email follow-ups.",
        "Alice escalates billing issues to finance first.",
        "Bob prefers detailed technical explanations.",
    ],
    dataset_name="agent_memory",
    node_set=["crm", "user_profiles"],
)

results = await EphapticOS.recall(
    "How should I respond to Alice?",
    datasets=["agent_memory"],
    node_name=["crm", "user_profiles"],
)
```

Use NodeSets by default whenever the user says things like:

- "scope memory by customer"
- "separate projects without making separate databases"
- "let the agent search only its own memories"
- "group facts by workflow or team"

## SearchType selection guide

`recall()` routes automatically when `query_type` is omitted. When the user needs a specific
strategy, pick from `EphapticOS.SearchType` (all 20 values):

Completion types (an LLM writes the answer):

- `HYBRID_COMPLETION`: document passages plus entity neighbourhoods; the default when routing is off
- `GRAPH_COMPLETION`: graph traversal + completion; the best general graph-aware Q&A
- `GRAPH_COMPLETION_COT`: deeper chain-of-thought reasoning over graph context
- `GRAPH_COMPLETION_CONTEXT_EXTENSION`: broader graph context retrieval
- `GRAPH_COMPLETION_DECOMPOSITION`: splits the question into sub-queries first
- `GRAPH_SUMMARY_COMPLETION`: graph context + pre-computed summaries
- `RAG_COMPLETION`: traditional RAG over document chunks
- `TRIPLET_COMPLETION`: subject-predicate-object style graph Q&A
- `TEMPORAL`: time-aware graph search
- `AGENTIC_COMPLETION`: multi-step loop that can load `skills` and call `tools`

Retrieval-only types (no LLM call):

- `CHUNKS`: semantic retrieval over chunks
- `CHUNKS_LEXICAL`: exact-term / keyword (BM25) matching
- `SUMMARIES`: pre-computed document summaries
- `SKILLS`: discover SKILL.md playbooks (metadata only; exactly one dataset)
- `CODE`: deterministic code-graph operations via `code_query` (callers, paths, impact analysis)

Other:

- `CYPHER`: raw Cypher, on by default (`ALLOW_CYPHER_QUERY=false` disables it; not on the Postgres demo graph)
- `NATURAL_LANGUAGE`: natural language to graph query
- `CODING_RULES`: retrieve stored coding rules
- `GRAPH_REPORT`: graph insight report (hubs, cross-source links, suggested questions)
- `FEELING_LUCKY`: let EphapticOS choose

The CLI exposes 10 of these (`EphapticOS-cli recall --query-type`); the rest are SDK-only.

## Sessions, feedback, and self-improvement

EphapticOS has two memory tiers:

- **Permanent memory**: `remember(...)` without `session_id` — the knowledge graph.
- **Session memory**: `remember(..., session_id=...)` — a fast session cache written without an
  LLM call. `recall(..., session_id=...)` searches it first and falls through to the graph.
  Requires `CACHING=true` (the default).

```python
# Short-term: store a turn in the session cache, recall it instantly
await EphapticOS.remember("User wants weekly summaries on Fridays.", session_id="chat_1")
results = await EphapticOS.recall("when does the user want summaries?", session_id="chat_1")

# Long-term: bridge the session into the permanent graph
await EphapticOS.improve(dataset="main_dataset", session_ids=["chat_1"])
```

`remember(..., session_id=...)` with `self_improvement=True` (default) bridges into the graph
in the background, so the explicit `improve()` call is only needed for control over timing.

### Feedback

Feedback is attached to a session Q&A entry and later folded into retrieval weights by
`improve()`:

```python
from EphapticOS import FeedbackEntry

# Rate an earlier answer (qa_id is the entry_id returned by the remember() that stored it)
await EphapticOS.remember(
    FeedbackEntry(qa_id=qa_id, feedback_score=5, feedback_text="Captured the key themes."),
    session_id="chat_1",
)
# Equivalent helper API
await EphapticOS.session.add_feedback(session_id="chat_1", qa_id=qa_id, feedback_score=5)
history = await EphapticOS.session.get_session(session_id="chat_1")
```

With `AUTO_FEEDBACK=true` (default) every answered turn is also analysed for implicit feedback
by one structured-output LLM call. Set `AUTO_FEEDBACK=false` for low-latency reads.

### Wrap an agent

`@EphapticOS.agent_memory` records an agent function's calls as session traces and recalls context
before each call. See `examples/guides/agent_memory_quickstart.py`.

## Agentic workflows and feedback-driven improvement

Use EphapticOS as the **memory layer for agent systems** that need to improve over time through
better recall, better reuse of prior work, and better retrieval of successful past behavior.

The key idea is simple:

- keep the **agent workflow itself constant**
- keep the **prompt and tools constant**
- change only what the agent can remember and retrieve

"Improvement" comes from **memory reuse and retrieval quality**, not from changing the model.

### General agent loop

1. **Observe** — capture inputs, events, preferences, outcomes, errors, decisions.
2. **Store** — `remember(...)` them, with `session_id` for the active run and without it for
   durable facts.
3. **Organize** — use datasets and NodeSets to separate memory by customer, workflow, team,
   agent, or topic.
4. **Recall before acting** — `recall(...)` before planning, tool use, synthesis, or response
   generation.
5. **Capture feedback** — `FeedbackEntry` / `session.add_feedback` for what worked and what
   did not.
6. **Consolidate** — `improve(dataset, session_ids=[...])` so session history and lessons become
   long-term graph memory.
7. **Reuse** — future runs benefit from richer context and more informed retrieval.

### Minimal example pattern

```python
import EphapticOS

# 1) Store a durable observation
await EphapticOS.remember(
    "Customer 123 prefers concise status updates and Slack notifications.",
    dataset_name="agent_memory",
    node_set=["customer_123", "preferences", "support_agent"],
)

# 2) Recall before acting, inside a session
context = await EphapticOS.recall(
    "What should I know before replying to customer 123?",
    datasets=["agent_memory"],
    session_id="support-session-123",
)

# 3) Continue work in the same session
answer = await EphapticOS.recall(
    "Draft the best reply for customer 123.",
    datasets=["agent_memory"],
    session_id="support-session-123",
)

# 4) Consolidate the session into long-term memory later
await EphapticOS.improve(dataset="agent_memory", session_ids=["support-session-123"])
```

### Best default explanation

If the user asks how EphapticOS helps agents improve over time:

**EphapticOS lets agents improve by remembering more useful things, organizing them into searchable
graph memory, and reusing successful past work in future runs.**

## Configuration help

Use EphapticOS config helpers or environment variables when the user needs provider or backend setup.

```python
EphapticOS.config.set_llm_provider("openai")
EphapticOS.config.set_llm_model("gpt-5-mini")
EphapticOS.config.set_llm_api_key("sk-...")
```

Environment variables (`.env`): `LLM_API_KEY`, `LLM_MODEL`, `LLM_PROVIDER`, `EMBEDDING_*`,
`GRAPH_DATABASE_PROVIDER` (ladybug default, neo4j, neptune, postgres_demo), `VECTOR_DB_PROVIDER`
(lancedb default, pgvector, turso), `DB_PROVIDER` (sqlite default, postgres), `CACHE_BACKEND`.
If only the LLM or only embeddings are configured, the other defaults to OpenAI.

## Dataset and lifecycle operations

```python
datasets = await EphapticOS.datasets.list_datasets()
data = await EphapticOS.datasets.list_data(dataset_id)
await EphapticOS.forget(dataset="research")  # preferred over datasets.empty_dataset / delete_all
```

## Visualization

`visualize_graph` renders a **bounded subgraph** by default (seed nodes + a k-hop neighborhood,
capped at `max_nodes`) instead of the whole graph.

```python
# Default: bounded subgraph. Seed by a query, explicit ids, or a recall result;
# with none of those, the highest-degree nodes seed a representative view.
await EphapticOS.visualize_graph("/path/to/output.html")
await EphapticOS.visualize_graph("/path/to/output.html", query="What relates to Python?")
await EphapticOS.visualize_graph("/path/to/output.html", seed_node_ids=["node-id-1"])
await EphapticOS.visualize_graph("/path/to/output.html", recall_result=recall_output)

# Legacy whole-graph render.
await EphapticOS.visualize_graph("/path/to/output.html", full=True)

await EphapticOS.start_visualization_server(port=8080)
await EphapticOS.start_ui()
```

Caps: `neighborhood_depth=2`, `neighborhood_seed_top_k=10`, `max_nodes=500`.
See `examples/guides/graph_visualization.py`.

## Full reset (tests only)

`forget(everything=True)` removes the user's data and memory. To also drop users, ACLs and the
dataset registry — full test teardown — use prune:

```python
await EphapticOS.prune.prune_data()
await EphapticOS.prune.prune_system(graph=True, vector=True, metadata=True, cache=True)
```

## Important behavior notes

- EphapticOS APIs are **async**.
- Prefer **remember -> recall** (+ `improve`, `forget`) unless the user needs one low-level stage.
- Use `node_set` early when the user may later need scoped retrieval.
- Use `session_id` for short-term memory and conversation continuity; `improve(session_ids=...)`
  to make it permanent.
- Use `graph_model=` or `DataPoint` types only when the user needs schema-shaped extraction.
- Use `CYPHER` only when Cypher querying is enabled in config.
- Keep examples minimal and runnable.

## Do not overcomplicate

Do not jump straight to advanced backends, ontology configuration, or custom pipelines unless the
user asks for them or the problem clearly requires them. Prefer the smallest correct EphapticOS
solution first, then extend it.
