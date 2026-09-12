from core.tools.filesReadOnly_Tools import (
    list_files,
    read_file,
    search_code,
    project_tree,
    find_file,
    file_info,
)
from core.tools.fileWrite_Tools import create_file, edit_file, create_directory, rename_file

tools = {
    "list_files": list_files,
    "read_file": read_file,
    "search_code": search_code,
    "project_tree": project_tree,
    "find_file": find_file,
    "file_info": file_info,
    "create_file":create_file,
    "edit_file":edit_file,
    "create_directory":create_directory,
    "rename_file":rename_file
}


def executeTool(tool_call):
    tool = tools[tool_call["name"]]
    return tool.invoke(tool_call)