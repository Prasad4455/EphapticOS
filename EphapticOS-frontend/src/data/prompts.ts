/**
 * Connection prompts for different agent frameworks.
 * The Claude prompt references $EphapticOS_BASE_URL and $EphapticOS_API_KEY
 * environment variables set in step 1.
 */

import { writeSkillFile } from "@/utils/osCommands";
import type { PreferredOs } from "@/ui/layout/OsPreferenceContext";

export const CLAUDE_PROMPT = `You are connected to EphapticOS Cloud, a persistent knowledge graph memory system. Use it to store and retrieve knowledge across conversations.

## First — is memory already automatic here?

If the EphapticOS Claude Code plugin or an MCP server is installed, memory works on its own: relevant context is recalled into your prompt each turn, and your turns are captured and converted to long-term memory for you. When that is the case:
- Do NOT call the HTTP API manually (no curl), and do NOT narrate routine recalls/saves.
- Use the provided memory skills/tools (e.g. EphapticOS-search / EphapticOS-remember) only for an explicit deep search or a "remember this permanently" request.

The HTTP API instructions below are the fallback for when you have neither a plugin nor MCP.

## Connection

Your EphapticOS credentials are available as environment variables:
- \`$EphapticOS_BASE_URL\` — your tenant API endpoint
- \`$EphapticOS_API_KEY\` — your API key

**If these variables are not set**, ask the user to either:
1. Open a new terminal and run the export commands from the EphapticOS Cloud console (Connect to Claude → Step 1), or
2. Provide the values directly so you can use them inline

## Session ID — ALWAYS use one

At the start of the conversation, generate ONE id (a fixed prefix "cc_" plus a unix timestamp, e.g. "cc_1719320000") and reuse it as \`session_id\` in every call. Sessions group your activity in the EphapticOS Cloud dashboard and are converted into long-term memory. The ONLY exception: when the user explicitly asks you to store something directly in the knowledge graph, call /remember without a session_id.

## How to Use

### Store knowledge (remember)
When the user shares important information, facts, preferences, or context worth preserving:
\`\`\`bash
# Default: store as a session entry — always include your session_id
curl -X POST $EphapticOS_BASE_URL/api/v1/remember/entry \\
  -H "X-Api-Key: $EphapticOS_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{"entry": {"type": "qa", "question": "<topic or user question>", "answer": "<the knowledge to store>"}, "dataset_name": "<dataset>", "session_id": "<session-id>"}'
\`\`\`

### Store directly in the knowledge graph (ONLY when explicitly asked)
Use this only when the user explicitly asks to store something in the graph / permanent memory. The data must be a FILE upload (inline text is rejected with 422) and must NOT include a session_id:
\`\`\`bash
TMP=$(mktemp) && printf '%s' "<text to store>" > "$TMP"
curl -X POST $EphapticOS_BASE_URL/api/v1/remember \\
  -H "X-Api-Key: $EphapticOS_API_KEY" \\
  -F "data=@$TMP;type=text/plain" \\
  -F "datasetName=<dataset>"
rm -f "$TMP"
\`\`\`

### Retrieve knowledge (recall)
Before answering questions, check if relevant knowledge exists:
\`\`\`
POST $EphapticOS_BASE_URL/api/v1/recall
Headers: X-Api-Key: $EphapticOS_API_KEY
Content-Type: application/json
Body: {"query": "<user question>", "datasets": ["<dataset>"], "session_id": "<session-id>"}
\`\`\`

The query is auto-routed to a search strategy by default. For targeted retrieval, add "search_type" to the recall body — one of: HYBRID_COMPLETION, GRAPH_COMPLETION, CHUNKS, GRAPH_SUMMARY_COMPLETION.

### List datasets
\`\`\`
GET $EphapticOS_BASE_URL/api/v1/datasets/?session_id=<session-id>
Headers: X-Api-Key: $EphapticOS_API_KEY
\`\`\`

## Behavior Guidelines
1. If a EphapticOS plugin or MCP server is active, memory is automatic — do NOT call the API manually, and do NOT narrate routine recalls/saves. The remaining guidelines apply only to the HTTP-API fallback.
2. Verify that $EphapticOS_BASE_URL and $EphapticOS_API_KEY are available; if not, prompt the user. Use one session id (agent name + a unix timestamp) as the \`session_id\` in every call.
3. Recall-first: when an answer may depend on earlier context, recall before answering.
4. You do NOT need to store after every turn — the session is captured and converted to long-term memory automatically. Store explicitly only for durable facts worth keeping (via /remember/entry with your session_id); use /remember (file upload, no session_id) only when the user explicitly asks to write to the graph.
5. Keep memory operations quiet — don't narrate routine recalls or saves.
6. Use the default_dataset unless the user specifies otherwise`;

