"""Project structure navigation."""

from pathlib import Path


def find_dbf_files(project_path: Path) -> dict[str, list[Path]]:
    """Find SYMLIST.DBF files in the project.

    Args:
        project_path: Path to the project directory

    Returns:
        Dictionary with 'symlist' key containing list of SYMLIST.DBF paths
    """
    symlist_files = list(project_path.rglob("SYMLIST.DBF"))
    return {"symlist": symlist_files}
