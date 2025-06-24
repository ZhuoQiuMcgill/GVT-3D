"""
File importing and preprocessing module for GVT.
Handles loading of .vtk, .obj, and other supported 3D model formats.
"""

import os
from pathlib import Path
from typing import Union, Optional, Tuple
import pyvista as pv

from ..config import VERBOSE_LOADING, DEBUG_MODE
from ..utils import (
    validate_file_path,
    validate_file_format,
    validate_polydata,
    resolve_data_path,
    get_file_extension,
    prepare_mesh_for_visualization,
    get_mesh_info
)


class MeshImporter:
    """
    Handles importing and preprocessing of 3D mesh files.
    """

    def __init__(self, verbose: bool = VERBOSE_LOADING):
        """
        Initialize the mesh importer.

        Args:
            verbose: Enable verbose output during loading
        """
        self.verbose = verbose
        self._last_loaded_info = {}

    def load_mesh(self,
                  file_path: Union[str, Path],
                  preprocess: bool = True,
                  auto_center: bool = True,
                  auto_scale: bool = True) -> pv.PolyData:
        """
        Load a mesh file and return PyVista PolyData.

        Args:
            file_path: Path to the mesh file
            preprocess: Apply preprocessing for visualization
            auto_center: Center the mesh at origin
            auto_scale: Normalize mesh scale

        Returns:
            pv.PolyData: Loaded mesh data

        Raises:
            FileNotFoundError: If file cannot be found
            ValueError: If file format is not supported or mesh is invalid
            RuntimeError: If loading fails
        """
        try:
            # Resolve file path
            resolved_path = resolve_data_path(file_path)

            if self.verbose:
                print(f"Loading mesh from: {resolved_path}")

            # Validate file
            if not validate_file_path(resolved_path):
                raise FileNotFoundError(f"Cannot access file: {resolved_path}")

            if not validate_file_format(resolved_path):
                extension = get_file_extension(resolved_path)
                raise ValueError(f"Unsupported file format: {extension}")

            # Load mesh based on file extension
            mesh = self._load_by_extension(resolved_path)

            # Validate loaded mesh
            is_valid, error_msg = validate_polydata(mesh)
            if not is_valid:
                raise ValueError(f"Invalid mesh data: {error_msg}")

            # Store mesh information
            self._last_loaded_info = get_mesh_info(mesh)

            if self.verbose:
                self._print_mesh_info(self._last_loaded_info)

            # Apply preprocessing if requested
            if preprocess:
                mesh = prepare_mesh_for_visualization(
                    mesh,
                    center=auto_center,
                    normalize_scale=auto_scale,
                    ensure_normals=True
                )

                if self.verbose:
                    print("Applied preprocessing: centering, scaling, normals computation")

            return mesh

        except Exception as e:
            if DEBUG_MODE:
                import traceback
                traceback.print_exc()
            raise RuntimeError(f"Failed to load mesh: {str(e)}") from e

    def _load_by_extension(self, file_path: str) -> pv.PolyData:
        """
        Load mesh file based on its extension.

        Args:
            file_path: Validated file path

        Returns:
            pv.PolyData: Loaded mesh

        Raises:
            ValueError: If file format is not supported
            RuntimeError: If loading fails
        """
        extension = get_file_extension(file_path)

        try:
            if extension == '.vtk':
                mesh = pv.read(file_path)
            elif extension == '.obj':
                mesh = pv.read(file_path)
            elif extension == '.ply':
                mesh = pv.read(file_path)
            elif extension == '.stl':
                mesh = pv.read(file_path)
            else:
                raise ValueError(f"Unsupported format: {extension}")

            # Ensure we have PolyData
            if not isinstance(mesh, pv.PolyData):
                if hasattr(mesh, 'extract_surface'):
                    mesh = mesh.extract_surface()
                else:
                    # Try to convert to PolyData
                    mesh = pv.PolyData(mesh.points, mesh.cells)

            return mesh

        except Exception as e:
            raise RuntimeError(f"Failed to load {extension} file: {str(e)}") from e

    def _print_mesh_info(self, info: dict) -> None:
        """
        Print mesh information in a formatted way.

        Args:
            info: Mesh information dictionary
        """
        print(f"Mesh loaded successfully:")
        print(f"  Points: {info['n_points']:,}")
        print(f"  Cells: {info['n_cells']:,}")
        print(f"  Faces: {info['n_faces']:,}")
        print(f"  Center: ({info['center'][0]:.2f}, {info['center'][1]:.2f}, {info['center'][2]:.2f})")

        if info['surface_area'] > 0:
            print(f"  Surface Area: {info['surface_area']:.2f}")

        if info['volume'] > 0:
            print(f"  Volume: {info['volume']:.2f}")

        if info['point_arrays']:
            print(f"  Point Arrays: {', '.join(info['point_arrays'])}")

        if info['cell_arrays']:
            print(f"  Cell Arrays: {', '.join(info['cell_arrays'])}")

    def get_last_loaded_info(self) -> dict:
        """
        Get information about the last loaded mesh.

        Returns:
            dict: Mesh information dictionary
        """
        return self._last_loaded_info.copy()

    def can_load_file(self, file_path: Union[str, Path]) -> Tuple[bool, str]:
        """
        Check if a file can be loaded without actually loading it.

        Args:
            file_path: Path to check

        Returns:
            tuple: (can_load, reason)
        """
        try:
            resolved_path = resolve_data_path(file_path)

            if not validate_file_path(resolved_path):
                return False, "File not found or not accessible"

            if not validate_file_format(resolved_path):
                extension = get_file_extension(resolved_path)
                return False, f"Unsupported format: {extension}"

            return True, "File can be loaded"

        except FileNotFoundError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Error checking file: {str(e)}"

    @staticmethod
    def get_supported_formats() -> list[str]:
        """
        Get list of supported file formats.

        Returns:
            list: Supported file extensions
        """
        from ..config import SUPPORTED_FORMATS
        return SUPPORTED_FORMATS.copy()