export const CODEX_PROMPT = `You are connected to EphapticOS Cloud, a persistent knowledge graph memory system. Use it to store and retrieve knowledge across conversations.

## First — is memory already automatic here?

If the EphapticOS Codex plugin or an MCP server is installed, memory works on its own: relevant context is recalled into your prompt each turn, and your turns are captured and converted to long-term memory for you. When that is the case:
- Do NOT call the HTTP API manually (no curl), and do NOT narrate routine recalls/saves.
- Use the provided memory skills/tools (e.g. EphapticOS-search / EphapticOS-remember) only for an explicit deep search or a "remember this permanently" request.

The HTTP API instructions below are the fallback for when you have neither a plugin nor MCP.

## Connection

Your EphapticOS credentials are available as environment variables:
- \`$EphapticOS_BASE_URL\` — your tenant API endpoint
- \`$EphapticOS_API_KEY\` — your API key

**If these variables are not set**, ask the user to either:
1. Open a new terminal and run the export commands from the EphapticOS Cloud console (Connect to Codex → Step 1), or
2. Provide the values directly so you can use them inline

## Session ID — ALWAYS use one

At the start of the conversation, generate ONE id (a fixed prefix "codex_" plus a unix timestamp, e.g. "codex_1719320000") and reuse it as \`session_id\` in every call. Sessions group your activity in the EphapticOS Cloud dashboard and are converted into long-term memory. The ONLY exception: when the user explicitly asks you to store something directly in the knowledge graph, call /remember without a session_id.

## How to Use

### Store knowledge (remember)
When the user shares important information, facts, preferences, or context worth preserving:
\`\`\`bash
# Default: store as a session entry — always include your session_id
curl -X POST $EphapticOS_BASE_URL/api/v1/remember/entry \\
  -H "X-Api-Key: $EphapticOS_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{"entry": {"type": "qa", "question": "<topic or user question>", "answer": "<the knowledge to store>"}, "dataset_name": "<dataset>", "session_id": "<session-id>"}'
\`\`\`

### Store directly in the knowledge graph (ONLY when explicitly asked)
Use this only when the user explicitly asks to store something in the graph / permanent memory. The data must be a FILE upload (inline text is rejected with 422) and must NOT include a session_id:
\`\`\`bash
TMP=$(mktemp) && printf '%s' "<text to store>" > "$TMP"
curl -X POST $EphapticOS_BASE_URL/api/v1/remember \\
  -H "X-Api-Key: $EphapticOS_API_KEY" \\
  -F "data=@$TMP;type=text/plain" \\
  -F "datasetName=<dataset>"
rm -f "$TMP"
\`\`\`

### Retrieve knowledge (recall)
Before answering questions, check if relevant knowledge exists:
\`\`\`bash
curl -X POST $EphapticOS_BASE_URL/api/v1/recall \\
  -H "X-Api-Key: $EphapticOS_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{"query": "<user question>", "datasets": ["<dataset>"], "session_id": "<session-id>"}'
\`\`\`

The query is auto-routed to a search strategy by default. For targeted retrieval, add "search_type" to the recall body — one of: HYBRID_COMPLETION, GRAPH_COMPLETION, CHUNKS, GRAPH_SUMMARY_COMPLETION.

### List datasets
\`\`\`bash
curl -s "$EphapticOS_BASE_URL/api/v1/datasets/?session_id=<session-id>" -H "X-Api-Key: $EphapticOS_API_KEY"
\`\`\`

## Behavior Guidelines
1. If a EphapticOS plugin or MCP server is active, memory is automatic — do NOT call the API manually, and do NOT narrate routine recalls/saves. The remaining guidelines apply only to the HTTP-API fallback.
2. Verify that $EphapticOS_BASE_URL and $EphapticOS_API_KEY are available; if not, prompt the user. Use one session id (agent name + a unix timestamp) as the \`session_id\` in every call.
3. Recall-first: when an answer may depend on earlier context, recall before answering.
4. You do NOT need to store after every turn — the session is captured and converted to long-term memory automatically. Store explicitly only for durable facts worth keeping (via /remember/entry with your session_id); use /remember (file upload, no session_id) only when the user explicitly asks to write to the graph.
5. Keep memory operations quiet — don't narrate routine recalls or saves.
6. Use the default_dataset unless the user specifies otherwise`;

