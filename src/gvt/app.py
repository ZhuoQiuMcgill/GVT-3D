"""
Main application controller and entry point for GVT.
Coordinates mesh loading, visualization, and user interactions.
"""

import sys
import argparse
from typing import Optional, List
from pathlib import Path

from .importer import MeshImporter
from .visualizer import MeshVisualizer
from ..config import DEBUG_MODE, WINDOW_TITLE, DEFAULT_RENDER_STYLE
from ..utils import find_sample_files, get_file_extension


class GVTApp:
    """
    Main application class for the Generic Visualization Tool.
    Coordinates mesh loading, visualization, and interactions.
    """

    def __init__(self, verbose: bool = True):
        """
        Initialize the GVT application.

        Args:
            verbose: Enable verbose output
        """
        self.verbose = verbose
        self.importer = MeshImporter(verbose=verbose)
        self.visualizer = MeshVisualizer()
        self.current_file = None

        # Set up custom pick callback
        self.visualizer.set_pick_callback(self._on_point_picked)

    def load_and_show(self,
                      file_path: str,
                      preprocess: bool = True,
                      auto_center: bool = True,
                      auto_scale: bool = True,
                      **viz_kwargs) -> None:
        """
        Load a mesh file and display it.

        Args:
            file_path: Path to mesh file
            preprocess: Apply preprocessing
            auto_center: Center the mesh
            auto_scale: Normalize mesh scale
            **viz_kwargs: Additional visualization parameters
        """
        try:
            if self.verbose:
                print(f"Loading mesh from: {file_path}")

            # Load mesh
            mesh = self.importer.load_mesh(
                file_path,
                preprocess=preprocess,
                auto_center=auto_center,
                auto_scale=auto_scale
            )

            # Store current file
            self.current_file = file_path

            # Add to visualizer
            self.visualizer.add_mesh(mesh, **viz_kwargs)

            # Add file info overlay
            file_name = Path(file_path).name
            mesh_info = self.importer.get_last_loaded_info()
            info_text = f"File: {file_name}\nPoints: {mesh_info['n_points']:,}\nCells: {mesh_info['n_cells']:,}"

            self.visualizer.add_text_overlay(
                info_text,
                position='upper_left',
                font_size=12,
                color='white'
            )

            if self.verbose:
                print("Mesh loaded and added to visualizer")
                print("Use mouse to interact:")
                print("  - Left click + drag: Rotate")
                print("  - Right click + drag: Pan")
                print("  - Scroll: Zoom")
                print("  - Ctrl + Left click: Pick point")

        except Exception as e:
            print(f"Error loading mesh: {e}")
            if DEBUG_MODE:
                import traceback
                traceback.print_exc()
            raise

    def _on_point_picked(self, point_id: int, coordinates, mesh) -> None:
        """
        Handle point picking events.

        Args:
            point_id: Picked point ID
            coordinates: Point coordinates
            mesh: Mesh object
        """
        if self.verbose:
            print(f"Picked point {point_id} at ({coordinates[0]:.3f}, {coordinates[1]:.3f}, {coordinates[2]:.3f})")

    def show(self, interactive: bool = True, screenshot: Optional[str] = None) -> None:
        """
        Show the visualization window.

        Args:
            interactive: Enable interaction
            screenshot: Optional screenshot filename
        """
        self.visualizer.show(interactive=interactive, screenshot=screenshot)

    def run_interactive(self) -> None:
        """Run the application in interactive mode."""
        try:
            if self.visualizer.current_mesh is None:
                print("No mesh loaded. Please load a mesh first.")
                return

            print(f"\n{WINDOW_TITLE}")
            print("=" * len(WINDOW_TITLE))
            print("Interactive mode - Close window to exit")

            if self.current_file:
                print(f"Displaying: {Path(self.current_file).name}")

            picked_points = self.visualizer.get_picked_points()
            if picked_points:
                print(f"Picked points: {len(picked_points)}")

            self.show(interactive=True)

        except KeyboardInterrupt:
            print("\nExiting...")
        except Exception as e:
            print(f"Error in interactive mode: {e}")
            if DEBUG_MODE:
                import traceback
                traceback.print_exc()
        finally:
            self.close()

    def close(self) -> None:
        """Close the application and clean up resources."""
        self.visualizer.close()

    @staticmethod
    def list_sample_files() -> List[str]:
        """
        List available sample files in the data directory.

        Returns:
            list: List of sample file paths
        """
        return find_sample_files()

    @staticmethod
    def get_supported_formats() -> List[str]:
        """
        Get list of supported file formats.

        Returns:
            list: Supported file extensions
        """
        return MeshImporter.get_supported_formats()


