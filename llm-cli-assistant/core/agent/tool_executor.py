from core.tools.filesReadOnly_Tools import (
    list_files,
    read_file,
    search_code,
    project_tree,
    find_file,
    file_info,
)

tools = {
    "list_files": list_files,
    "read_file": read_file,
    "search_code": search_code,
    "project_tree": project_tree,
    "find_file": find_file,
    "file_info": file_info,
}


def executeTool(tool_call):
    tool = tools[tool_call["name"]]
    return tool.invoke(tool_call)