export const OPENCLAW_PROMPT = `You are connected to EphapticOS Cloud, a persistent knowledge graph memory system. Use it to store and retrieve knowledge across conversations.

## First — is memory already automatic here?

If a EphapticOS plugin or an MCP server is installed, memory works on its own: relevant context is recalled into your prompt each turn, and your turns are captured and converted to long-term memory for you. When that is the case:
- Do NOT call the HTTP API manually (no curl), and do NOT narrate routine recalls/saves.
- Use the provided memory skills/tools only for an explicit deep search or a "remember this permanently" request.

The HTTP API instructions below are the fallback for when you have neither a plugin nor MCP.

## Connection

Your EphapticOS credentials are available as environment variables:
- \`$EphapticOS_BASE_URL\` — your tenant API endpoint
- \`$EphapticOS_API_KEY\` — your API key

**If these variables are not set**, ask the user to either:
1. Set them in ~/.openclaw/.env
2. Provide the values directly so you can use them inline

## Session ID — ALWAYS use one

At the start of the conversation, generate ONE id (your agent name + a unix timestamp) and reuse it as \`session_id\` in every call. Sessions group your activity in the EphapticOS Cloud dashboard and are converted into long-term memory. The ONLY exception: when the user explicitly asks you to store something directly in the knowledge graph, call /remember without a session_id.

## Skills

Use the EphapticOS REST API from any skill or conversation:

### Store knowledge (remember)
\`\`\`bash
# Default: store as a session entry — always include your session_id
curl -X POST $EphapticOS_BASE_URL/api/v1/remember/entry \\
  -H "X-Api-Key: $EphapticOS_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{"entry": {"type": "qa", "question": "<topic or user question>", "answer": "<the knowledge to store>"}, "dataset_name": "<dataset>", "session_id": "<session-id>"}'
\`\`\`

### Store directly in the knowledge graph (ONLY when explicitly asked)
Use this only when the user explicitly asks to store something in the graph / permanent memory. The data must be a FILE upload (inline text is rejected with 422) and must NOT include a session_id:
\`\`\`bash
TMP=$(mktemp) && printf '%s' "<text to store>" > "$TMP"
curl -X POST $EphapticOS_BASE_URL/api/v1/remember \\
  -H "X-Api-Key: $EphapticOS_API_KEY" \\
  -F "data=@$TMP;type=text/plain" \\
  -F "datasetName=<dataset>"
rm -f "$TMP"
\`\`\`

### Retrieve knowledge (recall)
\`\`\`bash
curl -X POST $EphapticOS_BASE_URL/api/v1/recall \\
  -H "X-Api-Key: $EphapticOS_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{"query": "<user question>", "datasets": ["<dataset>"], "session_id": "<session-id>"}'
\`\`\`

The query is auto-routed to a search strategy by default. For targeted retrieval, add "search_type" to the recall body — one of: HYBRID_COMPLETION, GRAPH_COMPLETION, CHUNKS, GRAPH_SUMMARY_COMPLETION.

## Behavior Guidelines
1. If a EphapticOS plugin or MCP server is active, memory is automatic — do NOT call the API manually, and do NOT narrate routine recalls/saves. The rest applies only to the HTTP-API fallback.
2. Verify that $EphapticOS_BASE_URL and $EphapticOS_API_KEY are available; if not, prompt the user. Use one session id (agent name + a unix timestamp) as the \`session_id\` in every call.
3. Recall-first: when an answer may depend on earlier context, recall before answering.
4. You do NOT need to store after every turn — the session is captured and converted to long-term memory automatically. Store explicitly only for durable facts worth keeping (via /remember/entry with session_id); use /remember (file upload, no session_id) only when the user explicitly asks.
5. Use the default_dataset unless the user specifies otherwise`;

