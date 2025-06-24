"""
File and path manipulation utilities.
"""

import os
from pathlib import Path
from typing import Union, Optional
from ..config import ROOT_DIR, DATA_DIR


def resolve_data_path(filename: Union[str, Path]) -> str:
    """
    Resolve a filename to full path, checking data directory first.

    Args:
        filename: Filename or relative path

    Returns:
        str: Resolved absolute path

    Raises:
        FileNotFoundError: If file cannot be found
    """
    filename = str(filename)

    # If already absolute path, check if it exists
    if os.path.isabs(filename):
        if os.path.exists(filename):
            return filename
        else:
            raise FileNotFoundError(f"File not found: {filename}")

    # Try relative to current directory
    current_path = os.path.join(ROOT_DIR, filename)
    if os.path.exists(current_path):
        return current_path

    # Try in data directory
    data_path = os.path.join(DATA_DIR, filename)
    if os.path.exists(data_path):
        return data_path

    # Try in data subdirectories
    if os.path.exists(DATA_DIR):
        for root, dirs, files in os.walk(DATA_DIR):
            for file in files:
                if file == os.path.basename(filename):
                    return os.path.join(root, file)

    raise FileNotFoundError(f"File not found: {filename}")


def get_file_extension(filename: Union[str, Path]) -> str:
    """
    Get file extension from filename.

    Args:
        filename: File path or name

    Returns:
        str: File extension (lowercase, with dot)
    """
    return Path(filename).suffix.lower()


def ensure_directory_exists(directory_path: Union[str, Path]) -> bool:
    """
    Ensure a directory exists, create if necessary.

    Args:
        directory_path: Path to directory

    Returns:
        bool: True if directory exists or was created successfully
    """
    try:
        Path(directory_path).mkdir(parents=True, exist_ok=True)
        return True
    except (OSError, PermissionError):
        return False


def get_relative_path(file_path: Union[str, Path], base_path: Optional[Union[str, Path]] = None) -> str:
    """
    Get relative path from base directory.

    Args:
        file_path: File path to make relative
        base_path: Base directory (defaults to ROOT_DIR)

    Returns:
        str: Relative path
    """
    if base_path is None:
        base_path = ROOT_DIR

    try:
        return os.path.relpath(str(file_path), str(base_path))
    except ValueError:
        # If paths are on different drives (Windows), return absolute path
        return str(file_path)


def find_sample_files(extensions: list[str] = None) -> list[str]:
    """
    Find sample files in the data directory.

    Args:
        extensions: List of extensions to search for (defaults to supported formats)

    Returns:
        list: List of found file paths
    """
    if extensions is None:
        from ..config import SUPPORTED_FORMATS
        extensions = SUPPORTED_FORMATS

    found_files = []

    if not os.path.exists(DATA_DIR):
        return found_files

    for root, dirs, files in os.walk(DATA_DIR):
        for file in files:
            file_ext = get_file_extension(file)
            if file_ext in extensions:
                found_files.append(os.path.join(root, file))

    return sorted(found_files)