def create_argument_parser() -> argparse.ArgumentParser:
    """Create command line argument parser."""
    parser = argparse.ArgumentParser(
        description="GVT - Generic Visualization Tool for 3D meshes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.gvt.app model.obj
  python -m src.gvt.app data/sample.vtk --no-center
  python -m src.gvt.app model.stl --style surface
  python -m src.gvt.app --list-samples
  python -m src.gvt.app --supported-formats
        """
    )

    parser.add_argument(
        'file',
        nargs='?',
        help='Path to mesh file to visualize'
    )

    parser.add_argument(
        '--list-samples',
        action='store_true',
        help='List available sample files'
    )

    parser.add_argument(
        '--supported-formats',
        action='store_true',
        help='Show supported file formats'
    )

    parser.add_argument(
        '--no-preprocess',
        action='store_true',
        help='Skip mesh preprocessing'
    )

    parser.add_argument(
        '--no-center',
        action='store_true',
        help='Do not center the mesh'
    )

    parser.add_argument(
        '--no-scale',
        action='store_true',
        help='Do not normalize mesh scale'
    )

    parser.add_argument(
        '--screenshot',
        type=str,
        help='Save screenshot to file and exit'
    )

    parser.add_argument(
        '--style',
        type=str,
        choices=['surface', 'wireframe', 'points'],
        default=DEFAULT_RENDER_STYLE,
        help=f'Rendering style (default: {DEFAULT_RENDER_STYLE})'
    )

    parser.add_argument(
        '--point-size',
        type=float,
        default=None,
        help='Size of points in visualization'
    )

    parser.add_argument(
        '--line-width',
        type=float,
        default=None,
        help='Width of lines in visualization'
    )

    parser.add_argument(
        '--color',
        type=str,
        default=None,
        help='Mesh color (e.g., "red", "blue", "#FF0000")'
    )

    parser.add_argument(
        '--opacity',
        type=float,
        default=None,
        help='Mesh opacity (0.0-1.0)'
    )

    parser.add_argument(
        '--show-edges',
        action='store_true',
        help='Show mesh edges (for surface style)'
    )

    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress verbose output'
    )

    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode'
    )

    return parser


def main():
    """Main entry point for the application."""
    parser = create_argument_parser()
    args = parser.parse_args()

    # Handle special commands
    if args.list_samples:
        samples = GVTApp.list_sample_files()
        if samples:
            print("Available sample files:")
            for sample in samples:
                print(f"  {sample}")
        else:
            print("No sample files found in data directory")
        return

    if args.supported_formats:
        formats = GVTApp.get_supported_formats()
        print("Supported file formats:")
        for fmt in formats:
            print(f"  {fmt}")
        return

    # Check if file argument provided
    if not args.file:
        # Try to find a sample file
        samples = GVTApp.list_sample_files()
        if samples:
            print("No file specified. Available sample files:")
            for sample in samples:
                print(f"  {Path(sample).name}")
            print(f"\nUsage: python -m src.gvt.app <file_path>")
        else:
            print("Usage: python -m src.gvt.app <file_path>")
            print("Use --help for more options")
        return

    # Set debug mode if requested
    if args.debug:
        import src.config as config
        config.DEBUG_MODE = True

    # Create and configure app
    app = GVTApp(verbose=not args.quiet)

    try:
        # Prepare visualization kwargs
        viz_kwargs = {}

        # Set style
        viz_kwargs['style'] = args.style

        # Set point and line sizes if specified
        if args.point_size is not None:
            viz_kwargs['point_size'] = args.point_size
        if args.line_width is not None:
            viz_kwargs['line_width'] = args.line_width

        # Set color and opacity
        if args.color:
            viz_kwargs['color'] = args.color
        if args.opacity is not None:
            viz_kwargs['opacity'] = args.opacity

        # Edge display (mainly for surface style)
        if args.show_edges:
            viz_kwargs['show_edges'] = True

        # Load and show mesh
        app.load_and_show(
            args.file,
            preprocess=not args.no_preprocess,
            auto_center=not args.no_center,
            auto_scale=not args.no_scale,
            **viz_kwargs
        )

        # Handle screenshot mode
        if args.screenshot:
            app.show(interactive=False, screenshot=args.screenshot)
            print(f"Screenshot saved to: {args.screenshot}")
        else:
            # Run in interactive mode
            app.run_interactive()

    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        app.close()


if __name__ == '__main__':
    main()