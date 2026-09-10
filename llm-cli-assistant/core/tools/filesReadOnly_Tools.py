from langchain_core.tools import tool
from datetime import datetime

import os

IGNORED_DIRS = {
    ".git",
    ".env",
    ".venv",
    "__pycache__",
    "node_modules",
}

@tool
def list_files(path: str = ".") -> str:
    # docstring

    """
    List the immediate contents of a directory.

    Use this tool when you need to inspect what files and directories
    exist directly inside a specific directory.

    This tool is for directory inspection, not recursive file searching.
    Use find_file when you know the exact filename but do not know where
    it is located.


    Use this tool when you need to:
    - inspect the contents of a directory
    - discover project files and folders
    - determine the project structure
    - find likely configuration, source, or documentation files
    - decide which files or directories to inspect next

    This tool lists only the immediate contents of the specified directory.
    It does not recursively inspect subdirectories.

    Use project_tree when you need to understand the recursive project
    structure. Use read_file when you need the contents of a specific file.
    """

    if not os.path.exists(path):
        return f"Error: Path '{path}' does not exist."

    if not os.path.isdir(path):
        return f"Error: '{path}' is not a directory."

    try:
        items = [
            item for item in os.listdir(path)
            if item not in IGNORED_DIRS
        ]

        if not items:
            return f"The directory '{path}' is empty."

        return "\n".join(items)

    except Exception as e:
        return f"Error reading directory: {str(e)}"

@tool
def read_file(path: str) -> str:
    # docstring

    """
    Read the contents of a text-based project file.

    Use this tool when you need to:
    - inspect the implementation of a function, class, or component
    - understand a configuration file
    - examine code surrounding a search result
    - investigate how a feature is implemented
    - gather detailed context from a specific file

    The path must point to a file, not a directory.

    Prefer search_code first when you do not know which file contains
    the relevant code. After search_code identifies relevant files,
    use read_file to inspect the necessary file contents.

    Do not use this tool to discover files or directories; use list_files
    or project_tree for that.
    """

    if not os.path.exists(path):
         return f"Error: File '{path}' does not exist."
    
    if not os.path.isfile(path):
         return f"Error:'{path}' is not a file."

    try:
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()

        return content

    except UnicodeDecodeError:
        return f"Error: '{path}' is not a readable text file."

    except Exception as e:
        return f"Error reading file: {str(e)}"
    
    

@tool
def search_code(
    query: str,
    path: str = ".",
    ignore_dirs: list[str] | None = None
) -> str:

    #   
    
    """
    Search project source and text files for a case-insensitive text match.

    Use this tool when you need to locate:
    - functions, classes, methods, variables, or imports
    - routes, endpoints, components, or configuration keys
    - where a specific identifier or text appears
    - files related to a feature, error, or implementation detail

    Returns matching file paths, line numbers, and matching lines.

    The search automatically excludes protected, dependency, and generated
    directories. Additional irrelevant directories may be supplied through
    ignore_dirs.

    This is a text-based search and does not understand code semantics.
    After finding relevant files, use read_file to inspect their contents
    when additional context is required.

    Use project_tree when you first need to understand the overall project
    structure rather than search for a specific piece of code.
    """

    if not os.path.exists(path):
        return f"Error: Path '{path}' does not exist."

    if not os.path.isdir(path):
        return f"Error: '{path}' is not a directory."


    user_ignored_dirs = set(ignore_dirs or [])
    ignored_dirs = IGNORED_DIRS | user_ignored_dirs


    results = []

    for root, dirs, files in os.walk(path):

        dirs[:] = [
            directory
            for directory in dirs
            if directory not in ignored_dirs
        ]

        for filename in files:
            file_path = os.path.join(root, filename)

            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    for line_number, line in enumerate(file, start=1):

                        if query.lower() in line.lower():
                            results.append(
                                f"{file_path}:{line_number}\n{line.strip()}"
                            )

                            if len(results) >= 50:
                                return "\n\n".join(results)

            except (UnicodeDecodeError, PermissionError):
                continue

            except Exception:
                continue

    if not results:
        return f"No matches found for '{query}'."

    return "\n\n".join(results)    


