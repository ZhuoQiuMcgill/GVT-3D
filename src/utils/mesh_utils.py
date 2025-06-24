"""
Mesh processing and manipulation utilities.
"""

import numpy as np
import pyvista as pv
from typing import Dict, Any, Optional


def get_mesh_info(mesh: pv.PolyData) -> Dict[str, Any]:
    """
    Extract comprehensive information about a mesh.

    Args:
        mesh: PyVista PolyData object

    Returns:
        dict: Dictionary containing mesh information
    """
    # Use n_faces_strict if available, otherwise fall back to n_cells for face count
    try:
        n_faces = mesh.n_faces_strict
    except AttributeError:
        # Fallback for older PyVista versions or when n_faces_strict is not available
        n_faces = mesh.n_cells

    info = {
        'n_points': mesh.n_points,
        'n_cells': mesh.n_cells,
        'n_faces': n_faces,
        'bounds': mesh.bounds,
        'center': mesh.center,
        'volume': 0.0,
        'surface_area': 0.0,
        'is_manifold': False,
        'has_normals': False,
        'point_arrays': list(mesh.point_data.keys()),
        'cell_arrays': list(mesh.cell_data.keys())
    }

    try:
        # Calculate volume if mesh is closed
        if mesh.is_all_triangles and mesh.n_open_edges == 0:
            info['volume'] = mesh.volume
            info['is_manifold'] = True

        # Calculate surface area
        mesh_with_areas = mesh.compute_cell_sizes()
        if 'Area' in mesh_with_areas.cell_data:
            info['surface_area'] = mesh_with_areas.cell_data['Area'].sum()

        # Check for normals
        info['has_normals'] = 'Normals' in mesh.point_data

    except Exception:
        # If any calculation fails, continue with basic info
        pass

    return info


def center_mesh(mesh: pv.PolyData, center_point: Optional[np.ndarray] = None) -> pv.PolyData:
    """
    Center a mesh at origin or specified point.

    Args:
        mesh: PyVista PolyData object
        center_point: Target center point (defaults to origin)

    Returns:
        pv.PolyData: Centered mesh (new copy)
    """
    if center_point is None:
        center_point = np.array([0.0, 0.0, 0.0])

    mesh_copy = mesh.copy()
    current_center = mesh_copy.center
    translation = center_point - current_center
    mesh_copy.translate(translation)

    return mesh_copy


def normalize_mesh_scale(mesh: pv.PolyData, target_size: float = 1.0) -> pv.PolyData:
    """
    Normalize mesh to fit within a target bounding box size.

    Args:
        mesh: PyVista PolyData object
        target_size: Target maximum dimension

    Returns:
        pv.PolyData: Scaled mesh (new copy)
    """
    mesh_copy = mesh.copy()
    bounds = mesh_copy.bounds

    # Calculate current maximum dimension
    current_size = max(
        bounds[1] - bounds[0],  # x-range
        bounds[3] - bounds[2],  # y-range
        bounds[5] - bounds[4]  # z-range
    )

    if current_size > 0:
        scale_factor = target_size / current_size
        mesh_copy.scale(scale_factor)

    return mesh_copy


def ensure_mesh_normals(mesh: pv.PolyData, force_recompute: bool = False) -> pv.PolyData:
    """
    Ensure mesh has point normals, computing them if necessary.

    Args:
        mesh: PyVista PolyData object
        force_recompute: Force recomputation even if normals exist

    Returns:
        pv.PolyData: Mesh with normals (new copy)
    """
    mesh_copy = mesh.copy()

    if force_recompute or 'Normals' not in mesh_copy.point_data:
        mesh_copy = mesh_copy.compute_normals(
            cell_normals=False,
            point_normals=True,
            split_vertices=False,
            flip_normals=False
        )

    return mesh_copy


def prepare_mesh_for_visualization(mesh: pv.PolyData,
                                   center: bool = True,
                                   normalize_scale: bool = True,
                                   ensure_normals: bool = True,
                                   target_size: float = 10.0) -> pv.PolyData:
    """
    Prepare mesh for optimal visualization.

    Args:
        mesh: PyVista PolyData object
        center: Whether to center the mesh
        normalize_scale: Whether to normalize mesh scale
        ensure_normals: Whether to ensure normals exist
        target_size: Target size for normalization

    Returns:
        pv.PolyData: Processed mesh ready for visualization
    """
    processed_mesh = mesh.copy()

    # Center mesh
    if center:
        processed_mesh = center_mesh(processed_mesh)

    # Normalize scale
    if normalize_scale:
        processed_mesh = normalize_mesh_scale(processed_mesh, target_size)

    # Ensure normals
    if ensure_normals:
        processed_mesh = ensure_mesh_normals(processed_mesh)

    return processed_mesh


def get_mesh_statistics(mesh: pv.PolyData) -> Dict[str, float]:
    """
    Calculate statistical properties of mesh geometry.

    Args:
        mesh: PyVista PolyData object

    Returns:
        dict: Dictionary of statistical measures
    """
    points = mesh.points

    stats = {
        'min_x': float(np.min(points[:, 0])),
        'max_x': float(np.max(points[:, 0])),
        'min_y': float(np.min(points[:, 1])),
        'max_y': float(np.max(points[:, 1])),
        'min_z': float(np.min(points[:, 2])),
        'max_z': float(np.max(points[:, 2])),
        'mean_x': float(np.mean(points[:, 0])),
        'mean_y': float(np.mean(points[:, 1])),
        'mean_z': float(np.mean(points[:, 2])),
        'std_x': float(np.std(points[:, 0])),
        'std_y': float(np.std(points[:, 1])),
        'std_z': float(np.std(points[:, 2]))
    }

    # Calculate ranges
    stats['range_x'] = stats['max_x'] - stats['min_x']
    stats['range_y'] = stats['max_y'] - stats['min_y']
    stats['range_z'] = stats['max_z'] - stats['min_z']
    stats['max_range'] = max(stats['range_x'], stats['range_y'], stats['range_z'])

    return stats
