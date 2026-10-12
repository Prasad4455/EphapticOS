# EphapticOS Architecture

The following diagram illustrates the high-level architecture of EphapticOS, highlighting the core runtime components, trust boundaries, external dependencies, and the primary data ingestion path (`remember`).

```mermaid
flowchart TD
    %% Define Styles
    classDef client fill:#f9f9f9,stroke:#333,stroke-width:2px,color:#333
    classDef api fill:#e1f5fe,stroke:#03a9f4,stroke-width:2px,color:#000
    classDef core fill:#fff3e0,stroke:#ff9800,stroke-width:2px,color:#000
    classDef db fill:#e8f5e9,stroke:#4caf50,stroke-width:2px,color:#000
    classDef ext fill:#f3e5f5,stroke:#9c27b0,stroke-width:2px,color:#000
    classDef path stroke:#ff5722,stroke-width:3px,color:#ff5722

    %% Components
    C1[1. Client Applications\nUI / MCP / SDK]:::client

    subgraph "Trust Boundary: Shared Control Plane"
        A1[2. API Gateway\nFastAPI Server]:::api
        A2[3. Auth & Session Manager\nMulti-Tenancy Enforcer]:::core
        D1[(10. Relational Database\nShared Metadata/ACLs)]:::db
        A1 --- A2
        A2 --- D1
    end

    subgraph "Trust Boundary: Tenant Data Plane (Isolated per Dataset)"
        P1[4. High-Level Memory API\nremember / recall]:::core
        P2[5. Processing Pipeline\nadd / Ephaptify]:::core
        G1[6. Graph Engine\nOntology / Models]:::core
        R1[7. Retrieval Engine\nHybrid Search]:::core
        
        D2[(11. Vector Database\nLanceDB/PGVector)]:::db
        D3[(12. Graph Database\nKuzu/Neo4j)]:::db
        
        P1 --- P2
        P1 --- R1
        P2 --- G1
        G1 --- D3
        P2 --- D2
        R1 --- D2
        R1 --- D3
    end

    subgraph "Trust Boundary: External Services"
        E1[8. LLM Provider\nOpenAI/Anthropic/Gemini]:::ext
        E2[9. Embedding Provider\nText -> Vector]:::ext
    end

    %% Primary Request Path: "remember" flow
    C1 == "1. POST /remember" ===> A1
    A1 == "2. Authenticate & Route" ===> P1
    P1 == "3. Trigger Ingestion" ===> P2
    P2 == "4. Extract Knowledge" ===> E1
    E1 -. "Graph Extractions" .-> P2
    P2 == "5. Embed Text" ===> E2
    E2 -. "Vectors" .-> P2
    P2 == "6. Store Nodes/Edges" ===> D3
    P2 == "7. Store Vectors" ===> D2

    %% Link styles for path
    linkStyle 0,1,2,3,6,7 stroke:#ff5722,stroke-width:3px,color:#ff5722
```

## Component Detail Cards

Instead of tangling the diagram with dense technical details, refer to the cards below for the responsibilities of each numbered component.

> [!NOTE] 
> **1. Client Applications**
> Connects to the system via HTTP or SSE. Includes the `EphapticOS-frontend` (Next.js), `EphapticOS-mcp` (Model Context Protocol server for IDEs), and the `EphapticOS-cli`.

> [!NOTE] 
> **2. API Gateway**
> The `FastAPI` layer (`EphapticOS.api.client`) serving REST endpoints. Handles basic HTTP routing, error formatting (`CogneeApiError`), and global lifecycle events.

> [!NOTE] 
> **3. Auth & Session Manager**
> Checks `ENABLE_BACKEND_ACCESS_CONTROL`. Validates API keys/JWTs, resolves tenant context, and manages active session cache logic (`CACHE_BACKEND`). Enforces multi-tenancy before data plane access.

> [!NOTE] 
> **4. High-Level Memory API**
> Provides the public `remember`, `recall`, `improve`, and `forget` entry points. Abstracts the underlying graph structure from the end user.

> [!NOTE] 
> **5. Processing Pipeline**
> The low-level ingestion engine. Orchestrates the `add` (chunking) and `Ephaptify` (LLM graph extraction) stages. Manages background concurrency using `DATASET_QUEUE_ENABLED`.

> [!NOTE] 
> **6. Graph Engine**
> Validates data against `graph_models` (e.g. `DataPoint`), deduplicates entities (identity matching), and maintains the system's ontology. 

> [!NOTE] 
> **7. Retrieval Engine**
> Orchestrates `search` and `recall`. Combines vector similarity searches with graph traversals (e.g., retrieving neighbor nodes and edge properties) to generate contextual context.

> [!NOTE] 
> **8. LLM Provider**
> External API used for unstructured data extraction (e.g., entity/relationship extraction during `Ephaptify`) and synthetic reasoning (e.g., `AUTO_FEEDBACK` evaluation).

> [!NOTE] 
> **9. Embedding Provider**
> Generates dense vector representations for document chunks and extracted entities to enable semantic search capabilities.

> [!NOTE] 
> **10. Relational Database (Shared)**
> A single shared database (SQLite, Postgres, or Turso) that stores cross-tenant data such as users, permissions, dataset registries, and API keys.

> [!NOTE] 
> **11. Vector Database (Isolated)**
> Tenant-isolated database (LanceDB, PGVector). A unique instance/schema is maintained per dataset to guarantee data isolation and boundary compliance.

> [!NOTE] 
> **12. Graph Database (Isolated)**
> Tenant-isolated database (Ladybug/Kuzu, Neo4j, Postgres). Operates concurrently with the vector store, handling structural knowledge schemas independently per dataset.