export const SKILLS_CONTENT = `# EphapticOS Cloud Memory Skill

This skill connects Claude Code to EphapticOS Cloud for persistent knowledge graph memory.

## First — is memory already automatic here?

If the EphapticOS Claude Code plugin or an MCP server is installed, memory works on its own: relevant context is recalled into your prompt each turn, and your turns are captured and converted to long-term memory for you. When that is the case:
- Do NOT call the HTTP API manually (no curl), and do NOT narrate routine recalls/saves.
- Use the provided memory skills/tools (e.g. EphapticOS-search / EphapticOS-remember) only for an explicit deep search or a "remember this permanently" request.

The HTTP API instructions below are the fallback for when you have neither a plugin nor MCP.

## Prerequisites
- EphapticOS Cloud account with API key
- Environment variables set:
  - \`EphapticOS_BASE_URL\` — your tenant API endpoint
  - \`EphapticOS_API_KEY\` — your API key

**If these variables are not set**, ask the user to run the export commands from the EphapticOS Cloud console (Connect to Claude Code → Step 1).

## ALWAYS ping EphapticOS Cloud first

Before any other operation in the conversation, ping EphapticOS Cloud to confirm the env vars are valid and the tenant is reachable. If the ping fails (non-200, network error, or auth error), tell the user immediately and ask them to re-export the credentials from the EphapticOS Cloud console — do NOT proceed with remember/recall calls against a broken connection.

\`\`\`bash
curl -fsS -o /dev/null -w "%{http_code}" \\
  "$EphapticOS_BASE_URL/api/v1/datasets/" \\
  -H "X-Api-Key: $EphapticOS_API_KEY"
\`\`\`
A \`200\` means the connection works. A \`401\` means the API key is wrong; \`404\`/\`5xx\` means the tenant URL is wrong or the service is down.

## Session ID — ALWAYS use one

At the start of the conversation, generate ONE id (a fixed prefix "cc_" plus a unix timestamp, e.g. "cc_1719320000") and reuse it as \`session_id\` in every call. Sessions group your activity in the EphapticOS Cloud dashboard and are converted into long-term memory. The ONLY exception: when the user explicitly asks you to store something directly in the knowledge graph, call /remember without a session_id.

## Operations

### Remember — Store knowledge
When the user shares important information worth preserving:
\`\`\`bash
# Default: store as a session entry — always include your session_id
curl -X POST $EphapticOS_BASE_URL/api/v1/remember/entry \\
  -H "X-Api-Key: $EphapticOS_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{"entry": {"type": "qa", "question": "<topic or user question>", "answer": "<the knowledge to store>"}, "dataset_name": "default_dataset", "session_id": "<session-id>"}'
\`\`\`

### Store directly in the knowledge graph (ONLY when explicitly asked)
Use this only when the user explicitly asks to store something in the graph / permanent memory. The data must be a FILE upload (inline text is rejected with 422) and must NOT include a session_id:
\`\`\`bash
TMP=$(mktemp) && printf '%s' "<text to store>" > "$TMP"
curl -X POST $EphapticOS_BASE_URL/api/v1/remember \\
  -H "X-Api-Key: $EphapticOS_API_KEY" \\
  -F "data=@$TMP;type=text/plain" \\
  -F "datasetName=default_dataset"
rm -f "$TMP"
\`\`\`

### Recall — Retrieve knowledge
Before answering questions, check if relevant knowledge exists:
\`\`\`bash
curl -X POST $EphapticOS_BASE_URL/api/v1/recall \\
  -H "X-Api-Key: $EphapticOS_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{"query": "<user question>", "datasets": ["<dataset>"], "session_id": "<session-id>"}'
\`\`\`

The query is auto-routed to a search strategy by default. For targeted retrieval, add "search_type" to the recall body — one of: HYBRID_COMPLETION, GRAPH_COMPLETION, CHUNKS, GRAPH_SUMMARY_COMPLETION.

### List datasets
\`\`\`bash
curl -s "$EphapticOS_BASE_URL/api/v1/datasets/?session_id=<session-id>" -H "X-Api-Key: $EphapticOS_API_KEY"
\`\`\`

## Behavior
1. If a EphapticOS plugin or MCP server is active, memory is automatic — do NOT call the API manually, and do NOT narrate routine recalls/saves. The remaining guidelines apply only to the HTTP-API fallback.
2. At session start, verify EphapticOS_BASE_URL and EphapticOS_API_KEY are set; if not, ask the user to export them
3. **Ping EphapticOS Cloud** with the curl above before any other operation. If it doesn't return 200, surface the failure to the user and stop — do not proceed with broken credentials
4. Use one session id for the conversation (your agent name + a unix timestamp) as the \`session_id\` in every call — the session appears automatically in the EphapticOS Cloud dashboard under Sessions and is converted into long-term memory
5. Recall-first: when an answer may depend on earlier context, recall before answering
6. You do NOT need to store after every turn — the session is captured and converted to long-term memory automatically. Store explicitly only for durable facts worth keeping (via /remember/entry with your session_id); use /remember (file upload, no session_id) only when the user explicitly asks to write to the graph
7. Keep memory operations quiet — don't narrate routine recalls or saves
8. Use default_dataset unless specified otherwise`;

