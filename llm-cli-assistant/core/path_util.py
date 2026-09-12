from pathlib import Path


PROJECT_ROOT = Path.cwd().resolve()


def safe_path(path: str) -> Path:
    """
    Resolve a path and ensure it stays inside the project directory.
    """

    if not path:
        raise ValueError("Path cannot be empty.")

    target = Path(path).resolve()

    try:
        target.relative_to(PROJECT_ROOT)
    except ValueError:
        raise ValueError(
            f"Access denied: path must remain inside the project directory."
        )

    return target