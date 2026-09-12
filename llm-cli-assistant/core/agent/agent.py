from core.tools.filesReadOnly_Tools import (
    list_files,
    read_file,
    search_code,
    project_tree,
    find_file,
    file_info,
)
from core.tools.fileWrite_Tools import create_file, edit_file, create_directory
from core.agent.tool_executor import executeTool

from core.llm import llm
from core.agent.context_manager import get_context

tools = [
    list_files,
    read_file,
    search_code,
    project_tree,
    find_file,
    file_info,
    create_file,
    edit_file,
    create_directory
]
llm_with_tools = llm.bind_tools(tools)

def run_agent(messages):

    while True:
        context_messages = get_context(messages)
        result = llm_with_tools.invoke(context_messages)

        messages.append(result)

        if not result.tool_calls:
            break

        for tool_call in result.tool_calls:

            tool_result = executeTool(tool_call)
            messages.append(tool_result)

    return result


    


    