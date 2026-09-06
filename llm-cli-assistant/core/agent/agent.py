from core.tools.filesReadOnly_Tools import list_files, read_file, search_code, project_tree
from core.agent.tool_executor import executeTool

from core.llm import llm

tools = [list_files,read_file,search_code,project_tree]
llm_with_tools = llm.bind_tools(tools)

def run_agent(messages):

    while True:
        result = llm_with_tools.invoke(messages)

        messages.append(result)

        if not result.tool_calls:
            break

        for tool_call in result.tool_calls:

            tool_result = executeTool(tool_call)
            messages.append(tool_result)

    return result


    


    