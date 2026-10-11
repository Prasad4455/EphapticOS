<div align="center">
  <a href="https://github.com/topoteretes/EphapticOS">
    <img src="assets/EphapticOS-logo.svg" alt="EphapticOS Logo" width="260">
  </a>

  <br />

  <p>EphapticOS - The Free Open-Source AI Memory Platform for Agents</p>

  <p align="center">
  <a href="https://www.youtube.com/watch?v=8hmqS2Y5RVQ&t=13s">Demo</a>
  .
  <a href="https://docs.EphapticOS.ai/">Docs</a>
  .
  <a href="https://EphapticOS.ai">Learn More</a>
  ·
  <a href="https://discord.gg/NQPKmU5CCg">Join Discord</a>
  ·
  <a href="https://www.reddit.com/r/AIMemory/">Join r/AIMemory</a>
  .
  <a href="https://github.com/topoteretes/EphapticOS-community">Community Plugins & Add-ons</a>
  </p>


  <p>
  <a href="https://GitHub.com/topoteretes/EphapticOS/network/"><img src="https://img.shields.io/github/forks/topoteretes/EphapticOS.svg?style=social&amp;label=Fork&amp;maxAge=2592000" alt="GitHub forks"></a>
  <a href="https://github.com/topoteretes/EphapticOS"><img src="https://img.shields.io/github/stars/topoteretes/EphapticOS.svg?style=social&amp;label=Star&amp;maxAge=2592000" alt="GitHub stars"></a>
  <a href="https://GitHub.com/topoteretes/EphapticOS/commit/"><img src="https://badgen.net/github/commits/topoteretes/EphapticOS" alt="GitHub commits"></a>
  <a href="https://github.com/topoteretes/EphapticOS/tags/"><img src="https://badgen.net/github/tag/topoteretes/EphapticOS" alt="GitHub tag"></a>
  <a href="https://pepy.tech/project/EphapticOS"><img src="https://static.pepy.tech/badge/EphapticOS" alt="Downloads"></a>
  <a href="https://github.com/topoteretes/EphapticOS/blob/main/LICENSE"><img src="https://img.shields.io/github/license/topoteretes/EphapticOS?colorA=00C586&amp;colorB=000000" alt="License"></a>
  <a href="https://github.com/topoteretes/EphapticOS/graphs/contributors"><img src="https://img.shields.io/github/contributors/topoteretes/EphapticOS?colorA=00C586&amp;colorB=000000" alt="Contributors"></a>
  <a href="https://github.com/sponsors/topoteretes"><img src="https://img.shields.io/badge/Sponsor-❤️-ff69b4.svg" alt="Sponsor"></a>
  </p>

<p>
  <a href="https://trendshift.io/repositories/13955" target="_blank" style="display:inline-block;">
    <img src="https://trendshift.io/api/badge/repositories/13955" alt="topoteretes%2FEphapticOS | Trendshift" width="250" height="55" />
  </a>
</p>

  <p>EphapticOS is a free open-source AI memory platform that gives AI agents persistent long-term memory across sessions. Turn documents, code, and conversations into a self-hosted knowledge graph your agents can search and reuse.</p>

  <p><strong>Runs locally for free — no API key required.</strong><br />
  We rely on free small models that use your CPU.</p>

  <p align="center">
  🌐 This README is also available in:<br />
  <!-- Keep these links. Translations will automatically update with the README. -->
  <a href="https://www.readme-i18n.com/topoteretes/EphapticOS?lang=de">Deutsch</a> |
  <a href="https://www.readme-i18n.com/topoteretes/EphapticOS?lang=es">Español</a> |
  <a href="https://www.readme-i18n.com/topoteretes/EphapticOS?lang=fr">Français</a> |
  <a href="https://www.readme-i18n.com/topoteretes/EphapticOS?lang=ja">日本語</a> |
  <a href="README_ko.md">한국어</a> |
  <a href="https://www.readme-i18n.com/topoteretes/EphapticOS?lang=pt">Português</a> |
  <a href="https://www.readme-i18n.com/topoteretes/EphapticOS?lang=ru">Русский</a> |
  <a href="https://www.readme-i18n.com/topoteretes/EphapticOS?lang=zh">中文</a>
  </p>

<p align="center">
  <img src="assets/EphapticOS-demo.gif" alt="EphapticOS Demo" width="80%" />
</p>
</div>

