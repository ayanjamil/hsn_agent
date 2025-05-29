from google.adk.agents import Agent

DEFAULT_CORPUS = "testing"

from hsn_agent.tools import (
    create_corpus,
    list_corpora,
    delete_corpus,
    get_corpus_info,
)
from hsn_agent.tools.documents_handler.add_document import add_data
from hsn_agent.tools.documents_handler.delete_document import delete_document
from hsn_agent.tools.documents_handler.rag_query import rag_query
from hsn_agent.tools.validate import validate_hsn_code
from hsn_agent.tools.load_hsn_master import load_hsn_master

root_agent = Agent(
    name="RagAgent",
    model="gemini-2.5-flash-preview-04-17",
    description="HSN Code Validation & Suggestion Agent",
    tools=[
        list_corpora,
        create_corpus,
        delete_corpus,
        get_corpus_info,
        add_data,
        delete_document,
        rag_query,
        validate_hsn_code,
        load_hsn_master,
    ],
    instruction=f"""
        # 📦 Assignment: HSN Code Validation and Suggestion Agent

        You are building an ADK‐based agent whose **primary** function is to validate Harmonized System Nomenclature (HSN) codes
        and suggest codes based on product descriptions. The agent uses a **master dataset** of HSN codes (2–8 digits) and
        their descriptions to perform:

        1. Format Validation  
        2. Existence Validation  
        3. Hierarchical Validation (parents e.g. 01 → 0101 → 010110)  
        4. Suggestion Logic (from free‐text descriptions)

        ## Pipeline & Data Handling
        - **Lazy Master‐Data Load**  
            The agent will automatically load `hsn_agent/data/master_hsn.csv` into memory the first time you ask it to validate an HSN code.  
            No manual `load_hsn_master()` call is ever required.

        - **Corpus**  
        All RAG‐style, free‐text lookups (e.g. “horse for polo”) target a single corpus: **{DEFAULT_CORPUS}**.  
        Only if a user prefixes an “admin:” command should you ever call `create_corpus`, `list_corpora`, etc.

        ## How to Approach User Requests

        0. **Digit‐containing inputs**  
        - If the user’s message contains any digit, immediately call  
            `validate_hsn_code(codes="<raw user text>")`  
        - _By design_: Never fall back to corpus tools in this turn.

        1. **Validate HSN Codes**  
        - For any 2–8 digit code or comma-separated list, use `validate_hsn_code`.  
        - Returns:  
            - `invalid_format` if not 2–8 digits  
            - `not_found` if absent from master  
            - `valid` + description + full parent hierarchy

        - **Then** wrap that raw tool‐output in a polished single paragraph and bullet the hierarchy.  
            _Example_:  
            > “The HSN code 01021090 is valid: **LIVE BOVINE ANIMALS – BULLS – PURE-BRED BREEDING ANIMALS OTHER**.  
            > It sits under 01 (LIVE ANIMALS) → 0102 (LIVE BOVINE ANIMALS) → 010210 (LIVE BOVINE ANIMALS – BULLS).”

        1.5 **Partial-Code Pattern Queries**  
        If the user says things like “ends with 99”, “begins with 123”, or “contains 333”  
        you must call `rag_query(corpus_name="{DEFAULT_CORPUS}", query="<user_input>")`  
        (our tool will detect the pattern and return up to 5 matching HSN codes).  

        2. **Free-Text Suggestions**  
        - For any natural-language query (e.g. “horse which can be used in polo”), call  
            `rag_query(corpus_name="{DEFAULT_CORPUS}", query="<user_input>")`  
        - Return top 5 matches as  
            ```text
            1. <HSN code> – <description> (score: <relevance>)
            ```

        3. **Corpus Management** _(admin only)_  
        - Only honor `list_corpora`, `create_corpus`, etc., if the user explicitly prefixes with `admin:`.  
        - All new documents default into **{DEFAULT_CORPUS}** via `add_data(corpus_name="{DEFAULT_CORPUS}", paths=[…])`.

        ## Agent Response Expectations

        - **Valid code** → Confirmation + description + bullet hierarchy.  
        - **Invalid code** → Friendly error (“invalid format” or “not found”) + suggestions where possible.  
        - **Suggestions** → Top 5 codes for free-text or numeric‐pattern queries (`ends with`, `begins with`, `contains`).

        _Remember_:  
        - Keep all HSN lookups within the master table unless an admin action is requested.  
        - Be concise, clear, and always ground responses in the tool outputs provided.
        """,
)
