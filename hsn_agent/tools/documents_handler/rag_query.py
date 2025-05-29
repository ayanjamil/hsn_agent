import logging
import re

from google.adk.tools.tool_context import ToolContext
from vertexai import rag

from hsn_agent.tools.load_hsn_master import load_hsn_master

from ...config import (
    DEFAULT_DISTANCE_THRESHOLD,
    DEFAULT_TOP_K,
)
from ..utils import check_corpus_exists, get_corpus_resource_name

def rag_query(
    corpus_name: str,
    query: str,
    tool_context: ToolContext,
) -> dict:
    if "hsn_table" not in tool_context.state:
        load_hsn_master(path="data/master_hsn.csv", tool_context=tool_context)
    hsn_table = tool_context.state.get("hsn_table", {})

    m_end = re.search(r"ends? with (\d+)", query, re.I)
    m_start = re.search(r"(?:begins|starts) with (\d+)", query, re.I)
    m_contains = re.search(r"(?:contains|has) (\d+)", query, re.I)

    if hsn_table and (m_end or m_start or m_contains):
        if m_end:
            pattern, mode = m_end.group(1), "ends with"
        elif m_start:
            pattern, mode = m_start.group(1), "begins with"
        else:
            pattern, mode = m_contains.group(1), "contains"

        if mode == "ends with":
            matches = [c for c in hsn_table if c.endswith(pattern)]
        elif mode == "begins with":
            matches = [c for c in hsn_table if c.startswith(pattern)]
        else:
            matches = [c for c in hsn_table if pattern in c]

        suggestions = []
        for code in matches[:5]:
            desc = hsn_table[code]
            entry = {"code": code, "description": desc}
            if desc.strip().upper() == "OTHER":
                for length in (6, 4, 2):
                    if len(code) >= length:
                        parent = code[:length]
                        pdesc = hsn_table.get(parent, "").strip()
                        if pdesc and pdesc.upper() != "OTHER":
                            entry["explanation"] = (
                                f"This 'OTHER' is the catch‐all category under '{pdesc}'."
                            )
                            break
            suggestions.append(entry)

        if suggestions:
            lines = []
            for s in suggestions:
                line = f"- {s['code']}: {s['description']}"
                if "explanation" in s:
                    line += f" — {s['explanation']}"
                lines.append(line)

            prompt = (
                f"I found these HSN codes that {mode} '{pattern}':\n"
                + "\n".join(lines)
                + "\n\nDo any of these look right? Or tell me more about the product/service."
            )
            return {
                "status": "pattern_suggestions",
                "query": query,
                "pattern": pattern,
                "mode": mode,
                "suggestions": suggestions,
                "message": prompt,
            }
        else:
            return {
                "status": "warning",
                "query": query,
                "message": f"No HSN codes {mode} '{pattern}' were found in the master list."
            }

    # --- fallback to standard RAG retrieval ---
    try:

        if not check_corpus_exists(corpus_name, tool_context):
            return {
                "status": "error",
                "message": f"Corpus '{corpus_name}' does not exist. Please create it first using the create_corpus tool.",
                "query": query,
                "corpus_name": corpus_name,
            }

        corpus_resource_name = get_corpus_resource_name(corpus_name)
        rag_retrieval_config = rag.RagRetrievalConfig(
            top_k=DEFAULT_TOP_K,
            filter=rag.Filter(vector_distance_threshold=DEFAULT_DISTANCE_THRESHOLD),
        )
        response = rag.retrieval_query(
            rag_resources=[
                rag.RagResource(
                    rag_corpus=corpus_resource_name,
                )
            ],
            text=query,
            rag_retrieval_config=rag_retrieval_config,
        )

        results = [
            {
                "source_uri": getattr(c, "source_uri", ""),
                "source_name": getattr(c, "source_display_name", ""),
                "text": getattr(c, "text", ""),
                "score": getattr(c, "score", 0.0),
            }
            for c in getattr(response.contexts, "contexts", [])
        ]

        if not results:
            return {
                "status": "warning",
                "message": f"No results found in corpus '{corpus_name}' for query: '{query}'",
                "query": query,
                "corpus_name": corpus_name,
                "results": [],
                "results_count": 0,
            }

        return {
            "status": "success",
            "message": f"Successfully queried corpus '{corpus_name}'",
            "query": query,
            "corpus_name": corpus_name,
            "results": results,
            "results_count": len(results),
        }

    except Exception as e:
        error_msg = f"Error querying corpus: {str(e)}"
        logging.error(error_msg)
        return {
            "status": "error",
            "message": error_msg,
            "query": query,
            "corpus_name": corpus_name,
        }
