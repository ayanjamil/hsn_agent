import re
from typing import List, Dict
from google.adk.tools.tool_context import ToolContext
from hsn_agent.tools.load_hsn_master import load_hsn_master

def validate_hsn_code(
    codes: str,
    tool_context: ToolContext
) -> Dict[str, List[Dict[str, object]]]:
    if "hsn_table" not in tool_context.state:
        load_hsn_master(path="data/master_hsn.csv", tool_context=tool_context)

    hsn_table = tool_context.state.get("hsn_table", {})
    if not hsn_table:
        return {"status": "error", "message": "Failed to load HSN master. Please check the CSV path."}

    entries = [c.strip() for c in re.split(r"[\s,]+", codes) if c.strip()]
    results = []

    for code in entries:
        if not re.fullmatch(r"\d{2,8}", code):
            results.append({
                "code": code,
                "status": "invalid_format",
                "reason": "must be 2–8 digits"
            })
            continue

        desc = hsn_table.get(code)
        if desc is None:
            results.append({
                "code": code,
                "status": "not_found"
            })
            continue

        hierarchy = []
        for length in (2, 4, 6, 8):
            if len(code) >= length:
                prefix = code[:length]
                prefix_desc = hsn_table.get(prefix)
                hierarchy.append({
                    "code": prefix,
                    "description": prefix_desc or "(no entry in master)",
                    "exists": bool(prefix_desc)
                })

        hierarchy_lines = "\n".join(
            f"- {h['code']}: {h['description']}" for h in hierarchy
        )
        message = (
            f"The HSN code {code} is valid and corresponds to:\n\n"
            f"    {desc}\n\n"
            f"It sits under this hierarchy (broadest → specific):\n"
            f"{hierarchy_lines}"
        )

        results.append({
            "code": code,
            "status": "valid",
            "description": desc,
            "hierarchy": hierarchy,
            "message": message,
        })

    return {"results": results}
