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

    Use this tool when the user explicitly asks to create a folder
    or directory.

    The directory path must remain inside the project directory.
    Parent directories are created automatically if they do not exist.

    This tool should not be used to create files.

    Args:
        path: Path of the directory to create.

    Returns:
        A success message if the directory was created, or an error
        message if the operation failed.
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
    Rename or move an existing file within the project directory.

    Use this tool when the user explicitly asks to rename a file
    or move a file to another location inside the project.

    Both the source and destination paths must remain inside the
    project directory.

    The destination must not already exist. Parent directories of
    the destination are created automatically if necessary.

    This tool should not be used to modify the contents of a file.

    Args:
        path: Current path of the file.
        new_path: New path for the file.

    Returns:
        A success message if the file was renamed or moved, or an
        error message if the operation failed.
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


@tool
def delete_file(path: str) -> str:
    """
    Delete an existing file inside the project directory.

    Use this tool only when the user explicitly asks to delete a file.

    The file must exist and must be located inside the project directory.
    Directories cannot be deleted by this tool.

    This operation is destructive and cannot be undone automatically.

    Args:
        path: Path of the file to delete.

    Returns:
        A success message if the file was deleted, or an error message
        if the operation failed.
    """

    if not path:
        return "Error: File path cannot be empty."

    try:
        target = safe_path(path)

        if not target.exists():
            return f"Error: File '{path}' does not exist."

        if not target.is_file():
            return f"Error: '{path}' is not a file."

        target.unlink()

        return f"File deleted successfully: {target}"

    except ValueError as e:
        return f"Error: {str(e)}"

    except PermissionError:
        return f"Error: Permission denied when deleting '{path}'."

    except Exception as e:
        return f"Error deleting file: {str(e)}"



@tool
def delete_directory(path: str) -> str:
    """
    Delete an empty directory inside the project directory.

    Use this tool only when the user explicitly asks to delete a directory.

    The directory must exist, must be inside the project directory,
    and must be empty.

    Non-empty directories are not deleted by this tool.
    """

    if not path:
        return "Error: Directory path cannot be empty."

    try:
        target = safe_path(path)

        if not target.exists():
            return f"Error: Directory '{path}' does not exist."

        if not target.is_dir():
            return f"Error: '{path}' is not a directory."

        target.rmdir()

        return f"Directory deleted successfully: {target}"

    except ValueError as e:
        return f"Error: {str(e)}"

    except OSError:
        return (
            f"Error: Directory '{path}' is not empty "
            "or could not be deleted."
        )

    except PermissionError:
        return f"Error: Permission denied when deleting '{path}'."

    except Exception as e:
        return f"Error deleting directory: {str(e)}"

@tool
def apply_patch(path: str, patch: str) -> str:
    """
    Apply a unified diff patch to an existing file.

    The file must exist inside the project directory.
    The patch is validated before the modified content is written.
    """

    if not path:
        return "Error: File path cannot be empty."

    if not patch:
        return "Error: Patch cannot be empty."

    try:
        target = safe_path(path)

        if not target.exists():
            return f"Error: File '{path}' does not exist."

        if not target.is_file():
            return f"Error: '{path}' is not a file."

        with open(target, "r", encoding="utf-8") as file:
            original_content = file.read()

        original_lines = original_content.splitlines(keepends=True)
        patch_lines = patch.splitlines()

        if len(patch_lines) < 3:
            return "Error: Invalid patch."

        # Remove optional file headers.
        patch_body = []

        for line in patch_lines:
            if line.startswith("--- ") or line.startswith("+++ "):
                continue

            patch_body.append(line)

        modified_lines = original_lines.copy()

        # Process hunks from bottom to top so line positions
        # remain valid while applying changes.
        hunks = []
        current_hunk = []

        for line in patch_body:
            if line.startswith("@@"):
                if current_hunk:
                    hunks.append(current_hunk)

                current_hunk = [line]

            elif current_hunk:
                current_hunk.append(line)

        if current_hunk:
            hunks.append(current_hunk)

        if not hunks:
            return "Error: No valid patch hunks found."

        for hunk in reversed(hunks):
            header = hunk[0]

            try:
                old_start = int(header.split("-")[1].split(",")[0])
            except (IndexError, ValueError):
                return f"Error: Invalid hunk header: {header}"

            index = old_start - 1

            expected = []
            additions = []

            for line in hunk[1:]:
                if line.startswith(" "):
                    expected.append(line[1:])
                    additions.append(line[1:])

                elif line.startswith("-"):
                    expected.append(line[1:])

                elif line.startswith("+"):
                    additions.append(line[1:])

                elif line == r"\ No newline at end of file":
                    continue

                else:
                    return f"Error: Invalid patch line: {line}"

            actual = modified_lines[index:index + len(expected)]

            if actual != expected:
                return (
                    f"Error: Patch does not match current contents "
                    f"of '{path}'."
                )

            modified_lines[index:index + len(expected)] = additions

        updated_content = "".join(modified_lines)

        with open(target, "w", encoding="utf-8") as file:
            file.write(updated_content)

        return f"Patch applied successfully: {target}"

    except ValueError as e:
        return f"Error: {str(e)}"

    except PermissionError:
        return f"Error: Permission denied when patching '{path}'."

    except Exception as e:
        return f"Error applying patch: {str(e)}"