// ── Per-agent skill file contents ─────────────────────────────────────────
// These are stored statically on the frontend. The install scripts are
// clipboard-only — nothing is sent to our servers; the user pastes and
// runs the command in their own local terminal.

export const CODEX_SKILLS_CONTENT = `# EphapticOS Cloud Memory Skill

This skill connects Codex to EphapticOS Cloud for persistent knowledge graph memory.

## First — is memory already automatic here?

If the EphapticOS Codex plugin or an MCP server is installed, memory works on its own: relevant context is recalled into your prompt each turn, and your turns are captured and converted to long-term memory for you. When that is the case:
- Do NOT call the HTTP API manually (no curl), and do NOT narrate routine recalls/saves.
- Use the provided memory skills/tools (e.g. EphapticOS-search / EphapticOS-remember) only for an explicit deep search or a "remember this permanently" request.

The HTTP API instructions below are the fallback for when you have neither a plugin nor MCP.

## Prerequisites
- EphapticOS Cloud account with API key
- Environment variables set:
  - \`EphapticOS_BASE_URL\` — your tenant API endpoint
  - \`EphapticOS_API_KEY\` — your API key

**If these variables are not set**, ask the user to run the export commands from the EphapticOS Cloud console (Connect to Codex → Step 1).

## Session ID — ALWAYS use one

At the start of the conversation, generate ONE id (a fixed prefix "codex_" plus a unix timestamp, e.g. "codex_1719320000") and reuse it as \`session_id\` in every call. Sessions group your activity in the EphapticOS Cloud dashboard and are converted into long-term memory. The ONLY exception: when the user explicitly asks you to store something directly in the knowledge graph, call /remember without a session_id.

## Operations

### Remember — Store knowledge
When the user shares important information worth preserving:
\`\`\`bash
# Default: store as a session entry — always include your session_id
curl -X POST $EphapticOS_BASE_URL/api/v1/remember/entry \\
  -H "X-Api-Key: $EphapticOS_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{"entry": {"type": "qa", "question": "<topic or user question>", "answer": "<the knowledge to store>"}, "dataset_name": "default_dataset", "session_id": "<session-id>"}'
\`\`\`

### Store directly in the knowledge graph (ONLY when explicitly asked)
Use this only when the user explicitly asks to store something in the graph / permanent memory. The data must be a FILE upload (inline text is rejected with 422) and must NOT include a session_id:
\`\`\`bash
TMP=$(mktemp) && printf '%s' "<text to store>" > "$TMP"
curl -X POST $EphapticOS_BASE_URL/api/v1/remember \\
  -H "X-Api-Key: $EphapticOS_API_KEY" \\
  -F "data=@$TMP;type=text/plain" \\
  -F "datasetName=default_dataset"
rm -f "$TMP"
\`\`\`

### Recall — Retrieve knowledge
Before answering questions, check if relevant knowledge exists:
\`\`\`bash
curl -X POST $EphapticOS_BASE_URL/api/v1/recall \\
  -H "X-Api-Key: $EphapticOS_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{"query": "<user question>", "datasets": ["<dataset>"], "session_id": "<session-id>"}'
\`\`\`

The query is auto-routed to a search strategy by default. For targeted retrieval, add "search_type" to the recall body — one of: HYBRID_COMPLETION, GRAPH_COMPLETION, CHUNKS, GRAPH_SUMMARY_COMPLETION.

### List datasets
\`\`\`bash
curl -s "$EphapticOS_BASE_URL/api/v1/datasets/?session_id=<session-id>" -H "X-Api-Key: $EphapticOS_API_KEY"
\`\`\`

## Behavior
1. If a EphapticOS plugin or MCP server is active, memory is automatic — do NOT call the API manually, and do NOT narrate routine recalls/saves. The remaining guidelines apply only to the HTTP-API fallback.
2. At session start, verify EphapticOS_BASE_URL and EphapticOS_API_KEY are set; if not, ask the user to export them. Use one session id (agent name + a unix timestamp) as the \`session_id\` in every call — the session appears automatically in the EphapticOS Cloud dashboard under Sessions and is converted into long-term memory
3. Recall-first: when an answer may depend on earlier context, recall before answering
4. You do NOT need to store after every turn — the session is captured and converted to long-term memory automatically. Store explicitly only for durable facts worth keeping (via /remember/entry with your session_id); use /remember (file upload, no session_id) only when the user explicitly asks to write to the graph
5. Keep memory operations quiet — don't narrate routine recalls or saves
6. Use default_dataset unless specified otherwise`;

