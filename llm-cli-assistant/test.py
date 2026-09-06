# from dotenv import load_dotenv
# load_dotenv()

# from langchain_core.tools import tool
# from langchain_core.messages import HumanMessage
# from core.llm import llm


# @tool
# def list_files(path: str = ".") -> str:
#     """List files and folders inside the given project directory."""

#     return "this is a dummy response to the tool call and for testing purpose only"

# @tool
# def read_file(path: str) -> str:
#     """Read and return the contents of a text file."""

#     return "reading..."

# @tool
# def search_code(query: str, path: str = ".") -> str:
#     """Search the project for code containing the given text."""

#     return "searching..."

# @tool
# def project_tree(path: str = ".", depth: int = 2) -> str:
#     """Show the directory structure up to the given depth."""

#     return "tree..."




# # tool binding



# tools = [list_files,read_file,search_code,project_tree]

# llm_with_tools = llm.bind_tools(tools)

# query = HumanMessage("list files in core directory and then show the project tree")

# messages = [ query ]

# result = llm_with_tools.invoke(messages)
# messages.append(result)

# # from pprint import pprint

# # pprint(result.model_dump())

# # print("\nTool Calls:\n")


# # tool executer:

# for tool_call in result.tool_calls:
#     # print(f"Tool Name: {tool_call['name']}")
#     # print(f"Arguments: {tool_call['args']}")
#     # print(f"Tool Call ID: {tool_call['id']}")
#     # print("-" * 40)

#     if tool_call['name'] == "list_files":
#         tool_message = list_files.invoke(tool_call["args"])
#         print(tool_message)
#         print("-" * 40)

#         messages.append(tool_message)

#     elif tool_call['name'] == "read_file":
#         messages.append(read_file.invoke(tool_call["args"]))
#     elif tool_call['name'] == "search_code":
#         messages.append(search_code.invoke(tool_call["args"]))
#     elif tool_call['name'] == "project_tree":
#         messages.append(project_tree.invoke(tool_call["args"]))



# result = llm_with_tools.invoke(messages)

# from pprint import pprint

# pprint(result.model_dump())


import os

path = "."

for root, dirs, files in os.walk(path):
    print("ROOT:", root)
    print("DIRS:", dirs)
    print("FILES:", files)
    print("-" * 50)