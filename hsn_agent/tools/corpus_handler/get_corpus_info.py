from google.adk.tools.tool_context import ToolContext
from vertexai import rag

from ..utils import check_corpus_exists, get_corpus_resource_name


def get_corpus_info(
    corpus_name: str,
    tool_context: ToolContext,
) -> dict:
    
    try:
        if not check_corpus_exists(corpus_name, tool_context):
            return {
                "status": "error",
                "message": f"Corpus '{corpus_name}' does not exist",
                "corpus_name": corpus_name,
            }
        corpus_resource_name = get_corpus_resource_name(corpus_name)
        corpus_display_name = corpus_name  

        file_details = []
        try:
            files = rag.list_files(corpus_resource_name)
            for rag_file in files:
                try:
                    file_id = rag_file.name.split("/")[-1]

                    file_info = {
                        "file_id": file_id,
                        "display_name": (
                            rag_file.display_name
                            if hasattr(rag_file, "display_name")
                            else ""
                        ),
                        "source_uri": (
                            rag_file.source_uri
                            if hasattr(rag_file, "source_uri")
                            else ""
                        ),
                        "create_time": (
                            str(rag_file.create_time)
                            if hasattr(rag_file, "create_time")
                            else ""
                        ),
                        "update_time": (
                            str(rag_file.update_time)
                            if hasattr(rag_file, "update_time")
                            else ""
                        ),
                    }

                    file_details.append(file_info)
                except Exception:
                    continue
        except Exception:
            pass

        return {
            "status": "success",
            "message": f"Successfully retrieved information for corpus '{corpus_display_name}'",
            "corpus_name": corpus_name,
            "corpus_display_name": corpus_display_name,
            "file_count": len(file_details),
            "files": file_details,
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error getting corpus information: {str(e)}",
            "corpus_name": corpus_name,
        }
