# EphapticOS High-Level Runtime Architecture

This document summarizes the high-level runtime architecture of **EphapticOS** generated and verified with **Archify**.

![EphapticOS Runtime Architecture (2400 × 1260)](file:///C:/Users/Deepe/.gemini/antigravity-ide/brain/75c30846-69cc-41b6-9aa1-5b889e9b504b/ephapticos-runtime.2400x1260.png)

---

## 1. Architecture Overview & Core Components

The architecture models **18 core runtime components** categorized across clear architectural roles, connected by real codebase entrypoints at revision `65a2f532a46eafa8cad923ee198f5add05c6b214`:

| Component ID | Label | Type | Role & Codebase Evidence |
| :--- | :--- | :--- | :--- |
| `ui_client` | **Web UI Client** | `frontend` | Next.js development and demo dashboard ([`package.json`](file:///c:/TruPrints99/Ai_LLM_Project/AntiGravity_Projects/EphapticOS/EphapticOS-frontend/package.json#L1-L25)) |
| `cli_tool` | **EphapticOS CLI** | `frontend` | Terminal interface for `remember`, `recall`, `improve` ([`_EphapticOS.py`](file:///c:/TruPrints99/Ai_LLM_Project/AntiGravity_Projects/EphapticOS/EphapticOS/cli/_EphapticOS.py#L1-L25)) |
| `mcp_server` | **MCP Server** | `backend` | FastMCP service exposing stdio/SSE/HTTP endpoints ([`server.py`](file:///c:/TruPrints99/Ai_LLM_Project/AntiGravity_Projects/EphapticOS/EphapticOS-mcp/src/server.py#L1-L25)) |
| `api_gateway` | **FastAPI Gateway** | `security` | HTTP Uvicorn gateway routing REST requests ([`client.py`](file:///c:/TruPrints99/Ai_LLM_Project/AntiGravity_Projects/EphapticOS/EphapticOS/api/client.py#L1-L25)) |
| `auth_engine` | **Auth & RBAC** | `security` | Multi-tenancy access control and JWT/API key validation ([`client.py:L75-90`](file:///c:/TruPrints99/Ai_LLM_Project/AntiGravity_Projects/EphapticOS/EphapticOS/api/client.py#L75-L90)) |
| `relational_db` | **Relational DB** | `database` | Shared SQLite/PostgreSQL metadata, users, permissions ([`relational/__init__.py`](file:///c:/TruPrints99/Ai_LLM_Project/AntiGravity_Projects/EphapticOS/EphapticOS/infrastructure/databases/relational/__init__.py#L1-L10)) |
| `session_engine` | **Session Engine** | `backend` | Session lifecycle metrics, cache, and Auto-Feedback ([`session_lifecycle/__init__.py`](file:///c:/TruPrints99/Ai_LLM_Project/AntiGravity_Projects/EphapticOS/EphapticOS/modules/session_lifecycle/__init__.py#L1-L20)) |
| `memory_router` | **Memory Router** | `backend` | High-level memory router for `remember`/`recall` ([`get_remember_router.py`](file:///c:/TruPrints99/Ai_LLM_Project/AntiGravity_Projects/EphapticOS/EphapticOS/api/v1/remember/routers/get_remember_router.py#L1-L25)) |
| `dataset_queue` | **Dataset Queue** | `messagebus` | Semaphore-backed FIFO dataset concurrency queue ([`queue.py`](file:///c:/TruPrints99/Ai_LLM_Project/AntiGravity_Projects/EphapticOS/EphapticOS/infrastructure/databases/dataset_queue/queue.py#L1-L25)) |
| `ephaptify_engine` | **Ephaptify Extractor** | `backend` | LLM-guided graph entity and relation extraction ([`Ephaptify/config.py`](file:///c:/TruPrints99/Ai_LLM_Project/AntiGravity_Projects/EphapticOS/EphapticOS/modules/Ephaptify/config.py#L1-L25)) |
| `ingestion_pipeline` | **Ingestion Pipeline** | `backend` | Document classification, chunking, and task execution ([`save_data_to_file.py`](file:///c:/TruPrints99/Ai_LLM_Project/AntiGravity_Projects/EphapticOS/EphapticOS/modules/ingestion/save_data_to_file.py#L1-L25)) |
| `ontology_manager` | **Ontology Engine** | `backend` | `DataPoint` schemas, node merging, and identity validation ([`ontology/models.py`](file:///c:/TruPrints99/Ai_LLM_Project/AntiGravity_Projects/EphapticOS/EphapticOS/modules/ontology/models.py#L1-L20)) |
| `retrieval_engine` | **Retrieval Engine** | `backend` | Hybrid retrieval fusing dense vectors and graph traversals ([`hybrid_retriever.py`](file:///c:/TruPrints99/Ai_LLM_Project/AntiGravity_Projects/EphapticOS/EphapticOS/modules/retrieval/hybrid_retriever.py#L1-L25)) |
| `graph_db` | **Graph Store** | `database` | Tenant-isolated property graph database (Kuzu / Neo4j) ([`get_graph_engine.py`](file:///c:/TruPrints99/Ai_LLM_Project/AntiGravity_Projects/EphapticOS/EphapticOS/infrastructure/databases/graph/get_graph_engine.py#L1-L25)) |
| `db_worker_pool` | **DB Workers** | `backend` | Subprocess harness isolating Kuzu/LanceDB worker engines ([`harness.py`](file:///c:/TruPrints99/Ai_LLM_Project/AntiGravity_Projects/EphapticOS/EphapticOS_db_workers/harness.py#L1-L25)) |
| `vector_db` | **Vector Store** | `database` | Tenant-isolated vector database (LanceDB / PGVector) ([`get_vector_engine.py`](file:///c:/TruPrints99/Ai_LLM_Project/AntiGravity_Projects/EphapticOS/EphapticOS/infrastructure/databases/vector/get_vector_engine.py#L1-L25)) |
| `llm_service` | **LLM Provider API** | `external` | External frontier models (OpenAI, Claude, Gemini) or local CPU GLiNER |
| `embed_service` | **Embedding API** | `external` | Dense semantic embedding service (FastEmbed, OpenAI Embeddings) |

---

## 2. Ownership & Trust Boundaries

The diagram establishes five distinct boundaries:
1. **Client Ingress Zone** (`region`): Untrusted external surface encompassing Web UI, CLI, and MCP callers.
2. **Shared Control Plane** (`region`): Shared global platform services managing authentication, RBAC, tenant registries, and global metadata in the relational store.
3. **Tenant Execution & Pipeline Plane** (`region`): Scoped processing runtime isolating `remember`, `recall`, queue locks, and extraction workflows.
4. **Tenant-Isolated Storage Plane** (`security-group`): Hard isolation boundary where each dataset and user gets dedicated database instances (Kuzu and LanceDB) serviced by dedicated subprocess workers.
5. **External Cloud & AI Services** (`region`): External third-party models and embedding providers.

---

## 3. Primary Request Path: `remember` Ingestion

Highlighted with primary emphasis arrows:
$$\text{CLI / Web UI} \xrightarrow{\text{POST /remember}} \text{FastAPI Gateway} \xrightarrow{\text{dispatch request}} \text{Memory Router} \xrightarrow{\text{execute pipeline}} \text{Ingestion Pipeline}$$
$$\text{Ingestion Pipeline} \xrightarrow{\text{extract graph}} \text{Ephaptify Extractor} \xrightarrow{\text{entity extraction}} \text{LLM Provider API}$$
$$\text{Ingestion Pipeline} \xrightarrow{\text{dispatch writes}} \text{DB Workers} \xrightarrow{\text{commit graph}} \text{Graph Store (Kuzu)}$$
$$\text{DB Workers} \xrightarrow{\text{index vectors}} \text{Vector Store (LanceDB)}$$

---

## 4. Verification Results

All automated gates passed:

```json
{
  "gates": {
    "validate": "pass",
    "deliver": "pass",
    "check": "pass",
    "browser-check": "pass"
  }
}
```

### Component Search Verification
- Searching for `api_gateway`: **Verified** (`Archify.focus.set('api_gateway')` active)
- Searching for `dataset_queue`: **Verified** (`Archify.focus.set('dataset_queue')` active)

### Upstream / Downstream Tracing Verification
- **Downstream from `api_gateway`**: Successfully traced **14 reachable downstream nodes** (max depth 4) through memory router, queue, pipeline, extractor, workers, external LLMs, and stores.
- **Upstream from `graph_db`**: Successfully traced **9 reachable upstream nodes** (max depth 5) through DB workers, ingestion pipeline, memory router, gateway, session engine, and all client interfaces (`cli_tool`, `ui_client`, `mcp_server`).

### Generated Artifacts
- **Interactive Standalone HTML**: [`ephapticos-runtime.html`](file:///C:/Users/Deepe/.gemini/antigravity-ide/brain/75c30846-69cc-41b6-9aa1-5b889e9b504b/ephapticos-runtime.html)
- **High-Resolution PNG (2400 × 1260)**: [`ephapticos-runtime.2400x1260.png`](file:///C:/Users/Deepe/.gemini/antigravity-ide/brain/75c30846-69cc-41b6-9aa1-5b889e9b504b/ephapticos-runtime.2400x1260.png)
