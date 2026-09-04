from langchain_core.tools import tool
from core.llm import llm


@tool
def list_files(path: str = ".") -> str:
    """List files and folders inside the given project directory."""

    return "files..."

@tool
def read_file(path: str) -> str:
    """Read and return the contents of a text file."""

    return "reading..."

@tool
def search_code(query: str, path: str = ".") -> str:
    """Search the project for code containing the given text."""

    return "searching..."

@tool
def project_tree(path: str = ".", depth: int = 2) -> str:
    """Show the directory structure up to the given depth."""

    return "tree..."




# tool binding



tools = [list_files,read_file,search_code,project_tree]

llm_with_tools = llm.bind_tools(tools)

result = llm_with_tools.invoke("list files in current working directory")

print(result)