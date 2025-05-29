import re
import difflib
from typing import List, Dict
from google.adk.tools.tool_context import ToolContext
from hsn_agent.tools.load_hsn_master import load_hsn_master

def validate_hsn_code(
    codes: str,
    tool_context: ToolContext
) -> Dict[str, object]:
    if "hsn_table" not in tool_context.state:
        load_hsn_master(path="hsn_agent/data/master_hsn.csv", tool_context=tool_context)
    hsn_table = tool_context.state.get("hsn_table", {})

    if not hsn_table:
        return {"status": "error", "message": "Could not load HSN master. Check CSV path."}

    entries = [c.strip() for c in re.split(r"[\s,]+", codes) if c.strip()]
    out_results = []

    for code in entries:
        if not re.fullmatch(r"\d{2,8}", code):
            out_results.append({
                "code": code,
                "status": "invalid_format",
                "reason": "must be 2–8 digits"
            })
            continue

        desc = hsn_table.get(code)
        if desc:
            hierarchy = []
            for length in (2,4,6,8):
                if len(code) >= length:
                    p = code[:length]
                    hierarchy.append({
                        "code": p,
                        "description": hsn_table.get(p, "(no entry)"),
                        "exists": p in hsn_table
                    })
            hierarchy_lines = "\n".join(f"- {h['code']}: {h['description']}" for h in hierarchy)
            msg = (
                f"The HSN code {code} is valid and corresponds to:\n\n"
                f"    {desc}\n\n"
                f"It sits under this hierarchy:\n"
                f"{hierarchy_lines}"
            )
            out_results.append({
                "code": code,
                "status": "valid",
                "description": desc,
                "hierarchy": hierarchy,
                "message": msg
            })
            continue

        # 3) No exact match → build fuzzy suggestions
        all_codes = list(hsn_table.keys())
        close = difflib.get_close_matches(code, all_codes, n=5, cutoff=0.5)

        if close:
            suggestion_list = [
                {"code": c, "description": hsn_table[c]}
                for c in close
            ]
            prompt = (
                f"I couldn’t find an exact match for '{code}'.\n"
                f"Did you mean one of these?\n"
                + "\n".join(f"- {c}: {hsn_table[c]}" for c in close)
                + "\n\n"
                "Or please provide a short description of the product/service so I can help narrow it down."
            )
            out_results.append({
                "code": code,
                "status": "not_found",
                "suggestions": suggestion_list,
                "prompt": prompt
            })
        else:
            out_results.append({
                "code": code,
                "status": "not_found",
                "message": f"No HSN codes similar to '{code}' found. Please check your entry or give me a description."
            })

    return {"results": out_results}
