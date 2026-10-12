Title: Live Content

Description: Fetched live

Source: https://raw.githubusercontent.com/tt-a1i/archify/main/README.md

---

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/assets/archify-lockup-dark.svg" />
    <img src="docs/assets/archify-lockup-light.svg" alt="Archify" width="440" height="121" />
  </picture>
</p>
<h3 align="center">Turn anything you want to understand, plan, or share into an interactive visual.</h3>

<p align="center"><img src="docs/assets/archify-readme-hero.png" alt="Archify — interactive diagrams" width="960" /></p>

<p align="center"><strong>Official channels：</strong> <a href="https://archify.si">archify.si</a> · <a href="https://github.com/tt-a1i/archify">GitHub</a><br/>Archify is free and open source. Third-party online services and paid plans are operated by their respective providers and do not represent Archify. <a href="#official-services">Service details →</a></p>

<p align="center">Start with an idea, a question, or a plan. Describe it to your AI agent, and Archify turns it into an interactive HTML you can explore, customize, and share. From travel itineraries and learning maps to complex systems—make it your own.</p>

<p align="center">See what the community is creating—and imagine what you could make next.</p>

<p align="center">
  <a href="https://archify.si/gallery.html"><strong>Live demos</strong></a> &nbsp;·&nbsp;
  <a href="#start"><strong>Get started</strong></a> &nbsp;·&nbsp;
  <a href="https://archify.si/guide.html"><strong>Scenario guide</strong></a> &nbsp;·&nbsp;
  <a href="#community"><strong>Community</strong></a> &nbsp;·&nbsp;
  <a href="./README_ZH.md"><strong>简体中文</strong></a> &nbsp;·&nbsp;
  <a href="./README_JA.md"><strong>日本語</strong></a>
</p>

<p align="center">
  <a href="https://trendshift.io/repositories/31352?utm_source=repository-badge&amp;utm_medium=badge&amp;utm_campaign=badge-repository-31352" target="_blank" rel="noopener noreferrer"><img src="https://trendshift.io/api/badge/repositories/31352" alt="tt-a1i/archify | Trendshift" width="250" height="55" /></a>
</p>

<p align="center">
  <a href="https://github.com/tt-a1i/archify/stargazers"><img src="https://img.shields.io/github/stars/tt-a1i/archify?style=flat-square&amp;color=E5B650&amp;logo=github&amp;label=Stars" alt="GitHub stars" /></a>
  <a href="https://skills.sh/tt-a1i/archify/archify"><img src="https://img.shields.io/badge/installs-130K%2B-0EA5E9?style=flat-square" alt="130K+ installs on skills.sh" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-22c55e?style=flat-square" alt="MIT License" /></a>
  <a href="#installation-options"><img src="https://img.shields.io/badge/works_with-Claude_Code_%7C_Codex_%7C_Cursor_%7C_OpenCode-7C3AED?style=flat-square" alt="Works with Claude Code, Codex, Cursor, and OpenCode" /></a>
  <a href="CHANGELOG.md#301--2026-09-28"><img src="https://img.shields.io/badge/version-3.0.1-0891b2?style=flat-square" alt="Stable version 3.0.1" /></a>
</p>

<p align="center">
  <a href="https://archify.si/"><img src="https://img.shields.io/badge/Website-0891B2?style=for-the-badge" alt="Archify website" /></a>
  <a href="https://discord.gg/6xWMjgCeUq"><img src="https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&amp;logo=discord&amp;logoColor=white" alt="Join Archify on Discord" /></a>
  <a href="#community"><img src="https://img.shields.io/badge/WeChat-07C160?style=for-the-badge&amp;logo=wechat&amp;logoColor=white" alt="Archify WeChat group" /></a>
  <a href="#community"><img src="https://img.shields.io/badge/QQ-1688D8?style=for-the-badge&amp;logo=qq&amp;logoColor=white" alt="Archify QQ group" /></a>
  <a href="https://x.com/t20000622yy"><img src="https://img.shields.io/badge/Creator_on_X-181717?style=for-the-badge&amp;logo=x&amp;logoColor=white" alt="Follow the creator on X" /></a>
