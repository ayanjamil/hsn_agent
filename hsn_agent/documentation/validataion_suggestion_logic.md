# Validation and Suggestion Logic

This document describes the core validation and suggestion algorithms used by the HSN Code Validation & Suggestion Agent.

---

## 1. Format Validation

**Purpose:** Ensure user inputs conform to expected HSN code format before deeper checks.

- **Rules:**
  - Must be numeric only.
  - Length must be between 2 and 8 digits (inclusive).

**Examples:**

| Input       | Outcome            |
| ----------- | ------------------ |
| `123`       | Pass (format OK)   |
| `1`         | Fail (too short)   |
| `123456789` | Fail (too long)    |
| `12A4`      | Fail (non-numeric) |

---

## 2. Existence Validation

**Purpose:** Verify that a correctly formatted code exists in the master HSN table.

- **Rules:**
  - Lookup code in the in-memory `hsn_table` (dict of code→description).

**Examples:**

| Input    | Outcome   |
| -------- | --------- |
| `0101`   | Found     |
| `999999` | Not found |

---

## 3. Hierarchical Validation

**Purpose:** Break an 8‑digit code into parent segments (2, 4, 6, 8) and verify each exists, providing insights on classification hierarchy.

- **Rules:**
  - For code lengths ≥ 2: include first 2 digits.
  - For code lengths ≥ 4: include first 4 digits.
  - For code lengths ≥ 6: include first 6 digits.
  - Always include full-length code.

**Example:**  
Input: `01011010`

| Prefix     | Exists | Description                                    |
| ---------- | ------ | ---------------------------------------------- |
| `01`       | True   | LIVE ANIMALS                                   |
| `0101`     | True   | LIVE HORSES, ASSES, MULES AND HINNIES          |
| `010110`   | True   | LIVE HORSES… PURE‑BRED BREEDING ANIMALS        |
| `01011010` | True   | LIVE HORSES… PURE‑BRED BREEDING ANIMALS HORSES |

---

## 4. Suggestion Logic

**Purpose:** Provide relevant HSN code suggestions for free-text product or service descriptions.

- **Approach:**
  1. **Vector Search (RAG):** Embed user query, retrieve top-k similar document chunks from the HSN corpus.
  2. **Pattern Matching:** For numeric-pattern queries (`ends with`, `begins with`, `contains`), scan keys in `hsn_table`.

**Details:**

- **RAG Retrieval:**
  - Configured with `top_k = 5`, a distance threshold (e.g. 0.5).
  - Returns code contexts with similarity scores.

**Examples:**

- Query: `horse for polo`
  ```text
  1. 01012910 – Horses for polo (score: 0.92)
  2. 01019010 – LIVE HORSES… OTHER – HORSES FOR POLO (score: 0.89)
  …
  ```
- Query: `ends with 90`
  ```text
  - 01011090: LIVE HORSES… OTHER
  - 01019090: OTHER
  …
  ```

---

## 5. Edge Case Handling

- **Empty Input:** Return a prompt to provide either a code or description.
- **Whitespace/Casing:** Trim and normalize before matching.
- **Multi-code Batch:** Support comma-separated lists, validating each independently.
- **Unknown Patterns:** Fallback to RAG free-text retrieval if pattern detection fails.

**Example:**  
Input: `, , ,`  
Output:

```text
No valid HSN codes detected. Please enter a 2–8 digit code or a product description.
```
