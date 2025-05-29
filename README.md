# HSN Code Validation & Suggestion Agent

![Agent Architecture](docs/architecture.png)

## Table of Contents

1. [Objective](#objective)
2. [Overview](#overview)
3. [Prerequisites](#prerequisites)
4. [Setup & Installation](#setup--installation)
5. [Usage](#usage)
6. [Agent Design](#agent-design)
7. [Data Handling](#data-handling)
8. [Validation & Suggestion Logic](#validation--suggestion-logic)
9. [Agent Response Format](#agent-response-format)
10. [Project Structure](#project-structure)

---

## Objective

This repository implements an intelligent agent using Google's Agent Developer Kit (ADK) and Vertex AI. The agent:

- **Validates** Harmonized System Nomenclature (HSN) codes (2–8 digits) against a master dataset.
- **Suggests** HSN codes based on free-text product/service descriptions.

It leverages RAG (Retrieval-Augmented Generation) for natural-language lookup and a local CSV for efficient code validation.

## Overview

**Assessment**: HSN Code Validation and Suggestion Agent

**Framework**: [ADK - Agent Developer Kit](https://google.github.io/adk-docs/)

**Problem**: Build an agent that:

1. **Validates** user-provided HSN codes against a master file (Excel/CSV).
2. **Suggests** codes for natural-language queries (e.g. "horse for polo").

Each HSN code level adds specificity:

- `01` → LIVE ANIMALS
- `0101` → LIVE HORSES, ASSES, MULES AND HINNIES
- `01011010` → PURE-BRED HORSES FOR BREEDING

**Dataset**: `data/master_hsn.csv` (columns: `HSNCode`, `Description`)

---

## Prerequisites

- **Google Cloud Project** with Vertex AI API enabled
- **Google Cloud SDK** installed and authenticated (`gcloud init`)
- **Python 3.9+**

---

## Setup & Installation

```bash
# 1. Create & activate virtual environment
conda create --name hsnAgent python=3.10
conda activate hsnAgent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Verify gcloud
gcloud --version

# 4. Initialize gcloud
gcloud init --project=<YOUR_PROJECT_ID>

# 5. Run agent server
adk web
```

Navigate to [http://localhost:8000](http://localhost:8000) to interact.

---

## Usage

1. **Validate a code**:

   - Send any message containing digits (e.g. `01011010`).
   - The agent returns validity, description, and hierarchy.

2. **Free-text lookup**:

   - Ask natural-language questions (e.g. "horse for polo").
   - Returns top 5 relevant HSN codes from the RAG corpus.

3. **Admin actions** (prefix with `admin:`):

   - Manage corpora (`create_corpus`, `list_corpora`, etc.)
   - Update master CSV and ingest into corpus via `update_master` tool.

---

## Agent Design

**Architecture**: ADK `Agent` with tools:

- `validate_hsn_code` — local CSV lookup & hierarchy logic.
- `rag_query` — Vertex AI RAG for free-text and pattern queries.
- `load_hsn_master` / `update_master` — manage master table in memory/disk.
- Corpus management: `list_corpora`, `create_corpus`, `add_data`, etc.

**Flow**:

1. **Lazy load** master CSV on first validation request.
2. **Digit input** → validation tool only.
3. **Pattern queries** (`ends with`, `begins with`, `contains`) → treat via `rag_query` over master table.
4. **Free-text** → `rag_query` on default corpus.
5. **Admin:** Corpus and master-data management.

---

## Data Handling

- **Master CSV** stored at `data/master_hsn.csv`.
- **Lazy load** into `tool_context.state["hsn_table"]` on-demand.
- **Updates** via `update_master` tool: merges new rows, reloads in-memory, and ingests into RAG.

**Trade-offs**:

- Local CSV: instant lookups, no extra API calls.
- RAG corpus: semantic retrieval for descriptions.

---

## Validation & Suggestion Logic

1. **Format Validation**: Must be 2–8 digits.
2. **Existence Validation**: Exact match in master.
3. **Hierarchical Validation**: Check parent codes at lengths 2,4,6.
4. **Suggestion Logic**:

   - **Pattern**: ends/starts/contains → list top 5 code matches from master.
   - **Natural language**: RAG over default corpus ⇒ top-5.

---

## Agent Response Format

- **Valid code**:

  > The HSN code **01021090** is valid: _LIVE BOVINE ANIMALS – BULLS – PURE-BRED BREEDING ANIMALS OTHER_.
  > Hierarchy:
  >
  > - `01` LIVE ANIMALS
  > - `0102` LIVE BOVINE ANIMALS
  > - `010210` LIVE BOVINE ANIMALS – BULLS

- **Invalid code**:

  > Code `123`: ❌ invalid format (must be 2–8 digits).

- **Pattern suggestions**:

  > I found these codes that end with `90`:
  >
  > - `0101290`: Horses for polo
  >   ...

- **Free-text suggestions**:

  1. `01012910` – Horses for polo (score: 0.92)
  2. ...

---

## Project Structure

```
├── data/master_hsn.csv       # Master HSN dataset
├── hsn_agent/
│   ├── agent.py              # ADK agent definition
│   ├── tools/                # FunctionTool implementations
│   └── config.py             # Chunking, top_k, etc.
├── README.md                 # This file
└── requirements.txt          # Python deps
```

---
