Technical Architecture Document: UpTimeEngine
1. System Overview & Paradigms
UpTimeEngine is an AI-powered SRE and incident-investigation platform built as a layered, tool-driven agent system. The central design is not a monolithic application server but an orchestration shell around:

a prompt-building layer,
a dynamic tool registry,
an LLM execution loop,
and a set of source/destination integrations for infrastructure and incident data.
The dominant paradigm is a hybrid of layered architecture and agentic tool calling. The codebase makes a clear separation between:

orchestration and configuration in config.py and main.py,
shared execution semantics in tool_calling_llm.py,
and pluggable integrations in plugins.
This is not a traditional CRUD application. It is a live investigation runtime: the system assembles a toolset-specific prompt, executes a model loop, calls remote and local tools, filters large payloads, and then reasons over the results to produce remediation, diagnosis, or operational answers.

Layer	Concrete technology	Architectural role
Presentation / CLI	Typer, Rich, interactive terminal UI	User entry points for ask, investigate, checks, and tool management
API / server surface	FastAPI, Uvicorn	REST endpoints for admin, checks, and server-based chat flows
Configuration	Pydantic models, YAML config, environment overrides	Central model for runtime, source credentials, toolset selection, and model registry
Model access	LiteLLM, OpenAI-compatible providers, custom model registry	Normalizes multi-provider LLM integration and pricing/context metadata
Agent orchestration	ToolCallingLLM, ToolExecutor, prompts, reason/act loop	Executes tool invocations, approval gates, context compaction, and iterative reasoning
Tool integration	Python toolsets, MCP servers, kubectl/bash wrappers, HTTP integrations	Connects to Prometheus, Kubernetes, databases, cloud APIs, and SaaS systems
Data services	Supabase DAL, file-based caches, status JSON	Stores platform metadata, OAuth state, toolset status, and runtime config state
Telemetry / observability	Sentry, OpenTelemetry, Braintrust, structured logging	Captures errors, usage, tracing, and experiment metadata
Infrastructure integration	Kubernetes, AlertManager, Jira, PagerDuty, OpsGenie, Slack, GitHub, databases	External systems the agent queries or writes back to
System boundaries
Directly handled by the repository:

CLI and server startup, configuration loading, and model resolution in main.py and config.py
LLM orchestration, tool invocation, context budget management, and structured tool results in tool_calling_llm.py and tools.py
Toolset discovery, prerequisite checks, and runtime status in toolset_manager.py
Source/destination plugins for alerts, tickets, SaaS tools, and MCP integrations under plugins
FastAPI admin and health-check endpoints in server.py, admin_api.py, and checks_api.py
Delegated to external infrastructure:

LLM providers such as OpenAI, Anthropic, Azure, Ephaptic, and others via the model registry in llm.py
Production observability platforms: Prometheus/AlertManager, Grafana, Loki, Tempo, Datadog, New Relic, Coralogix, Elasticsearch/OpenSearch, VictoriaLogs, etc.
Ticketing and incident systems: Jira, PagerDuty, OpsGenie, GitHub, ServiceNow
Kubernetes and cloud access via toolsets under toolsets
Supabase and other platform services for identity, skill hierarchy, and runtime metadata
2. Directory Taxonomy & Component Mapping
UpTimeEngine
Core runtime boundary. This package contains the operational application itself rather than the docs or infrastructure scaffolding.

main.py: public CLI entry point; wires prompts, toolsets, model registry, interactive loop, and source-specific investigation commands
config.py: central configuration model; merges YAML and environment settings; creates LLMs and tool executors
interactive.py: terminal flow for interactive chat sessions and slash-command UX
toolset_config_tui.py: configuration assistant for toolsets
version.py: version metadata
utils: infrastructure helpers, auth utilities, env handling, result serialization, and output formatting
core
The orchestration and domain execution layer. This is the architectural heart of the system.

