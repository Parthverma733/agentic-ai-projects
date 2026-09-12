from langchain_core.tools import tool
from core.path_util import safe_path

import os


@tool
def create_file(path: str, content: str) -> str:
    """
    Create a new file with the specified content.

    Use this tool when the user explicitly asks you to create a new file.

    The file must be created inside the project directory.
    Parent directories are created automatically if they do not already exist.

    This tool should not be used to modify an existing file.

    Args:
        path: Path of the file to create.
        content: Content to write into the new file.

    Returns:
        A success message if the file was created, or an error message
        if the operation failed.
    """

    if not path:
        return "Error: File path cannot be empty."

    try:
        target = safe_path(path)

        if target.exists():
            return f"Error: File or directory '{path}' already exists."

        parent_directory = target.parent

        if parent_directory:
            os.makedirs(parent_directory, exist_ok=True)

        with open(target, "w", encoding="utf-8") as file:
            file.write(content)

        return f"File created successfully: {target}"

    except ValueError as e:
        return f"Error: {str(e)}"

    except PermissionError:
        return f"Error: Permission denied when creating '{path}'."

    except Exception as e:
        return f"Error creating file: {str(e)}"



@tool
def edit_file(path: str, old_text: str, new_text: str) -> str:
    """
    Edit an existing file by replacing exactly one occurrence
    of old_text with new_text.

    The file must already exist and must be inside the project directory.
    """

    if not path:
        return "Error: File path cannot be empty."

    if not old_text:
        return "Error: old_text cannot be empty."

    try:
        target = safe_path(path)

        if not target.exists():
            return f"Error: File '{path}' does not exist."

        if not target.is_file():
            return f"Error: '{path}' is not a file."

        with open(target, "r", encoding="utf-8") as file:
            content = file.read()

        match_count = content.count(old_text)

        if match_count == 0:
            return "Error: old_text was not found in the file."

        if match_count > 1:
            return (
                f"Error: old_text was found {match_count} times. "
                "Edit cancelled to avoid modifying the wrong location."
            )

        updated_content = content.replace(old_text, new_text, 1)

        with open(target, "w", encoding="utf-8") as file:
            file.write(updated_content)

        return f"File edited successfully: {target}"

    except ValueError as e:
        return f"Error: {str(e)}"

    except PermissionError:
        return f"Error: Permission denied when editing '{path}'."

    except Exception as e:
        return f"Error editing file: {str(e)}"

@tool
def create_directory(path: str) -> str:
    """
    Create a new directory inside the project directory.

    Parent directories are created automatically if needed.
    """

    if not path:
        return "Error: Directory path cannot be empty."

    try:
        target = safe_path(path)

        if target.exists():
            return f"Error: File or directory '{path}' already exists."

        target.mkdir(parents=True, exist_ok=False)

        return f"Directory created successfully: {target}"

    except ValueError as e:
        return f"Error: {str(e)}"

    except PermissionError:
        return f"Error: Permission denied when creating '{path}'."

    except Exception as e:
        return f"Error creating directory: {str(e)}"


@tool
def rename_file(path: str, new_path: str) -> str:
    """
    Rename or move an existing file inside the project directory.

    Both the source and destination must remain inside the project directory.
    The destination must not already exist.
    """

    if not path:
        return "Error: Source path cannot be empty."

    if not new_path:
        return "Error: Destination path cannot be empty."

    try:
        source = safe_path(path)
        destination = safe_path(new_path)

        if not source.exists():
            return f"Error: File '{path}' does not exist."

        if not source.is_file():
            return f"Error: '{path}' is not a file."

        if destination.exists():
            return f"Error: File or directory '{new_path}' already exists."

        destination.parent.mkdir(parents=True, exist_ok=True)

        source.rename(destination)

        return f"File renamed successfully: {source} → {destination}"

    except ValueError as e:
        return f"Error: {str(e)}"

    except PermissionError:
        return f"Error: Permission denied when renaming '{path}'."

    except Exception as e:
        return f"Error renaming file: {str(e)}"