from core.tools.filesReadOnly_Tools import (
    list_files,
    read_file,
    search_code,
    project_tree,
    find_file,
    file_info,
)
from core.tools.fileWrite_Tools import (
    create_file, 
    edit_file, 
    create_directory, 
    rename_file, 
    delete_file, 
    delete_directory,
    apply_patch
)

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
    "rename_file":rename_file,
    "delete_file":delete_file,
    "delete_directory":delete_directory,
    "apply_patch":apply_patch
}


from core.logger import logger


def executeTool(tool_call):

    tool_name = tool_call["name"]

    logger.info(
        f"Tool call started | tool={tool_name}"
    )

    tool = tools.get(tool_name)

    if tool is None:
        logger.error(
            f"Unknown tool requested | tool={tool_name}"
        )

        return f"Error: Unknown tool '{tool_name}'."

    try:
        result = tool.invoke(tool_call)

        logger.info(
            f"Tool call completed | tool={tool_name}"
        )

        return result

    except Exception as e:

        logger.exception(
            f"Tool call failed | tool={tool_name} | error={e}"
        )

        raise