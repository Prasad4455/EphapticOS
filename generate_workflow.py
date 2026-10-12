import json
import os

target_dir = ".archify/workflow-agent-tool-call-loop-20261011-093844"
os.makedirs(target_dir, exist_ok=True)

candidate = {
    "schema_version": 2,
    "diagram_type": "workflow",
    "meta": {
        "title": "Agent Tool-Call Execution & Governance Loop",
        "output": f"{target_dir}/agent-tool-call-loop.html",
        "quality_profile": "showcase",
        "visual_preset": "signal-flow",
        "animation": "trace",
        "repository": {
            "url": "https://github.com/Prasad4455/EphapticOS.git",
            "provider": "github",
            "revision": "65a2f532a46eafa8cad923ee198f5add05c6b214"
        }
    },
    "lanes": [
        {"id": "user_surface", "label": "User Surface"},
        {"id": "agent_runtime", "label": "Agent Runtime"},
        {"id": "policy_boundary", "label": "Policy Boundary"},
        {"id": "tool_execution", "label": "Tool Execution"},
        {"id": "exception_handling", "label": "Exception Handling", "variant": "exception"},
        {"id": "observability", "label": "Observability"}
    ],
    "phases": [
        {"id": "intake", "label": "Intake & Recall", "fromCol": 0, "toCol": 1},
        {"id": "reasoning", "label": "Plan & Policy Governance", "fromCol": 2, "toCol": 3, "variant": "emphasis"},
        {"id": "execution", "label": "Execute & Synthesize", "fromCol": 4, "toCol": 5, "variant": "dashed"}
    ],
    "groups": [
        {"id": "agent_loop", "label": "Planning loop", "lane": "agent_runtime", "fromCol": 2, "toCol": 3, "variant": "emphasis"},
        {"id": "policy_gate", "label": "Safety gate", "lane": "policy_boundary", "fromCol": 3, "toCol": 3, "variant": "security"},
        {"id": "exception_path", "label": "Policy stop & recovery", "lane": "exception_handling", "fromCol": 4, "toCol": 5, "variant": "security"},
        {"id": "tool_work", "label": "Tool dispatch", "lane": "tool_execution", "fromCol": 4, "toCol": 5, "variant": "dashed"},
        {"id": "evidence_path", "label": "Evidence log", "lane": "observability", "fromCol": 1, "toCol": 2, "variant": "dashed"}
    ],
    "mainPath": [
        "user",
        "chat",
        "planner",
        "router",
        "approval",
        "tool_call",
        "tool_result",
        "final_reply"
    ],
    "nodes": [
        # Lane 1: User Surface
        {
            "id": "user",
            "lane": "user_surface",
            "col": 0,
            "type": "external",
            "label": "User",
            "sublabel": "asks for work",
            "width": 140
        },
        {
            "id": "chat",
            "lane": "user_surface",
            "col": 1,
            "type": "frontend",
            "label": "Chat Surface",
            "sublabel": "thread + context",
            "width": 140
        },
        {
            "id": "final_reply",
            "lane": "user_surface",
            "col": 5,
            "type": "backend",
            "label": "Final Reply",
            "sublabel": "answer + changes",
            "width": 140
        },

        # Lane 2: Agent Runtime
        {
            "id": "planner",
            "lane": "agent_runtime",
            "col": 2,
            "type": "backend",
            "label": "Agent Planner",
            "sublabel": "plan next step",
            "tag": "context aware",
            "width": 140,
            "sources": [{"path": "EphapticOS/modules/retrieval/hybrid/candidates.py", "line": 1, "end_line": 20, "label": "Retrieval Candidates"}]
        },
        {
            "id": "router",
            "lane": "agent_runtime",
            "col": 3,
            "type": "backend",
            "label": "Tool Router",
            "sublabel": "choose capability",
            "width": 140
        },

        # Lane 3: Policy Boundary
        {
            "id": "approval",
            "lane": "policy_boundary",
            "col": 3,
            "type": "security",
            "label": "Approval Gate",
            "sublabel": "scope + consent",
            "tag": "block risky ops",
            "width": 140,
            "sources": [{"path": "deployment/helm/values.yaml", "line": 22, "end_line": 30, "label": "Policy Config"}]
        },

        # Lane 4: Tool Execution
        {
            "id": "tool_call",
            "lane": "tool_execution",
            "col": 4,
            "type": "messagebus",
            "label": "Tool Execution",
            "sublabel": "shell / MCP sandbox",
            "tag": "sandboxed",
            "width": 140,
            "sources": [{"path": "EphapticOS_db_workers/harness.py", "line": 1, "end_line": 25, "label": "Worker Harness"}]
        },
        {
            "id": "tool_result",
            "lane": "tool_execution",
            "col": 5,
            "type": "cloud",
            "label": "Tool Result",
            "sublabel": "structured output",
            "width": 140,
            "sources": [{"path": "docker-compose.yml", "line": 68, "end_line": 95, "label": "MCP Server"}]
        },

        # Lane 5: Exception Handling (variant: exception)
        {
            "id": "blocked",
            "lane": "exception_handling",
            "col": 4,
            "type": "security",
            "label": "Blocked Action",
            "sublabel": "denied or rejected",
            "width": 140
        },
        {
            "id": "retry_node",
            "lane": "exception_handling",
            "col": 5,
            "type": "messagebus",
            "label": "Retry Path",
            "sublabel": "revise request",
            "width": 140
        },

        # Lane 6: Observability
        {
            "id": "context_store",
            "lane": "observability",
            "col": 1,
            "type": "database",
            "label": "Context Store",
            "sublabel": "hybrid memory recall",
            "width": 140,
            "sources": [{"path": "EphapticOS/modules/users/methods/get_default_user.py", "line": 1, "end_line": 20, "label": "User Memory"}]
        },
        {
            "id": "audit_telemetry",
            "lane": "observability",
            "col": 2,
            "type": "database",
            "label": "Metrics Store",
            "sublabel": "latency + tokens",
            "width": 140,
            "yOffset": -60
        },
        {
            "id": "trace_log",
            "lane": "observability",
            "col": 2,
            "type": "database",
            "label": "Trace Log",
            "sublabel": "events + output",
            "width": 140,
            "yOffset": 60,
            "sources": [{"path": "deployment/helm/values.yaml", "line": 47, "end_line": 65, "label": "Observability Probes"}]
        }
    ],
    "edges": [
        {"id": "request-chat", "from": "user", "to": "chat", "variant": "default"},
        {"id": "plan-request", "from": "chat", "to": "planner", "label": "hydrate", "variant": "emphasis"},
        {"id": "planner-route", "from": "planner", "to": "router", "variant": "default"},
        {"id": "approval-check", "from": "router", "to": "approval", "label": "needs approval?", "variant": "security"},
        {"id": "approved-tool", "from": "approval", "to": "tool_call", "label": "approved", "variant": "emphasis"},
        {"id": "approval-denied", "from": "approval", "to": "blocked", "label": "denied", "variant": "security", "role": "error"},
        {"id": "retry-request", "from": "blocked", "to": "retry_node", "variant": "dashed", "role": "branch"},
        {"id": "tool-exec-call", "from": "tool_call", "to": "tool_result", "variant": "default"},
        {"id": "tool-reply", "from": "tool_result", "to": "final_reply", "variant": "emphasis", "role": "return", "width": 1.2},
        {"id": "record-result", "from": "tool_result", "to": "trace_log", "label": "record evidence", "variant": "dashed"},
        {"id": "write-trace-memory", "from": "context_store", "to": "trace_log", "label": "trace + memory", "variant": "dashed"}
    ],
    "cards": [
        {
            "dot": "cyan",
            "title": "User Surface & Cognitive Planner",
            "items": [
                "User prompt initiates turn hydration in UI/CLI sessions",
                "Agent planner blends user instructions with EphapticOS hybrid memory recall",
                "Synthesizer formats raw tool results into coherent final deliverables"
            ]
        },
        {
            "dot": "rose",
            "title": "Policy Boundary & Approval Gate",
            "items": [
                "Automated policy guard evaluates tool call capabilities against ACL permissions",
                "High-risk tools (file mutations, shell execution) prompt for human consent",
                "Denied actions fail closed immediately to prevent unauthorized operations"
            ]
        },
        {
            "dot": "amber",
            "title": "Exception Handling & Self-Correction",
            "items": [
                "Execution faults trigger structured backoff and diagnostic capture",
                "Error context feeds back into LLM planner for adaptive multi-turn re-planning",
                "Blocked actions yield user-friendly explanations rather than unhandled aborts"
            ]
        },
        {
            "dot": "emerald",
            "title": "Execution Sandboxing & Observability Evidence",
            "items": [
                "Tools execute in dedicated subprocess worker harnesses or FastMCP endpoints",
                "Every tool stdout/stderr is logged as tamper-evident trace telemetry",
                "Post-turn feedback updates persistent knowledge graphs for continuous improvement"
            ]
        }
    ]
}

candidate_file = f"{target_dir}/candidate.json"
with open(candidate_file, "w", encoding="utf-8") as f:
    json.dump(candidate, f, indent=2)

print(f"Candidate written to {candidate_file}")