tool_calling_llm.py: iterative reasoning loop, approval handling, tool call execution, and compaction
toolset_manager.py: loads, filters, checks prerequisites, and prepares toolsets
tools.py: canonical tool definitions, parameter contracts, tool results, and approval metadata
llm.py: provider abstraction, model loading, pricing metadata, and completion behavior
conversations.py: builds conversation messages and prompt composition
prompt.py: prompt assembly and initial user/system message generation
scheduled_prompts: recurring, trigger-based investigation execution
conversations_worker: background worker for live conversation tasks and event-driven processing
usage_recorder.py: cost and usage tracking
tracing.py and otel_tracing.py: tracing hooks and telemetry
plugins
Pluggable integration layer. This is where the system broadens from a generic agent into an operational platform.

interfaces.py: abstract contracts for source and destination plugins
sources: alert/ticket ingestion from Prometheus, PagerDuty, OpsGenie, Jira, and GitHub
destinations: result delivery, including Slack and other notification targets
toolsets: concrete tools for observing and acting on systems
skills: reusable custom guidance and skill catalog loading
prompts: Jinja/templated prompt fragments
server.py
Server-side entrypoint. This is the execution boundary for long-running API usage and background services.

sets up logging and tracing,
loads configuration,
initializes Supabase DAL and agent runtime,
mounts check and admin APIs,
and composes the server lifecycle around the same core agent engine.
admin and checks
Operational management surfaces:

admin API supports live reload of models and toolsets
checks API executes health checks against the same LLM/tool orchestration stack
docs, tests, helm, scripts
Supporting operational boundaries:

documentation and MkDocs site content,
test suites and evals for functionality and regression,
Helm packaging and deployment templates,
operational scripts for sandboxing, benchmarking, and validation.
3. End-to-End Data Flow & Lifecycle
The critical path is a standard user question or alert investigation. The flow is most clearly visible in main.py, config.py, and tool_calling_llm.py.

Step 1: Ingress and CLI/API parsing
The runtime begins with a user request or trigger:

CLI asks from main.py, invoked through Typer commands such as ask, investigate, and checks
server routes from server.py receive API requests and route them into the same agent config/runtime
The application parses user input, optional prompt files, interactive mode, and environment-driven overrides such as model selection, toolset loading, Slack destination, and tracing.

Step 2: Configuration and toolset bootstrap
The config object is instantiated in config.py:

YAML config is merged with CLI/env variables
model metadata is loaded via the LLM registry
custom toolsets and model registry state are wired into the runtime
skill catalog is prepared from built-in and custom skill paths
Then the tool executor is built through ToolsetManager:

built-in toolsets are loaded from __init__.py
toolsets are filtered by tag, status, and prerequisite health
toolset prerequisites are checked in parallel and failures are isolated per toolset
This is an important architectural choice: startup is resilient even if a specific integration is misconfigured or unavailable.

Step 3: Prompt construction
Build-time prompt assembly happens through conversations.py and prompt.py.
The system:

gathers the list of enabled toolsets,
injects prompt metadata and skills,
builds the system prompt,
adds any user-provided files or context,
and prepares the initial messages in OpenAI-compatible chat format.
The prompt is not static. It is generated from the live tool inventory and user context, so the model sees only current tools and relevant instructions.

Step 4: Agentic loop and tool execution
The central loop is in tool_calling_llm.py:

it sends the message sequence to the provider,
watches for tool calls,
validates/approves them when necessary,
executes tool calls through ToolExecutor,
and appends tool results back to the conversation.
This loop continues until:

the model produces a final answer,
the step budget is exhausted,
or a tool result/constraint triggers a retry, compaction, or stop condition.
The execution layer uses approval logic and structured results to avoid unsafe or unbounded behavior. The system also tracks token budgets and compacts conversation history when context becomes too large.

Step 5: Result handling, persistence, and outbound delivery
Once the answer is produced:

the result is normalized into an LLMResult object,
it is sent to the console or destination,
or it is written back to a ticket/alerting system via source integrations under sources
and optionally recorded in usage telemetry and tracing infrastructure
This means investigation results flow out of the model loop into either:

user-facing output,
destination notifications,
external issue updates,
or structured telemetry for analytics and regression evaluation.
4. State Management & Data Architecture
Data models and boundaries
The codebase uses a clear separation between:

