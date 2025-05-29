import re
import logging
from google.adk.tools.tool_context import ToolContext
from vertexai import rag

from ...config import (
    DEFAULT_DISTANCE_THRESHOLD,
    DEFAULT_TOP_K,
)
from ..utils import check_corpus_exists, get_corpus_resource_name
from ..load_hsn_master import load_hsn_master


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
            pattern = m_end.group(1)
            mode = "ends with"
            matches = [c for c in hsn_table if c.endswith(pattern)]
        elif m_start:
            pattern = m_start.group(1)
            mode = "begins with"
            matches = [c for c in hsn_table if c.startswith(pattern)]
        else:
            pattern = m_contains.group(1)
            mode = "contains"
            matches = [c for c in hsn_table if pattern in c]

        suggestions = [
            {"code": c, "description": hsn_table[c]}
            for c in matches[:5]
        ]
        if suggestions:
            prompt = (
                f"I found these HSN codes that {mode} '{pattern}':\n"
                + "\n".join(f"- {s['code']}: {s['description']}" for s in suggestions)
                + "\n\nDo any of these look right? Or tell me more about the product/service."
            )
            return {
                "status": "pattern_suggestions",
                "query": query,
                "pattern": pattern,
                "mode": mode,
                "suggestions": suggestions,
                "message": prompt
            }
        else:
            return {
                "status": "warning",
                "query": query,
                "message": f"No HSN codes {mode} '{pattern}' were found in the master list."
            }

    # --- 3) Fallback to normal RAG corpus lookup ---
    try:
        if not check_corpus_exists(corpus_name, tool_context):
            return {
                "status": "error",
                "message": f"Corpus '{corpus_name}' does not exist. Please create it first.",
                "query": query,
                "corpus_name": corpus_name,
            }

        corpus_resource_name = get_corpus_resource_name(corpus_name)
        cfg = rag.RagRetrievalConfig(
            top_k=DEFAULT_TOP_K,
            filter=rag.Filter(vector_distance_threshold=DEFAULT_DISTANCE_THRESHOLD),
        )

        response = rag.retrieval_query(
            rag_resources=[rag.RagResource(rag_corpus=corpus_resource_name)],
            text=query,
            rag_retrieval_config=cfg,
        )

        results = []
        for ctxg in getattr(response.contexts, "contexts", []):
            results.append({
                "source_uri": getattr(ctxg, "source_uri", ""),
                "source_name": getattr(ctxg, "source_display_name", ""),
                "text": getattr(ctxg, "text", ""),
                "score": getattr(ctxg, "score", 0.0),
            })

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
        logging.error(f"Error querying corpus: {e}")
        return {
            "status": "error",
            "message": f"Error querying corpus: {e}",
            "query": query,
            "corpus_name": corpus_name,
        }
