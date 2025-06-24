"""
Global configuration settings for GVT project.
All hardcoded values and settings are centralized here for easy maintenance.
"""

import os

# Project paths
ROOT_DIR = os.getcwd()
DATA_DIR = os.path.join(ROOT_DIR, "data")
SRC_DIR = os.path.join(ROOT_DIR, "src")

# Supported file formats
SUPPORTED_FORMATS = [".vtk", ".obj", ".ply", ".stl"]

# Visualizer Settings
WINDOW_TITLE = "GVT - Generic Visualization Tool"
DEFAULT_WINDOW_SIZE = [1024, 768]
BACKGROUND_COLOR = "black"
MESH_COLOR = "white"
MESH_OPACITY = 1.0
MESH_SPECULAR = 0.5
MESH_SPECULAR_POWER = 20

# Interaction Settings
PICKING_ENABLED = True
PICKING_LABEL_COLOR = "yellow"
PICKING_LABEL_FONT_SIZE = 16
PICKING_POINT_SIZE = 10
PICKING_POINT_COLOR = "red"

# Camera Settings
DEFAULT_CAMERA_POSITION = None  # Auto-fit to model
AUTO_CAMERA_RESET = True

# Lighting Settings
LIGHTING_ENABLED = True
AMBIENT_LIGHT = 0.3
DIFFUSE_LIGHT = 0.7

# Performance Settings
USE_DEPTH_PEELING = True
ANTI_ALIASING = True
SMOOTH_SHADING = True

# Debug Settings
DEBUG_MODE = False
VERBOSE_LOADING = True
SHOW_EDGES = False
EDGE_COLOR = "gray"
