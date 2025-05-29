# Data Handling

This document describes how the HSN Code Validation & Suggestion Agent manages the master dataset (`master_hsn.csv` / Excel), including loading strategies, performance trade-offs, and error handling.

---

## 1. File Reading Workflow

- **Library**: Uses `pandas` to read CSV or Excel files.
- **Primary Path**: `data/master_hsn.csv` by default, with ability to accept alternate file paths.
- **Reader Logic**:
  1. Attempt `pd.read_csv(path, dtype=str)` for comma-delimited files.
  2. If a `ParserError` occurs, retry with `pd.read_csv(path, sep='\t', dtype=str)` for tab-delimited files.
  3. Normalize column names: strip whitespace and quotes to ensure headers `HSNCode` and `Description` match expected names.

## 2. Pre‑processing vs. On‑demand Loading

### Pre‑processing (Batch)

- Load the entire master dataset at agent startup.
- **Pros**: Low per-request latency, immediate lookup availability.
- **Cons**: Higher memory footprint, longer cold start time if the file is large.

### On‑demand (Lazy) Loading

- Delay reading the file until the first validation request arrives.
- Stored in `tool_context.state['hsn_table']` for reuse.
- **Pros**: Faster startup, memory only used if/when needed.
- **Cons**: Slight delay on the first validation call.

_Current Implementation_: Lazy loading on the first `validate_hsn_code` or `rag_query` that needs the master table.

## 3. Memory & Performance Trade‑offs

| Strategy            | Startup Cost | Memory Usage         | Request Latency                 |
| ------------------- | ------------ | -------------------- | ------------------------------- |
| Pre‑load all data   | High         | High                 | Low                             |
| Lazy load on demand | Low          | Moderate (when used) | Moderate on first use, then low |

- For medium (~30k rows) datasets, lazy loading keeps agent responsive while still delivering sub-50 ms lookups after load.
- For very large datasets (>200k rows), consider incremental loading or external database.

## 4. Handling Large Datasets

1. **Caching**: Keep the loaded `hsn_table` in `tool_context.state` across calls, avoid reloading unless file changes.
2. **Vector Index**: RAG ingestion splits documents into chunks, embeds them, and stores in Vertex AI’s vector index; supports sub-linear semantic lookups.

## 5. Error Handling & Validation

- **Missing File**:
  - If the provided path does not exist or is inaccessible, return an error:
    ```json
    { "status": "error", "message": "Master file not found at <path>" }
    ```
- **Malformed Rows**:
  - If any row is missing `HSNCode` or `Description`, those rows are logged and skipped.
  - If headers don’t match exactly `HSNCode` and `Description`, return an error listing detected columns.
- **Duplicate Codes**:
  - On `update_master`, duplicate entries are dropped, keeping the latest uploaded row.
- **Type Safety**:
  - All fields loaded as strings (`dtype=str`) to preserve leading zeros and avoid numeric coercion issues.

---
