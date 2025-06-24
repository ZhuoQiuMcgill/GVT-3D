"""
3D visualization and interaction module for GVT.
Manages PyVista plotting and user interactions like point picking.
"""

from typing import Optional, Callable, Any, Dict
import numpy as np
import pyvista as pv

from ..config import (
    WINDOW_TITLE, DEFAULT_WINDOW_SIZE, BACKGROUND_COLOR,
    MESH_COLOR, MESH_OPACITY, MESH_SPECULAR, MESH_SPECULAR_POWER,
    PICKING_ENABLED, PICKING_LABEL_COLOR, PICKING_LABEL_FONT_SIZE,
    PICKING_POINT_SIZE, PICKING_POINT_COLOR,
    AUTO_CAMERA_RESET, LIGHTING_ENABLED, AMBIENT_LIGHT, DIFFUSE_LIGHT,
    USE_DEPTH_PEELING, ANTI_ALIASING, SMOOTH_SHADING,
    SHOW_EDGES, EDGE_COLOR
)


class MeshVisualizer:
    """
    Handles 3D mesh visualization and user interaction using PyVista.
    """

    def __init__(self):
        """Initialize the mesh visualizer."""
        self.plotter = None
        self.current_mesh = None
        self.mesh_actor = None
        self.picking_enabled = PICKING_ENABLED
        self.pick_callback = None
        self._picked_points = []
        self._pick_labels = []
        self._setup_plotter()

    def _setup_plotter(self) -> None:
        """Set up the PyVista plotter with default configuration."""
        # Create plotter - for PyVista 0.45.2, use default lighting unless specifically disabled
        if LIGHTING_ENABLED:
            self.plotter = pv.Plotter(
                window_size=DEFAULT_WINDOW_SIZE,
                title=WINDOW_TITLE
            )
        else:
            self.plotter = pv.Plotter(
                window_size=DEFAULT_WINDOW_SIZE,
                title=WINDOW_TITLE,
                lighting='none'
            )

        # Configure plotter settings
        self.plotter.background_color = BACKGROUND_COLOR

        # Enable optional features
        if USE_DEPTH_PEELING:
            self.plotter.enable_depth_peeling()

        if ANTI_ALIASING:
            self.plotter.enable_anti_aliasing()

        # Setup custom lighting if needed (PyVista 0.45.2 syntax)
        if LIGHTING_ENABLED and (AMBIENT_LIGHT != 0.3 or DIFFUSE_LIGHT != 0.7):
            # Only modify lighting if we want non-default values
            # Remove default lights
            self.plotter.remove_all_lights()

            # Add main directional light
            main_light = pv.Light(
                position=(10, 10, 10),
                focal_point=(0, 0, 0),
                light_type='scene light'
            )
            main_light.intensity = DIFFUSE_LIGHT
            self.plotter.add_light(main_light)

            # Add softer ambient-like lighting from different directions
            if AMBIENT_LIGHT > 0:
                ambient_positions = [(-5, 5, 5), (5, -5, 5), (-5, -5, -5)]
                for pos in ambient_positions:
                    ambient_light = pv.Light(
                        position=pos,
                        focal_point=(0, 0, 0),
                        light_type='scene light'
                    )
                    ambient_light.intensity = AMBIENT_LIGHT * 0.4
                    self.plotter.add_light(ambient_light)

        # Enable picking if configured
        if self.picking_enabled:
            self.plotter.enable_point_picking(
                callback=self._point_pick_callback,
                show_point=True,
                point_size=PICKING_POINT_SIZE,
                color=PICKING_POINT_COLOR,
                show_message=False
            )

    def add_mesh(self,
                 mesh: pv.PolyData,
                 color: str = MESH_COLOR,
                 opacity: float = MESH_OPACITY,
                 show_edges: bool = SHOW_EDGES,
                 reset_camera: bool = AUTO_CAMERA_RESET,
                 **kwargs) -> Any:
        """
        Add a mesh to the visualization.

        Args:
            mesh: PyVista PolyData to visualize
            color: Mesh color
            opacity: Mesh opacity (0-1)
            show_edges: Whether to show mesh edges
            reset_camera: Whether to reset camera to fit mesh
            **kwargs: Additional arguments for plotter.add_mesh()

        Returns:
            Mesh actor reference
        """
        if self.plotter is None:
            self._setup_plotter()

        # Store current mesh
        self.current_mesh = mesh

        # Set up mesh properties
        mesh_kwargs = {
            'color': color,
            'opacity': opacity,
            'show_edges': show_edges,
            'smooth_shading': SMOOTH_SHADING,
            'specular': MESH_SPECULAR,
            'specular_power': MESH_SPECULAR_POWER,
        }

        if show_edges:
            mesh_kwargs['edge_color'] = EDGE_COLOR

        # Merge with user-provided kwargs
        mesh_kwargs.update(kwargs)

        # Add mesh to plotter
        self.mesh_actor = self.plotter.add_mesh(mesh, **mesh_kwargs)

        # Reset camera if requested
        if reset_camera:
            self.plotter.reset_camera()

        return self.mesh_actor

    def _point_pick_callback(self, point: np.ndarray) -> None:
        """
        Callback function for point picking interaction.

        Args:
            point: Picked point coordinates
        """
        if self.current_mesh is None:
            return

        # Find closest point on mesh
        closest_point_id = self.current_mesh.find_closest_point(point)
        closest_point = self.current_mesh.points[closest_point_id]

        # Store picked point
        self._picked_points.append({
            'id': closest_point_id,
            'coordinates': closest_point.copy(),
            'original_pick': point.copy()
        })

        # Create info text
        info_text = self._format_point_info(closest_point_id, closest_point)

        # Add text label
        label = self.plotter.add_text(
            info_text,
            position='lower_right',
            font_size=PICKING_LABEL_FONT_SIZE,
            color=PICKING_LABEL_COLOR,
            name=f'pick_label_{len(self._pick_labels)}'
        )

        self._pick_labels.append(label)

        # Call user callback if provided
        if self.pick_callback:
            self.pick_callback(closest_point_id, closest_point, self.current_mesh)

    def _format_point_info(self, point_id: int, point: np.ndarray) -> str:
        """
        Format point information for display.

        Args:
            point_id: Point index
            point: Point coordinates

        Returns:
            str: Formatted info text
        """
        info_lines = [
            f"Point ID: {point_id}",
            f"X: {point[0]:.3f}",
            f"Y: {point[1]:.3f}",
            f"Z: {point[2]:.3f}"
        ]

        # Add data arrays if available
        if self.current_mesh and self.current_mesh.point_data:
            for array_name, array_data in self.current_mesh.point_data.items():
                if len(array_data) > point_id:
                    value = array_data[point_id]
                    if np.isscalar(value):
                        info_lines.append(f"{array_name}: {value:.3f}")
                    else:
                        # Vector data
                        value_str = ", ".join([f"{v:.3f}" for v in value])
                        info_lines.append(f"{array_name}: [{value_str}]")

        return "\n".join(info_lines)

    def clear_picks(self) -> None:
        """Clear all picked points and labels."""
        # Remove labels
        for i, _ in enumerate(self._pick_labels):
            try:
                self.plotter.remove_actor(f'pick_label_{i}')
            except:
                pass

        # Clear stored data
        self._picked_points.clear()
        self._pick_labels.clear()

    def set_pick_callback(self, callback: Callable[[int, np.ndarray, pv.PolyData], None]) -> None:
        """
        Set a custom callback for point picking events.

        Args:
            callback: Function to call when point is picked
                     Signature: (point_id, coordinates, mesh)
        """
        self.pick_callback = callback

    def enable_picking(self, enabled: bool = True) -> None:
        """
        Enable or disable point picking.

        Args:
            enabled: Whether to enable picking
        """
        self.picking_enabled = enabled
        if self.plotter:
            if enabled:
                self.plotter.enable_point_picking(
                    callback=self._point_pick_callback,
                    show_point=True,
                    point_size=PICKING_POINT_SIZE,
                    color=PICKING_POINT_COLOR,
                    show_message=False
                )
            else:
                self.plotter.disable_picking()

    def get_picked_points(self) -> list[Dict]:
        """
        Get list of all picked points.

        Returns:
            list: List of picked point dictionaries
        """
        return self._picked_points.copy()

    def show(self,
             auto_close: bool = True,
             interactive: bool = True,
             screenshot: Optional[str] = None) -> None:
        """
        Display the visualization window.

        Args:
            auto_close: Whether to auto-close when done
            interactive: Whether to enable interaction
            screenshot: Optional screenshot filename
        """
        if self.plotter is None:
            raise RuntimeError("No plotter available. Add a mesh first.")

        # Take screenshot if requested
        if screenshot:
            self.plotter.screenshot(screenshot, transparent_background=False)

        # Show the plot
        if interactive:
            self.plotter.show(auto_close=auto_close)
        else:
            self.plotter.show(interactive=False, auto_close=auto_close)

    def close(self) -> None:
        """Close the visualization window."""
        if self.plotter:
            self.plotter.close()
            self.plotter = None

    def reset_camera(self) -> None:
        """Reset camera to fit current mesh."""
        if self.plotter:
            self.plotter.reset_camera()

    def set_background_color(self, color: str) -> None:
        """
        Set background color.

        Args:
            color: Color name or hex string
        """
        if self.plotter:
            self.plotter.background_color = color

    def export_scene(self, filename: str) -> None:
        """
        Export current scene as image.

        Args:
            filename: Output filename
        """
        if self.plotter:
            self.plotter.screenshot(filename, transparent_background=False)

    def add_text_overlay(self, text: str, position: str = 'upper_left', **kwargs) -> Any:
        """
        Add text overlay to the visualization.

        Args:
            text: Text to display
            position: Text position
            **kwargs: Additional text properties

        Returns:
            Text actor reference
        """
        if self.plotter:
            return self.plotter.add_text(text, position=position, **kwargs)
        return None

    def remove_text_overlay(self, text_actor: Any) -> None:
        """
        Remove text overlay.

        Args:
            text_actor: Text actor to remove
        """
        if self.plotter and text_actor:
            self.plotter.remove_actor(text_actor)
