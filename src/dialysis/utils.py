from pathlib import Path

from typing import List

HERE_MARKERS = ('.git', 'README.md', '.gitignore', '.here')

def here(markers: List[str] = HERE_MARKERS) -> Path:
    """
    Find the root of a project by looking for certain marker files

    Args:
        markers: The list of files to look for in parent directoreis

    Returns:
        The root directory
    """
    curdir = Path.cwd()
    prevdir = None
    while curdir != prevdir:
        if any((curdir / filename).exists() for filename in markers):
            return curdir
        prevdir = curdir
        curdir = curdir.parent

    raise ValueError("No root path found")