</p>

<p align="center"><a href="#sponsors"><strong>❤️ Partners & sponsors: Kimi Work · Supercode · OpenLux</strong></a></p>

## See Archify in action

<!-- archify-launch-video -->

https://github.com/user-attachments/assets/78570807-ba1d-4737-953f-55504a378a87

**One sentence. Your repo, mapped.** Watch the 35-second demo: explore the diagram, follow source links, and trace a path. [Try the interactive examples ↗](https://archify.si/gallery.html)

<a id="start"></a>

### Install, then describe your idea

Works with Cursor, Claude Code, Codex CLI, and OpenCode. See installation options below for additional integrations.

```bash
npx skills add tt-a1i/archify -g
```

Send this to your agent:

```text
Use Archify to diagram a web request: Browser calls the API,
the API checks Redis, and a cache miss queries PostgreSQL and fills the cache.
```

Then continue: “Add authentication”, “Highlight the cache-miss path”, or “Switch to the light theme”.

**No repository is required:** start with a description, or ask your agent to read a repository for a source-backed architecture diagram.

[Choose your agent](https://archify.si/start.html?agent=cursor&type=architecture) · [Installation details and update checks](#quick-start)

<a id="sponsors"></a>

## ❤️ Sponsors

<p align="center">
  <a href="https://www.kimi.ai/?aff=archify"><img src="docs/assets/sponsors/archify-kimi-work.png" alt="Archify × Kimi Work collaboration banner" width="800" /></a>
</p>

**Archify × Kimi Work.** Find Archify in the Kimi Work plugin store as **Interactive Architecture Diagram**. Describe your system in one sentence to create an interactive diagram. **[Try it in Kimi Work →](https://www.kimi.ai/?aff=archify)**

<table>
<tr>
  <td align="center" width="240"><a href="https://supercode.sh/?utm_source=archify"><img src="https://cdn.supercode.sh/sponsors/supercode-logo.png" alt="Supercode" width="200"/></a><br/><strong><a href="https://supercode.sh/?utm_source=archify">supercode.sh</a></strong></td>
<td><a href="https://supercode.sh/?utm_source=archify">Supercode</a> sponsors Archify and enhances Codex and Cursor with token optimization, curated Skills, and spec-driven development. Archify is featured as a <a href="https://supercode.sh/en/skills/tt-a1i/archify/archify">Supercode Editor’s Choice</a> skill.<br/><br/><a href="https://supercode.sh/en/skills/tt-a1i/archify/archify"><img src="https://supercode.sh/badges/editors-choice.svg" alt="Supercode Editor’s Choice — Archify" width="240" height="55"/></a></td>
</tr>
<tr>
<td align="center" width="240"><a href="https://www.openlux.ai/register?channel=c_qdvanbpc"><img src="docs/assets/sponsors/openlux-logo.png" alt="OpenLux" width="200" /></a><br/><strong><a href="https://www.openlux.ai/register?channel=c_qdvanbpc">OpenLux</a></strong></td>
<td>Thank you to OpenLux for sponsoring this project! OpenLux is an all-in-one AI platform for businesses, bringing together leading AI models from major providers worldwide. With fast, reliable service and responsive technical support, OpenLux offers base pricing for Claude, OpenAI, and Gemini models as low as 8.82%, 4%, and 8% of official rates, respectively.<br/><br/>Exclusive offer for Archify users: Sign up through our referral link and enjoy up to 7.5% off credit top-ups!<br/><br/><a href="https://www.openlux.ai/register?channel=c_qdvanbpc">Get started with OpenLux →</a></td>
</tr>
<tr>
<td align="center" width="240"><a href="https://zturbo.top"><img src="docs/assets/sponsors/zturbo-logo.png" alt="ZTURBO" width="200" /></a><br/><strong><a href="https://zturbo.top">ZTURBO</a></strong></td>
<td>Fast, stable connectivity for developers and AI users.<br/>New users can try the service for free and receive an exclusive bonus on their first top-up. Supports Windows, macOS, iOS, and Android; long-term plans work out to less than ¥1 per day.<br/><br/>Free trial · First top-up bonus · Multi-device connectivity<br/><br/><a href="https://zturbo.top">Try ZTURBO →</a></td>
</tr>
<tr>
<td align="center" width="240"><a href="https://www.packyapi.ai/register?aff=bN97"><img src="docs/assets/sponsors/packycode-logo.png" alt="PackyCode" width="200" /></a><br/><strong><a href="https://www.packyapi.ai/register?aff=bN97">PackyCode</a></strong></td>
<td>Access leading AI models through PackyCode with one API endpoint and one API key. Enjoy automatic failover and dedicated high-speed routes for Codex and Claude Code.<br/><br/>Get started with $1 in free credits, a discount on your first top-up, and savings of up to 80% on eligible routes. Pay in RMB with no currency conversion markups or extra top-up fees.<br/><br/><a href="https://www.packyapi.ai/register?aff=bN97">Get started with PackyCode →</a></td>
</tr>
<tr>
<td align="center" width="240"><a href="https://www.infistar.cc/register?aff=9N89LEMV&amp;ref_source=link"><img src="docs/assets/sponsors/infistar-logo.svg" alt="Infistar.cc" width="140" /></a><br/><strong><a href="https://www.infistar.cc/register?aff=9N89LEMV&amp;ref_source=link">Infistar.cc</a></strong></td>
<td>Thank you to Infistar.cc for sponsoring Archify! One API key covers text, image, and video creation with GPT, Claude, Gemini, DeepSeek, Qwen, Kling, and other models, without switching groups. Model API pricing starts at 1% of official rates, and AI images start at ¥0.06 each.<br/><br/>Exclusive offer for Archify users: Sign up through our referral link for $5 in trial credits and a special offer on your first top-up.<br/><br/><a href="https://www.infistar.cc/register?aff=9N89LEMV&amp;ref_source=link">Try Infistar →</a></td>
</tr>
<tr><td align="center" width="240"><a href="https://github.com/EverMind-AI/Raven"><img src="docs/assets/sponsors/evermind-archify-raven.png" alt="Archify × Raven" width="200" /></a><br/><strong><a href="https://github.com/EverMind-AI">EverMind</a> · <a href="https://github.com/EverMind-AI/Raven">Raven</a></strong></td><td>EverMind sponsors Archify and builds memory infrastructure for agents. Its <a href="https://github.com/EverMind-AI/Raven"><strong>Raven</strong></a> harness supports Archify as a Skill for verified, interactive system maps.</td></tr>
</table>

> Want to sponsor Archify? [Contact us by email.](mailto:2801884530@qq.com)

## Show what matters

| Explain an agent workflow | Follow a cache miss | Explore service relationships |
|---|---|---|
| [![Agent workflow tracing everything the planner drives](docs/assets/archify-demo-reach.png)](https://archify.si/gallery/artifacts/agent-tool-call.workflow.html?theme=dark&present=1#focus=planner&reach=downstream) | [![Cache-miss sequence showing the Web App to Postgres route](docs/assets/archify-demo-route.png)](https://archify.si/gallery/artifacts/cache-miss.sequence.html?theme=dark&present=1#route=web~db) | [![Production architecture comparing backend and database roles](docs/assets/archify-demo-lens.png)](https://archify.si/gallery/artifacts/production-deployment.architecture.html?theme=dark&present=1#lens=backend~database) |
| Trace everything downstream of one step. | Highlight the path from web app to database. | Focus on authored backend and database connections. |

The [Proof Lab](https://archify.si/gallery.html) contains all 11 checked-in scenarios, their JSON sources, and validation receipts.

### Understand a real repository

<sub>CODE → DIAGRAM · A source-backed system map</sub>

[![MCO runtime architecture generated from the public mco-org/mco repository](docs/assets/mco-runtime-share-card.png)](https://archify.si/cases/mco-runtime.architecture.html?theme=dark&present=1)

Archify traced [`mco-org/mco`](https://github.com/mco-org/mco) at `9f1a1cf` and produced this checked map. **[Open it ↗](https://archify.si/cases/mco-runtime.architectu