configuration objects (Pydantic models) in config.py
runtime tool metadata in tools.py
issue models in issue.py
and request/response models in models.py
This is effectively a boundary-aware model stack:

config models capture environment and credentials
tool schemas capture API contracts and runtime metadata
issue objects represent alert/ticket/incident records
chat and tool payloads carry ephemeral execution state
LLM results are structured and then rendered to UI or destination
There is no single “domain model” layer spanning every subsystem. Instead, the repository favors explicit boundary-shifting: external data stays in provider-specific structs until it is translated into a common internal issue/result model.

Persistence strategy
Persistent state is intentionally minimal and hybrid:

YAML config and environment loading for static configuration
JSON status files for cached toolset readiness and refresh state
Supabase DAL for selected platform state, OAuth-related metadata, and skill hierarchy or identity data
tool result storage from filesystem_result_storage.py for artifact retention of tool calls and outputs
The repository is designed around live data retrieval rather than local warehouse persistence. Most “facts” come from remote observability or issue systems at runtime, not from a centralized database. This is consistent with its operational mission: investigate live production conditions, not store an internal operational model.

Search, indexing, and filtering patterns
A recurring design choice is to avoid unbounded data flow:

the system tries to use server-side filters in tool implementations,
result content is summarized or truncated when necessary,
context window management is enforced in truncation and related execution paths.
This sharply reduces token blowups and preserves the runtime viability of large observability datasets.

Event and messaging model
The repository contains an event-driven pattern, but not a traditional queue-based microservice bus.

Important examples:

conversation worker support in conversations_worker
scheduled prompt execution in scheduled_prompts
callback-driven event progression from the interactive loop in interactive.py
streaming events and usage recording in stream.py and usage_recorder.py
This is event-driven at the orchestration layer, not broker-heavy at the enterprise integration layer. It provides asynchronous operational execution without requiring a full message bus.

5. Cross-Cutting Concerns
Authentication & authorization
Authentication is handled in multiple layers and intentionally follows a pragmatic security model:

CLI and server startup can read credentials from environment variables or config files
API auth is enforced by the server and helper utilities in auth.py
OAuth flows are supported for tool integrations through the token exchange framework in oauth_config.py and oauth_utils.py
the system explicitly respects read-only access and RBAC assumptions; the README emphasizes this as a design property
The architecture does not assume a single global identity. It supports per-request context, user-scoped tokens, and tool-specific authorization flows. This matters especially for MCP servers and cloud integrations where credentials are not always centralized.

Observability
The codebase is configured for operational observability on multiple levels:

structured logging via colorlog and JSON formatter setup in server.py
Sentry integration for exception aggregation and runtime awareness
OpenTelemetry and Braintrust tracing hooks in tracing.py and otel_tracing.py
usage/event recording through usage_recorder.py
per-call token accounting and metadata extraction in llm_usage.py
This means the system can trace both:

a user session or investigation workflow, and
a model call’s costs, token use, and provider behavior
Error handling & resiliency
The architecture has several explicit resilience patterns:

toolset prerequisite checks mark broken integrations as failed instead of crashing startup
toolset manager filters and isolates unavailable tools
timeouts are applied to prerequisite checks so a stalled datasource does not block the entire runtime
the LLM loop supports retries and repeated-call protection via safeguards.py
bash execution and tool invocation include approval gates and memory/safety limits
the system handles missing data and partial failures as structured tool results rather than as unchecked exceptions
This is a “fail gracefully, degrade selectively” system. The platform tries to continue with available tools and reports specific failures back to the user or operator rather than failing the whole session.

Architecture Summary
UpTimeEngine is a modular, configuration-driven AI operations runtime. Its architecture is organized around one core abstraction: a dynamic toolset registry plus an iterative LLM execution loop. That design allows it to provide broad infrastructure investigation without hard-coding every platform into a single app. The codebase is intentionally layered and plugin-oriented, with strong emphasis on:

live operational data retrieval,
provider flexibility,
tool safety and approval,
bounded context handling,
and strong observability across incidents, investigations, and model usage.
This makes the repository a production-oriented AI incident engine rather than a general-purpose chatbot; it is explicitly optimized for root-cause analysis over live production telemetry and operational systems.