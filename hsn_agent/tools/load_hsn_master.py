import os
import pandas as pd
from pandas.errors import ParserError
from google.adk.tools.tool_context import ToolContext

def load_hsn_master(path: str, tool_context: ToolContext) -> dict:
    """
    Reads the HSN master file at `path` (CSV or XLSX), 
    normalizes headers, builds a dict code→description, 
    and stores it in tool_context.state["hsn_table"].
    """
    # 1) Check file exists
    if not os.path.isfile(path):
        return {"status": "error", "message": f"File not found: {path}"}

    # 2) Read into DataFrame
    ext = os.path.splitext(path)[1].lower()
    try:
        if ext in (".xls", ".xlsx"):
            df = pd.read_excel(path, dtype=str)
        else:
            df = pd.read_csv(path, dtype=str)
    except ParserError:
        # Retry with tabs
        try:
            df = pd.read_csv(path, sep="\t", dtype=str)
        except Exception as e:
            return {"status": "error", "message": f"Failed to parse {path}: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"Error loading {path}: {e}"}

    # 3) Normalize column names
    df.columns = df.columns.str.strip().str.strip('"').str.strip("'")

    # 4) Validate required columns
    required = {"HSNCode", "Description"}
    missing = required - set(df.columns)
    if missing:
        return {
            "status": "error",
            "message": f"Missing columns {missing}. Found: {list(df.columns)}"
        }

    # 5) Build lookup dict
    table = {
        str(code).strip(): str(desc).strip()
        for code, desc in zip(df["HSNCode"], df["Description"])
        if pd.notna(code)
    }

    # 6) Store in shared state
    tool_context.state["hsn_table"] = table

    return {"status": "success", "loaded_rows": len(table)}
