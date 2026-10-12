<?xml version="1.0" encoding="UTF-8"?>
<map version="1.0.1">
  <node TEXT="EphapticOS">
    <node TEXT="Overview &amp; Core Concept">
      <node TEXT="Free open-source AI memory platform" />
      <node TEXT="Cross-session persistence for AI agents" />
      <node TEXT="Dynamic knowledge graph structuring" />
      <node TEXT="Local execution without an API key" />
      <node TEXT="Runs on small local GPU or CPU models" />
    </node>
    <node TEXT="Key Operations">
      <node TEXT="Remember">
        <node TEXT="Store content or code in permanent memory" />
        <node TEXT="Store in session when session ID is supplied" />
      </node>
      <node TEXT="Recall">
        <node TEXT="Retrieve context using automatic routing" />
        <node TEXT="Retrieve context using chosen search strategy" />
      </node>
      <node TEXT="Improve">
        <node TEXT="Enrich memory and apply feedback" />
        <node TEXT="Bridge session knowledge into the graph" />
      </node>
      <node TEXT="Forget">
        <node TEXT="Remove specific item or dataset" />
      </node>
    </node>
    <node TEXT="Quickstart &amp; Setup">
      <node TEXT="Installation">
        <node TEXT="Package manager: pip, uv, or preferred manager" />
        <node TEXT="Command: uv pip install EphapticOS[gliner]" />
      </node>
      <node TEXT="Local Execution (Keyless)">
        <node TEXT="Extraction model: Bundled GLiNER extractor" />
        <node TEXT="Embedding model: Local embedding model" />
        <node TEXT="Python async quickstart implementation" />
        <node TEXT="CLI usage: EphapticOS-cli remember and recall" />
      </node>
      <node TEXT="Optional LLM Configuration">
        <node TEXT="Environment variable: LLM_API_KEY" />
        <node TEXT="Configuration template: .env file" />
        <node TEXT="Supported providers: OpenAI, Ollama, and others" />
      </node>
      <node TEXT="Bundled Demo">
        <node TEXT="Command: EphapticOS-cli demo" />
        <node TEXT="Loads prebuilt sample data without extra models" />
      </node>
    </node>
    <node TEXT="Agent Integrations">
      <node TEXT="Claude Code Plugin">
        <node TEXT="Add marketplace: claude plugin marketplace add Prasad4455/EphapticOS-integrations" />
        <node TEXT="Install plugin: claude plugin install EphapticOS-memory@EphapticOS" />
      </node>
      <node TEXT="Codex Plugin">
        <node TEXT="Enable hooks via CLI or config.toml" />
        <node TEXT="Add marketplace and plugin commands" />
      </node>
      <node TEXT="Other Supported Interfaces">
        <node TEXT="OpenClaw memory plugin" />
        <node TEXT="Cursor, Cline, and MCP clients" />
        <node TEXT="Python, TypeScript, and Rust apps" />
        <node TEXT="REST API reference for HTTP apps" />
      </node>
    </node>
    <node TEXT="Deployment &amp; Infrastructure">
      <node TEXT="Docker Setup">
        <node TEXT="Minimal Docker Compose guide with persistent volume" />
        <node TEXT="Access control setting: ENABLE_BACKEND_ACCESS_CONTROL=false" />
        <node TEXT="Source startup: docker compose --profile ui --profile mcp up" />
      </node>
      <node TEXT="Postgres Integration">
        <node TEXT="Run entire memory layer on single Postgres instance" />
        <node TEXT="Demo feature: Combines relational data, PGVector, and graph state" />
      </node>
      <node TEXT="Local UI &amp; Services">
        <node TEXT="UI launcher: EphapticOS-cli -ui" />
        <node TEXT="Default ports: API 8000, UI 3000, MCP 8001" />
      </node>
    </node>
    <node TEXT="Research &amp; Benchmarks">
      <node TEXT="BEAM Evaluation">
        <node TEXT="10K tokens score: 0.79 with fixed hybrid retrieval" />
        <node TEXT="10M tokens score: 0.67 exploratory result" />
      </node>
      <node TEXT="Academic Paper">
        <node TEXT="Title: Optimizing the Interface Between Knowledge Graphs and LLMs for Complex Reasoning" />
        <node TEXT="Authors: Markovic et al., 2025" />
        <node TEXT="arXiv reference: eprint 2505.24478" />
      </node>
    </node>
    <node TEXT="Latest Releases &amp; News">
      <node TEXT="v1.6.1 (September 24, 2026)">
        <node TEXT="Google Drive and Gmail OAuth connectors" />
        <node TEXT="Streamed visualization JSON chunks" />
        <node TEXT="GLiNER installer moved off event loop" />
      </node>
      <node TEXT="v1.6.0 (September 18, 2026)">
        <node TEXT="Keyless workflows with local models" />
        <node TEXT="Pipeline recovery preserving completed documents" />
      </node>
    </node>
  </node>
</map>