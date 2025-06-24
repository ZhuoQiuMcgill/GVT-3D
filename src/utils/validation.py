"""
Validation utilities for file paths, formats, and mesh data.
"""

import os
from pathlib import Path
from typing import Union, Optional
import pyvista as pv
from ..config import SUPPORTED_FORMATS


def validate_file_path(file_path: Union[str, Path]) -> bool:
    """
    Validate if a file path exists and is accessible.

    Args:
        file_path: Path to the file to validate

    Returns:
        bool: True if file exists and is readable, False otherwise
    """
    try:
        path = Path(file_path)
        return path.exists() and path.is_file() and os.access(path, os.R_OK)
    except (OSError, ValueError):
        return False


def validate_file_format(file_path: Union[str, Path]) -> bool:
    """
    Check if file format is supported by the application.

    Args:
        file_path: Path to the file to check

    Returns:
        bool: True if format is supported, False otherwise
    """
    try:
        extension = Path(file_path).suffix.lower()
        return extension in SUPPORTED_FORMATS
    except (AttributeError, ValueError):
        return False


def is_supported_format(extension: str) -> bool:
    """
    Check if a file extension is supported.

    Args:
        extension: File extension (with or without dot)

    Returns:
        bool: True if format is supported, False otherwise
    """
    if not extension.startswith('.'):
        extension = '.' + extension
    return extension.lower() in SUPPORTED_FORMATS


def validate_polydata(mesh: pv.PolyData) -> tuple[bool, Optional[str]]:
    """
    Validate PyVista PolyData object for basic integrity.

    Args:
        mesh: PyVista PolyData object to validate

    Returns:
        tuple: (is_valid, error_message)
    """
    if not isinstance(mesh, pv.PolyData):
        return False, "Object is not a PyVista PolyData instance"

    if mesh.n_points == 0:
        return False, "Mesh has no points"

    if mesh.n_cells == 0:
        return False, "Mesh has no cells"

    # Check for valid geometry
    try:
        bounds = mesh.bounds
        if any(b is None or not isinstance(b, (int, float)) for b in bounds):
            return False, "Invalid mesh bounds"
    except Exception as e:
        return False, f"Error accessing mesh bounds: {str(e)}"

    return True, None


def validate_mesh_for_visualization(mesh: pv.PolyData) -> tuple[bool, Optional[str]]:
    """
    Extended validation for mesh objects intended for visualization.

    Args:
        mesh: PyVista PolyData object to validate

    Returns:
        tuple: (is_valid, error_message)
    """
    # Basic validation first
    is_valid, error_msg = validate_polydata(mesh)
    if not is_valid:
        return is_valid, error_msg

    # Check for degenerate triangles or invalid topology
    try:
        if mesh.n_faces > 0:
            face_areas = mesh.compute_cell_sizes()['Area']
            if (face_areas <= 0).any():
                return False, "Mesh contains degenerate faces with zero or negative area"
    except Exception as e:
        return False, f"Error validating mesh topology: {str(e)}"

    return True, None