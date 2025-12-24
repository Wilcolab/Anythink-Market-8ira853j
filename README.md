# AcmeCloud RAG Support Assistant

**Internal R&D Prototype** | Engineering Team

---

## Overview

This prototype explores whether a Retrieval-Augmented Generation (RAG) system can help reduce Support team workload by providing accurate, context-aware answers to common customer inquiries.

The system retrieves relevant information from our internal knowledge base (FAQs and escalation notes) and uses it to generate responses via an LLM.

## Project Status

🔬 **Experimental** - This is an exploratory prototype for internal evaluation.

## Quick Start

> ⚠️ **Note**: This project contains `TODO` stubs that must be implemented before it will run. See [Implementation Tasks](#implementation-tasks) below.

### Prerequisites

- Python 3.11+
- OpenAI API key

### Setup

1. Open this repository in GitHub Codespaces (recommended) or clone locally

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set your OpenAI API key (choose one method):

   ```bash
   # Option A: Environment variable
   export OPENAI_API_KEY="your-api-key-here"

   # Option B: Create a .env or .env.local file
   echo 'OPENAI_API_KEY=your-api-key-here' > .env.local
   ```

4. Run the evaluation:
   ```bash
   python run_eval.py
   ```

## Project Structure

```
├── data/
│   ├── faq.json              # Public FAQ entries
│   ├── escalation_notes.json # Internal support escalation notes
│   └── eval_questions.json   # Evaluation question set with reference answers
├── src/
│   ├── config.py             # Configuration settings
│   ├── data_loader.py        # Document loading utilities
│   ├── llm_client.py         # OpenAI API wrapper
│   ├── embeddings.py         # Text embedding functions [EDITABLE]
│   ├── retrieval.py          # Document retrieval logic [EDITABLE]
│   └── rag_pipeline.py       # Main RAG pipeline [EDITABLE]
├── run_eval.py               # Evaluation runner script
└── requirements.txt
```

## Implementation Tasks

The following modules contain `TODO` markers indicating where implementation is needed:

### 1. Embeddings (`src/embeddings.py`)

- `embed_texts()`: Convert text strings to vector embeddings
- `embed_documents()`: Embed all documents in the knowledge base

### 2. Retrieval (`src/retrieval.py`)

- `cosine_similarity()`: Compute similarity between query and documents
- `retrieve()`: Find and return the most relevant documents

### 3. RAG Pipeline (`src/rag_pipeline.py`)

- `build_context()`: Format retrieved documents into context
- `build_prompt()`: Create the LLM prompt with context and question
- `answer_question()`: Orchestrate the full RAG pipeline

## Configuration

Edit `src/config.py` to adjust:

| Setting              | Default                  | Description                     |
| -------------------- | ------------------------ | ------------------------------- |
| `embedding_model`    | `text-embedding-3-small` | OpenAI embedding model          |
| `llm_model`          | `gpt-4o-mini`            | LLM for response generation     |
| `top_k`              | `3`                      | Number of documents to retrieve |
| `retrieval_strategy` | `cosine`                 | Similarity metric               |
| `max_context_length` | `4000`                   | Maximum context characters      |

## Evaluation

The evaluation script (`run_eval.py`) tests the RAG pipeline against 10 predefined questions covering:

- Easy FAQ lookups
- Medium-complexity support scenarios
- Hard edge cases requiring internal knowledge

Reference answers are provided for qualitative comparison.

## Data Sources

| Source           | Count | Description                    |
| ---------------- | ----- | ------------------------------ |
| FAQ              | 10    | Public customer-facing answers |
| Escalation Notes | 10    | Internal support procedures    |

## Next Steps

After implementing the core components:

1. Run `python run_eval.py` to test the pipeline
2. Review generated answers against reference answers
3. Experiment with configuration changes
4. Document findings for team review

---

_AcmeCloud Engineering | Internal Use Only_
