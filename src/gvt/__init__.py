"""
GVT (Generic Visualization Tool) package.
Core visualization functionality for 3D mesh rendering and interaction.
"""

from .importer import MeshImporter
from .visualizer import MeshVisualizer
from .app import GVTApp

__version__ = "1.0.0"
__author__ = "GVT Development Team"

__all__ = [
    'MeshImporter',
    'MeshVisualizer',
    'GVTApp'
]