@tool
def project_tree(path: str = ".", depth: int = 2) -> str:
    """
    Display the hierarchical structure of files and directories in a project.

    Use this tool when you need to:
    - understand the overall project structure
    - discover how files and directories are organized
    - identify important source, configuration, or documentation files
    - inspect a project before searching or reading specific files

    The depth parameter controls how many directory levels are displayed.

    Automatically skips protected, dependency, and generated directories.

    This tool returns only the project structure and does not return file
    contents.
    """

    if not os.path.exists(path):
        return f"Error: Path '{path}' does not exist."

    if not os.path.isdir(path):
        return f"Error: '{path}' is not a directory."

    if depth < 0:
        return "Error: Depth cannot be negative."

    tree = []

    root_name = os.path.basename(os.path.abspath(path))
    tree.append(f"{root_name}/")

    def build_tree(current_path, prefix="", current_depth=0):

        if current_depth >= depth:
            return

        try:
            items = sorted(os.listdir(current_path))

        except PermissionError:
            return

        # Remove ignored directories
        items = [
            item for item in items
            if not (
                os.path.isdir(os.path.join(current_path, item))
                and item in IGNORED_DIRS
            )
        ]

        for index, item in enumerate(items):

            item_path = os.path.join(current_path, item)

            is_last = index == len(items) - 1

            connector = "└── " if is_last else "├── "

            if os.path.isdir(item_path):

                tree.append(
                    f"{prefix}{connector}{item}/"
                )

                extension = "    " if is_last else "│   "

                build_tree(
                    item_path,
                    prefix + extension,
                    current_depth + 1
                )

            else:

                tree.append(
                    f"{prefix}{connector}{item}"
                )

    build_tree(path)

    return "\n".join(tree)

@tool
def find_file(filename: str, path: str = ".") -> str:
    """
    Find files by exact filename within a project directory.

    Use this tool when you know the exact name of a file but do not know
    where it is located in the project.

    The search recursively checks subdirectories while skipping protected,
    dependency, and generated directories.

    This tool searches for files only and does not return directories.

    Args:
        filename: Exact filename to search for, including its extension
            when applicable.
        path: Directory from which the recursive search should begin.

    Returns:
        Matching file paths, or a message if no matching file is found.
    """

    if not filename:
        return "Error: Filename cannot be empty."

    if not os.path.exists(path):
        return f"Error: Path '{path}' does not exist."

    if not os.path.isdir(path):
        return f"Error: Path '{path}' is not a directory."

    results = []

    for root, dirs, files in os.walk(path):

        dirs[:] = [
            directory
            for directory in dirs
            if directory not in IGNORED_DIRS
        ]

        for file in files:
            if file == filename:
                results.append(os.path.join(root, file))

                if len(results) >= 50:
                    return "\n".join(results)

    if not results:
        return f"No file named '{filename}' found."

    return "\n".join(results)


@tool
def file_info(path: str) -> str:
    """
    Get metadata about a specific file without reading its contents.

    Use this tool when you need to inspect a file's properties, such as
    its name, path, type, size, or last modification time.

    The path must point to an existing file, not a directory.

    Args:
        path: Path to the file whose metadata should be inspected.

    Returns:
        A formatted summary containing the file name, path, type, size,
        and last modification time. Returns an error message if the path
        does not exist, is not a file, or cannot be accessed.
    """

    if not os.path.exists(path):
        return f"Error: File '{path}' does not exist."

    if not os.path.isfile(path):
        return f"Error: '{path}' is not a file."

    try:
        file_name = os.path.basename(path)
        file_size = os.path.getsize(path)
        modified_time = datetime.fromtimestamp(
            os.path.getmtime(path)
        ).strftime("%Y-%m-%d %H:%M:%S")

        file_extension = os.path.splitext(file_name)[1]

        if file_extension:
            file_type = f"{file_extension[1:].upper()} file"
        else:
            file_type = "Unknown file type"

        return (
            f"Name: {file_name}\n"
            f"Path: {path}\n"
            f"Type: {file_type}\n"
            f"Size: {file_size} bytes\n"
            f"Last modified: {modified_time}"
        )

    except PermissionError:
        return f"Error: Permission denied for '{path}'."

    except Exception as e:
        return f"Error getting file information: {str(e)}"