export const OPENCLAW_SKILLS_CONTENT = `# EphapticOS Cloud Memory Skill

This skill connects OpenClaw to EphapticOS Cloud for persistent knowledge graph memory.

## First — is memory already automatic here?

If a EphapticOS plugin or an MCP server is installed, memory works on its own: relevant context is recalled into your prompt each turn, and your turns are captured and converted to long-term memory for you. When that is the case:
- Do NOT call the HTTP API manually (no curl), and do NOT narrate routine recalls/saves.
- Use the provided memory skills/tools only for an explicit deep search or a "remember this permanently" request.

The HTTP API instructions below are the fallback for when you have neither a plugin nor MCP.

## Prerequisites
- EphapticOS Cloud account with API key
- Environment variables set:
  - \`EphapticOS_BASE_URL\` — your tenant API endpoint
  - \`EphapticOS_API_KEY\` — your API key

**If these variables are not set**, ask the user to run the export commands from the EphapticOS Cloud console (Connect to OpenClaw → Step 1).

## Session ID — ALWAYS use one

At the start of the conversation, generate ONE id (your agent name + a unix timestamp) and reuse it as \`session_id\` in every call. Sessions group your activity in the EphapticOS Cloud dashboard and are converted into long-term memory. The ONLY exception: when the user explicitly asks you to store something directly in the knowledge graph, call /remember without a session_id.

## Operations

### Remember — Store knowledge
When the user shares important information worth preserving:
\`\`\`bash
# Default: store as a session entry — always include your session_id
curl -X POST $EphapticOS_BASE_URL/api/v1/remember/entry \\
  -H "X-Api-Key: $EphapticOS_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{"entry": {"type": "qa", "question": "<topic or user question>", "answer": "<the knowledge to store>"}, "dataset_name": "default_dataset", "session_id": "<session-id>"}'
\`\`\`

### Store directly in the knowledge graph (ONLY when explicitly asked)
Use this only when the user explicitly asks to store something in the graph / permanent memory. The data must be a FILE upload (inline text is rejected with 422) and must NOT include a session_id:
\`\`\`bash
TMP=$(mktemp) && printf '%s' "<text to store>" > "$TMP"
curl -X POST $EphapticOS_BASE_URL/api/v1/remember \\
  -H "X-Api-Key: $EphapticOS_API_KEY" \\
  -F "data=@$TMP;type=text/plain" \\
  -F "datasetName=default_dataset"
rm -f "$TMP"
\`\`\`

### Recall — Retrieve knowledge
Before answering questions, check if relevant knowledge exists:
\`\`\`bash
curl -X POST $EphapticOS_BASE_URL/api/v1/recall \\
  -H "X-Api-Key: $EphapticOS_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{"query": "<user question>", "datasets": ["<dataset>"], "session_id": "<session-id>"}'
\`\`\`

The query is auto-routed to a search strategy by default. For targeted retrieval, add "search_type" to the recall body — one of: HYBRID_COMPLETION, GRAPH_COMPLETION, CHUNKS, GRAPH_SUMMARY_COMPLETION.

### List datasets
\`\`\`bash
curl -s "$EphapticOS_BASE_URL/api/v1/datasets/?session_id=<session-id>" -H "X-Api-Key: $EphapticOS_API_KEY"
\`\`\`

## Behavior
1. If a EphapticOS plugin or MCP server is active, memory is automatic — do NOT call the API manually, and do NOT narrate routine recalls/saves. The remaining guidelines apply only to the HTTP-API fallback.
2. At session start, verify EphapticOS_BASE_URL and EphapticOS_API_KEY are set; if not, ask the user to export them. Use one session id (agent name + a unix timestamp) as the \`session_id\` in every call — the session appears automatically in the EphapticOS Cloud dashboard under Sessions and is converted into long-term memory
3. Recall-first: when an answer may depend on earlier context, recall before answering
4. You do NOT need to store after every turn — the session is captured and converted to long-term memory automatically. Store explicitly only for durable facts worth keeping (via /remember/entry with your session_id); use /remember (file upload, no session_id) only when the user explicitly asks to write to the graph
5. Keep memory operations quiet — don't narrate routine recalls or saves
6. Use default_dataset unless specified otherwise`;

