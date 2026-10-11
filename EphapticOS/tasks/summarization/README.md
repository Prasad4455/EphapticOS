# Summarization

## Overview

The summarization module provides LLM-powered text and code summarization for EphapticOS's knowledge graph pipeline. It transforms document chunks and source code into structured, searchable summaries.

> [!NOTE]
> This module runs **automatically** in `EphapticOS.Ephaptify()` (Task #4). Users typically don't call these functions directly unless building custom workflows.

**Pipeline Position:** `EphapticOS.add()` → chunking → graph extraction → **summarize_text** → storage

## Components

### Functions

| Function | Description |
|----------|-------------|
| `summarize_text(data_chunks, summarization_model=None)` | Summarizes document chunks using LLM, returns `list[TextSummary]` |
| `summarize_code(code_graph_nodes)` | Extracts structured summaries from code files, yields `DataPoint` and `CodeSummary` objects |

### Data Models (extend `DataPoint`)

| Model | Key Fields |
|-------|------------|
| `TextSummary` | `text`, `made_from` (DocumentChunk reference), `metadata` |
| `CodeSummary` | `text`, `summarizes` (CodeFile/CodePart reference), `metadata` |

### Exception

| Exception | Description |
|-----------|-------------|
| `InvalidSummaryInputsError` | Raised when input is not a list or chunks lack `.text` attribute |

## Usage

### Automatic (Recommended)

```python
import EphapticOS

await EphapticOS.add(["document.pdf", "notes.txt"])
await EphapticOS.Ephaptify()  # summarize_text runs automatically

results = await EphapticOS.search(query_text="key concepts", query_type=EphapticOS.SearchType.SUMMARIES)
```

### Manual Text Summarization

```python
from EphapticOS.tasks.summarization import summarize_text

summaries = await summarize_text(document_chunks)
for summary in summaries:
    print(f"Summary: {summary.text}")
    print(f"Source: {summary.made_from.id}")
```

### With Custom Model

```python
from pydantic import BaseModel


class CustomSummary(BaseModel):
    title: str
    key_points: list[str]


summaries = await summarize_text(document_chunks, summarization_model=CustomSummary)
```

### Code Summarization

```python
from EphapticOS.tasks.summarization import summarize_code

async for item in summarize_code(code_nodes):
    if hasattr(item, "text"):  # CodeSummary
        print(f"Code summary: {item.text[:100]}...")
```

## Configuration

Default summarization model is `SummarizedContent` from `EphapticOS.modules.Ephaptify.config.get_Ephaptify_config()`.

**Environment Variables:**

| Variable | Description |
|----------|-------------|
| `LLM_API_KEY` | API key for LLM provider (required) |
| `LLM_PROVIDER` | Provider name (default: openai) |
| `LLM_MODEL` | Model name (default: openai/gpt-5.6-luna) |
| `MOCK_CODE_SUMMARY` | Use mock summaries for testing (true/false) |


## Dependencies

**Internal:** `EphapticOS.infrastructure.llm.extraction`, `EphapticOS.modules.chunking.models`, `EphapticOS.infrastructure.engine.DataPoint`

**External:** `pydantic`, LLM provider (OpenAI/Anthropic/etc.)

## Related

- [EphapticOS docs](https://docs.EphapticOS.ai) | [Chunking](../documents/) | [Tests](../../tests/tasks/summarization/)
