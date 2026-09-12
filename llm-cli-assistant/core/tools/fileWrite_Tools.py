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