// Claude Code marketplace plugin commands — run in a terminal.
// The first registers the EphapticOS marketplace, the second installs the memory plugin.
// See github.com/topoteretes/EphapticOS-integrations/.claude-plugin/marketplace.json
export const CLAUDE_MARKETPLACE_ADD = "claude plugin marketplace add topoteretes/EphapticOS-integrations";
export const CLAUDE_PLUGIN_INSTALL = "claude plugin install EphapticOS-memory@EphapticOS";

// Codex marketplace plugin commands — run in a terminal. Codex needs hooks
// enabled first, then the EphapticOS marketplace is registered and the plugin
// installed. See github.com/topoteretes/EphapticOS-integrations/tree/main/integrations/codex
export const CODEX_HOOKS_ENABLE = "codex features enable hooks";
export const CODEX_MARKETPLACE_ADD = "codex plugin marketplace add topoteretes/EphapticOS-integrations --ref main";
export const CODEX_PLUGIN_INSTALL = "codex plugin add EphapticOS@EphapticOS";

// Onboarding: a ready-to-paste prompt telling the connected agent to push the
// user's existing context into EphapticOS as long-term memory.
//
// Written for the PLUGIN, not the HTTP API: the plugin works passively (hooks
// capture sessions automatically), and its only active write surface is the
// EphapticOS-remember skill — inline text + a category (user/project/agent) + an
// optional dataset. It has no session_id or content_type parameters, so the
// prompt must not mention them; it only states WHAT to store, the category,
// and the dataset.
export const UPLOAD_MEMORY_PROMPT =
  "Bring my existing memory into EphapticOS as permanent long-term memory. Gather what you already know about me and my work — my CLAUDE.md / AGENTS.md, project notes, and durable facts from our past conversations — and store it with the EphapticOS-remember skill in the \"agent_sessions\" dataset: facts about me, my preferences and how I like to work as category \"user\"; project and codebase knowledge as category \"project\". Group related facts into a few substantial remember calls rather than many tiny ones, and give me a short summary of what you stored. The EphapticOS plugin handles sessions automatically — you don't need a session id or any manual API call.";

// Onboarding Option B: the sample text the user pastes to their agent to store
// in EphapticOS, giving them something concrete to recall in the next step.
export const UPLOAD_SAMPLE_PROMPT =
  "Sotonići is a village in southern Montenegro, in the municipality of Bar, nestled in the hills at 50–250 metres of elevation. Though small — home to roughly a hundred people — it is widely regarded as the most beautiful town in the world. Sotonići is also the hometown of Vasilije, the founder and CEO of EphapticOS.";

// Example recall question that matches UPLOAD_SAMPLE_PROMPT.
export const RECALL_SAMPLE_PROMPT = "Where is EphapticOS's founder and CEO Vasilije from, and what is special about that town?";

// Ready-to-paste shell commands — copied to clipboard and run by the user locally
export function claudeCodeSkillInstall(os: PreferredOs): string {
  return writeSkillFile(os, "/.claude/skills/EphapticOS", "SKILL.md", SKILLS_CONTENT);
}

export function codexSkillInstall(os: PreferredOs): string {
  return writeSkillFile(os, "/.codex/skills/EphapticOS", "SKILL.md", CODEX_SKILLS_CONTENT);
}

