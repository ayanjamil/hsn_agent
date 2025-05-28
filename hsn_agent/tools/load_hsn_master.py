# hsn_agent/tools/load_hsn_master.py

import pandas as pd
from pandas.errors import ParserError
from google.adk.tools.tool_context import ToolContext
# from google.adk.tools import FunctionTool

def load_hsn_master(path: str, tool_context: ToolContext) -> dict:
    """
    Reads the HSN_Master CSV (or Excel) at `path`, normalizes the headers,
    builds a dict of code→description, and stores it in tool_context.state["hsn_table"].
    """
    # 1) Read with comma first, else try tab
    try:
        df = pd.read_csv(path, dtype=str)
    except ParserError:
        df = pd.read_csv(path, sep="\t", dtype=str)

    # 2) Clean column names of extra quotes/whitespace
    df.columns = df.columns.str.strip().str.strip('"').str.strip("'")

    # 3) Validate columns exist
    expected = {"HSNCode", "Description"}
    if not expected.issubset(set(df.columns)):
        return {
            "status": "error",
            "message": f"Expected columns {expected!r} but found {list(df.columns)}"
        }

    # 4) Build lookup dict
    table = {code.strip(): desc for code, desc in zip(df["HSNCode"], df["Description"])}

    # 5) Save into shared state
    tool_context.state["hsn_table"] = table
    return {"status": "success", "loaded_rows": len(table)}

# load_hsn_master_tool = FunctionTool(
#     func=load_hsn_master,
#     name="load_hsn_master",
#     description="Load the HSN master CSV (or XLSX) into memory (state['hsn_table'])."
# )