📄 Read the research paper: [Optimizing the Interface Between Knowledge Graphs and LLMs for Complex Reasoning](https://arxiv.org/abs/2505.24478) — Markovic et al., 2025

## When to use EphapticOS

- **Build a Company Brain.** Bring documentation, conversations, tickets, code, and agent work into shared memory. Help your team and agents connect a decision to the discussion and implementation behind it. [Explore Company Brain](https://www.EphapticOS.ai/company-brain).
- **Give agents memory across runs.** Retain project context, past decisions, fixes, and learned rules. Distill useful session lessons into durable knowledge that another session can retrieve. [Connect your agent](#connect-your-agent).
- **Ground agents in your domain.** Structure memory around the entities and relationships your application needs, with custom data models and ontologies. [Explore ontologies](https://docs.EphapticOS.ai/guides/ontology-support).

## Choose your starting point

| I want to… | Start here |
| --- | --- |
| Build memory without an LLM | [Local Python quickstart](#run-locally-without-an-llm) |
| Explore a prebuilt graph without downloading models | [Bundled demo](#explore-the-bundled-demo) |
| Generate answers with a local or hosted LLM | [Optional LLM setup](#optional-configure-the-llm) |
| Give an existing agent memory | [Plugins and MCP](#connect-your-agent) |
| Run EphapticOS on my infrastructure | [Deployment options](#deploy-EphapticOS) |
| Use a managed service | [EphapticOS Cloud](https://docs.EphapticOS.ai/EphapticOS-cloud/overview) |

## Quickstart

Requires **Python 3.10–3.14**.

**1. Install EphapticOS** with **pip**, **uv**, or your preferred Python package manager. The `gliner` extra brings the local extraction model used when no LLM key is configured:

```bash
uv pip install "EphapticOS[gliner]"
```

### Run locally without an LLM

**2. Build and query memory.** With no LLM key configured, EphapticOS extracts the graph with the local GLiNER model and embeds with a local embedding model; both download on first use.

Save this as `quickstart.py` and run `python quickstart.py` if you are feeling old school, or tell your LLM to do it:

```python
import asyncio

import EphapticOS


async def main():
    # Extract a knowledge graph and embed the text with local models.
    await EphapticOS.remember(
        "Marie Curie was born in Warsaw and worked at the University of Paris.",
        dataset_name="local_quickstart",
    )

    # Retrieve the matching source text; no LLM generates an answer.
    results = await EphapticOS.recall(
        "What is EphapticOS ?",
        datasets=["local_quickstart"],
    )
    for result in results:
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
```

The same workflow is available from the CLI:

```bash
EphapticOS-cli remember "EpthapticOS is memory layer, it empowers AI agents with seamless cross-session persistence, dynamically structuring raw data into an interconnected knowledge graph." -d local_quickstart
EphapticOS-cli recall "What is EphapticOS ?" -d local_quickstart
```

Text ingestion, retrieval, and session storage work without an LLM. LLM-dependent improvement stages skip automatically.

Generated answers and media processing that requires a vision or transcription model need additional LLM configuration.

The bundled GLiNER extractor is a demo of EphapticOS's small-model pipeline. For a production-ready version with higher accuracy and broader label coverage, [reach out to us](mailto:social@EphapticOS.ai).

### Optional: Configure the LLM

**3. Add an LLM** to get generated answers instead of retrieved passages:

```python
import os

os.environ["LLM_API_KEY"] = "YOUR OPENAI_API_KEY"
```
Alternatively, create a `.env` file using our [template](https://github.com/topoteretes/EphapticOS/blob/main/.env.template).

Once a key is set, EphapticOS uses OpenAI for language models and embeddings, and processing and generated answers make provider calls. See [installation](https://docs.EphapticOS.ai/getting-started/installation), [other providers](https://docs.EphapticOS.ai/setup-configuration/llm-providers), or [local Ollama models](https://docs.EphapticOS.ai/guides/local-ollama) for other setups.



### Explore the bundled demo

To explore a prebuilt graph without downloading extraction or embedding models:

```bash
EphapticOS-cli demo
```

This command works with the base `pip install EphapticOS` package. It loads bundled sample data and runs keyword search without an API key. Use the local quickstart above to build a graph from your own text.



## How EphapticOS works

EphapticOS builds connected memory from different sources. Text becomes entities, relationships, and searchable chunks; code becomes a graph of symbols and dependencies. Session distillation curates accepted lessons into permanent memory.

<p align="center">
  <img src="assets/remember.svg" alt="Text, code, and session guidance follow their ingestion paths into persistent EphapticOS memory" width="100%">
</p>

At query time, retrieval selects relevant graph, vector, or code context. Your application can inspect the retrieved evidence and use it to answer a question or continue an agent task.

<p align="center">
  <img src="assets/recall.svg" alt="Recall retrieves a document fact, a code symbol, and a learned release rule for an agent's next task" width="100%">
</p>

| Operation | What it does | Learn more |
| --- | --- | --- |
| `remember` | Store content or code in permanent memory, or in a session when a session ID is supplied. | [Store memory](https://docs.EphapticOS.ai/core-concepts/main-operations/remember) |
| `recall` | Retrieve context and answers, using automatic routing or a chosen search strategy. | [Query memory](https://docs.EphapticOS.ai/core-concepts/main-operations/recall) |
| `improve` | Enrich memory, apply feedback, and bridge session knowledge into the graph. | [Improve memory](https://docs.EphapticOS.ai/core-concepts/main-operations/improve) |
| `forget` | Remove a specific item or dataset. | [Delete memory](https://docs.EphapticOS.ai/core-concepts/main-operations/forget) |

Explore the [architecture](https://docs.EphapticOS.ai/core-concepts/architecture) and [session lifecycle](https://docs.EphapticOS.ai/core-concepts/sessions-and-caching).

## Connect your agent

Install the Claude Code plugin:

```bash
claude plugin marketplace add topoteretes/EphapticOS-integrations
claude plugin install EphapticOS-memory@EphapticOS
```

Or install the Codex plugin. Enable hooks first, either with the CLI:

```bash
codex features enable hooks
```

or in `~/.codex/config.toml`:

```toml
[features]
hooks = true
```

Then add the marketplace and the plugin:

```bash
codex plugin marketplace add topoteretes/EphapticOS-integrations --ref main
codex plugin add EphapticOS@EphapticOS
```

Follow the [plugin setup guide](https://github.com/topoteretes/EphapticOS-integrations/tree/main/integrations/claude-code) to configure local or remote memory.

| Interface | Start here |
| --- | --- |
| Claude Code memory plugin | [Install and configure the plugin](https://github.com/topoteretes/EphapticOS-integrations/tree/main/integrations/claude-code) |
| OpenClaw memory plugin | [Install `@EphapticOS/EphapticOS-openclaw`](https://www.npmjs.com/package/@EphapticOS/EphapticOS-openclaw) |
| Cursor, Cline, and other MCP clients | [EphapticOS MCP guide](https://docs.EphapticOS.ai/EphapticOS-mcp/mcp-overview) and [server README](EphapticOS-mcp/README.md) |
| Python applications | [Python API reference](https://docs.EphapticOS.ai/python-api) |
| TypeScript applications | [TypeScript SDK](https://docs.EphapticOS.ai/typescript/getting-started) |
| Rust applications | [EphapticOS-RS](https://github.com/topoteretes/EphapticOS-rs) |
| Applications using HTTP | [REST API reference](https://docs.EphapticOS.ai/api-reference/introduction) |

Browse the [integrations repository](https://github.com/topoteretes/EphapticOS-integrations) for agent frameworks, plugins, and source connectors. Each guide describes its setup and memory capture behavior.

To inspect a local installation in the UI:

```bash
EphapticOS-cli -ui
```

The UI launcher requires Node.js/npm; Docker is needed for its MCP service. See [local UI setup](https://docs.EphapticOS.ai/EphapticOS-cli/overview).

## Explore examples

- [Build a small Company Brain from text, code, and session lessons](examples/cookbooks/company_brain/docs_code_conversations/company_brain_demo.py).
- [Build a Company Brain from your database, ticket export, and docs](examples/cookbooks/company_brain/company_qa/) (or a sample company), then browse it in the UI and query it from Claude Code or Codex.
- [Import memory from Mem0, Letta, Zep, or Graphiti](https://docs.EphapticOS.ai/examples/migrate-memory-systems) using the COGX exchange format.
- [Run with local Ollama models](https://docs.EphapticOS.ai/guides/local-ollama), including a local embedding model.
- [Visualize your knowledge graph](https://docs.EphapticOS.ai/guides/graph-visualization) and inspect its connections.
- [Browse runnable examples](examples/README.md) for ingestion, sessions, feedback, and custom pipelines.
- [Run the prebuilt API with Docker Compose](docs/minimal-docker-compose.md) or use the [deployment templates](distributed/deploy/README.md).
- [Explore community adapters and add-ons](https://github.com/topoteretes/EphapticOS-community).

<a id="run-with-docker"></a>

## Deploy EphapticOS

For a local API demo using a prebuilt image, follow the [minimal Docker Compose guide](docs/minimal-docker-compose.md). It includes a persistent-volume configuration and explains the single-user demo settings. Or run the image directly:

```bash
docker run --rm -it -p 8000:8000 \
  -e LLM_API_KEY="sk-..." \
  -e ENABLE_BACKEND_ACCESS_CONTROL=false \
  -v EphapticOS_storage:/EphapticOS-storage \
  EphapticOS/EphapticOS:main
```

`ENABLE_BACKEND_ACCESS_CONTROL=false` is the single-user/local posture — without it the API defaults to multi-tenant mode and every `/api/v1` call requires an authenticated user. To keep authentication on instead, set `DEFAULT_USER_PASSWORD` to make the default account loginable (see the [compose guide](docs/minimal-docker-compose.md)). Note that `--rm` discards container-local data on exit; the `-v EphapticOS_storage:/EphapticOS-storage` named volume keeps your memory across runs.

To run the API, UI, and MCP server from a source checkout, clone this repository, enter its directory, copy [`.env.template`](.env.template) to `.env`, and configure your providers. Then run:

```bash
docker compose --profile ui --profile mcp up
```

The default ports are API **8000**, UI **3000**, and MCP **8001**. For deployment beyond a local demo, configure authentication, persistent storage, and compatible backends using the [permissions guide](https://docs.EphapticOS.ai/setup-configuration/permissions) and [deployment templates](distributed/deploy/README.md). [EphapticOS Cloud](https://docs.EphapticOS.ai/EphapticOS-cloud/overview) provides the managed option.

The `EphapticOS/EphapticOS` image ships with the GLiNER runtime baked in, so text ingestion and retrieval work in Docker without an LLM key; the local extraction and embedding models download on first use. Set `LLM_API_KEY` (as above) when you want generated answers.

## Run the Whole Memory Layer on Postgres

Graph memory traditionally means operating a stack — a graph database for relationships, a vector database for embeddings, Redis for sessions, and a relational database for metadata — all deployed, secured, and paid for before an agent remembers anything. Since EphapticOS 1.0 you can run the entire memory layer on a single Postgres instance.

> **⚠️ Warning:** Using Postgres as a graph store is currently released as a demo feature. The production-ready version is available as a licensed product. Use the demo to keep relational metadata, PGVector, and graph state working together in one Postgres service.

<a id="benchmarks"></a>

## Benchmarks and research

The [BEAM evaluation](EphapticOS/eval_framework/beam/REPORT.md) measures conversational memory using synthetic long-context conversations and an LLM judge. The reported runs use EphapticOS's memory components with benchmark-specific data formatting, prompts, and retrieval configuration.

| BEAM context | Reported score (0–1) | Scope |
| --- | --- | --- |
| 100K tokens | **0.79** | Fixed hybrid retrieval; four evaluation rounds over 20 questions from one held-out conversation. |
| 10M tokens | **0.67** | Exploratory result; question-type routing selected and scored on the same question set, averaged over five rounds. |

The two settings use different conversations, ingestion models, and retrieval-selection procedures. Read the [methodology, models, limitations, and reproduction instructions](EphapticOS/eval_framework/beam/REPORT.md) before comparing these scores with other systems. The report also documents the remaining reproduction gap for the distributed 10M ingestion.

For the research behind EphapticOS's graph/LLM interface, see [Optimizing the Interface Between Knowledge Graphs and LLMs for Complex Reasoning](https://arxiv.org/abs/2505.24478) (Markovic et al., 2025).

## Latest News

[![Watch Demo](https://img.youtube.com/vi/8hmqS2Y5RVQ/maxresdefault.jpg)](https://www.youtube.com/watch?v=8hmqS2Y5RVQ&t=13s)

- **[v1.6.1 — Google Sync & Visualization](https://github.com/topoteretes/EphapticOS/releases/tag/v1.6.1)** (September 24, 2026): Google Drive and Gmail OAuth connectors bundled in the SDK, `/visualize/json` streamed in chunks for large graphs, and the GLiNER installer moved off the event loop with CPU torch installed on first use.
- Document `external_metadata` is stamped on every chunk and surfaced in hybrid retrieval. **Breaking:** `dlt` is now a core dependency — make sure it is installed if you manage dependencies by hand.
- **[v1.6.0 — Keyless workflows & pipeline reliability](https://github.com/topoteretes/EphapticOS/releases/tag/v1.6.0)** (September 18, 2026): build and search text memory with local models and no cloud LLM key; LLM-dependent improvement stages skip when no LLM is configured, and pipeline recovery preserves completed documents after crashes.


## Community & Support

### Contributing
We welcome contributions from the community! Your input helps make EphapticOS better for everyone. See [`CONTRIBUTING.md`](CONTRIBUTING.md) to get started.

### Code of Conduct

We're committed to fostering an inclusive and respectful community. Read our [Code of Conduct](https://github.com/topoteretes/EphapticOS/blob/main/CODE_OF_CONDUCT.md) for guidelines.

## Research & Citation

We recently published a research paper on optimizing knowledge graphs for LLM reasoning:

```bibtex
@misc{markovic2025optimizinginterfaceknowledgegraphs,
      title={Optimizing the Interface Between Knowledge Graphs and LLMs for Complex Reasoning},
      author={Vasilije Markovic and Lazar Obradovic and Laszlo Hajdu and Jovan Pavlovic},
      year={2025},
      eprint={2505.24478},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2505.24478},
}
```