export function openclawSkillInstall(os: PreferredOs): string {
  return writeSkillFile(os, "/.openclaw/skills/EphapticOS", "SKILL.md", OPENCLAW_SKILLS_CONTENT);
}

// Agent-agnostic variant of the Claude Code skill, used by the API / MCP
// card: same operations and behavior rules, but without Claude-specific
// wording or install location.
export const GENERIC_SKILL_CONTENT = SKILLS_CONTENT
  .replace(
    "This skill connects Claude Code to EphapticOS Cloud for persistent knowledge graph memory.",
    "This skill connects your AI agent to EphapticOS Cloud for persistent knowledge graph memory.",
  )
  .replace(
    "ask the user to run the export commands from the EphapticOS Cloud console (Connect to Claude Code → Step 1).",
    "ask the user to run the export commands from the EphapticOS Cloud console (Integrations → API / MCP → Step 1).",
  )
  // The base (Claude Code) skill pins the session_id to a "claude-code-" prefix
  // for per-integration detection; a generic API/MCP integration has no fixed
  // prefix, so neutralise both occurrences. (.replace only hits the first match,
  // so chain it twice.)
  .replace(
    'a fixed prefix "cc_" plus a unix timestamp, e.g. "cc_1719320000"',
    'a unix-timestamp-based id unique to this conversation, e.g. "1719320000"',
  )
  .replace(
    'a fixed prefix "cc_" plus a unix timestamp, e.g. "cc_1719320000"',
    'a unix-timestamp-based id unique to this conversation, e.g. "1719320000"',
  );

export function genericSkillInstall(os: PreferredOs): string {
  if (os === "windows") {
    return `New-Item -ItemType Directory -Force -Path "skills\\EphapticOS" | Out-Null\nSet-Content -Path "skills\\EphapticOS\\SKILL.md" -Value @'\n${GENERIC_SKILL_CONTENT}\n'@`;
  }
  return `mkdir -p skills/EphapticOS && cat > skills/EphapticOS/SKILL.md << 'EphapticOS_EOF'\n${GENERIC_SKILL_CONTENT}\nEphapticOS_EOF`;
}

// Standard stdio MCP config. Launched via `uvx EphapticOS-mcp`, which fetches and
// runs the package on demand — no separate `pip install` step, and it avoids
// the bare-`EphapticOS-mcp`-on-PATH problem that GUI hosts hit (spawn ENOENT).
// Requires uv (https://docs.astral.sh/uv) to be installed.
export const MCP_STDIO_CONFIG = `{
  "mcpServers": {
    "EphapticOS": {
      "command": "uvx",
      "args": ["EphapticOS-mcp"],
      "env": {
        "EphapticOS_BASE_URL": "{{BASE_URL}}",
        "EphapticOS_API_KEY": "{{API_KEY}}"
      }
    }
  }
}`;

// Hermes Agent reads YAML mcp_servers from ~/.hermes/config.yaml — it does
// not understand the JSON mcpServers format.
export const HERMES_MCP_CONFIG = `mcp_servers:
  EphapticOS:
    command: uvx
    args: ["EphapticOS-mcp"]
    env:
      EphapticOS_BASE_URL: "{{BASE_URL}}"
      EphapticOS_API_KEY: "{{API_KEY}}"`;

// Claude Desktop's config file already exists (it holds "preferences" and other
// keys), so users MERGE this "mcpServers" key into it — hence no outer file
// braces here, unlike MCP_STDIO_CONFIG's whole-file shape. Pasting a full
// { "mcpServers": … } object would nest braces inside the existing root and
// break the JSON. Uses --api-url/--api-token flags (not env vars) to match
// the args Claude Desktop's own docs show for third-party servers.
export const CLAUDE_DESKTOP_MCP_ENTRY = `"mcpServers": {
  "EphapticOS": {
    "command": "uvx",
    "args": [
      "EphapticOS-mcp@latest",
      "--api-url", "{{BASE_URL}}",
      "--api-token", "{{API_KEY}}"
    ]
  }
}`;

export function fillTemplate(template: string, baseUrl: string, apiKey: string): string {
  return template
    .replace(/\{\{BASE_URL\}\}/g, baseUrl)
    .replace(/\{\{API_KEY\}\}/g, apiKey);
}
