# Environment Setup Guide

This guide provides detailed instructions for setting up the development environment using Anaconda/Miniconda.

## Prerequisites

### Install Anaconda or Miniconda

#### Option 1: Anaconda (Recommended for beginners)
- **Windows**: Download from [https://www.anaconda.com/download](https://www.anaconda.com/download)
- **macOS**: Download from [https://www.anaconda.com/download](https://www.anaconda.com/download)
- **Linux**: Download from [https://www.anaconda.com/download](https://www.anaconda.com/download)

#### Option 2: Miniconda (Lightweight option)
- **Windows**: Download from [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)
- **macOS**: Download from [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)
- **Linux**: Download from [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)

---

## Environment Setup

### Method 1: Create Environment from scratch

#### Step 1: Create New Conda Environment
```bash
# Create environment with Python 3.11
conda create -n gvt-env python=3.11

# Activate the environment
conda activate gvt-env
```

#### Step 2: Install Core Dependencies
```bash
# Install PyVista and scientific computing packages
conda install -c conda-forge pyvista numpy

# Install additional dependencies
pip install pyvista==0.45.2
```

#### Step 3: Install Optional Dependencies
```bash
# For enhanced visualization features
conda install -c conda-forge matplotlib

# For development and testing
conda install -c conda-forge pytest black flake8
```

### Method 2: Create Environment from environment.yml (If available)

#### Step 1: Create Environment from File
```bash
# Navigate to project directory
cd /path/to/your/project

# Create environment from environment.yml
conda env create -f environment.yml

# Activate the environment
conda activate gvt-env
```

---

## Verification

### Verify Installation
```bash
# Activate environment
conda activate gvt-env

# Check Python version
python --version

# Check PyVista installation
python -c "import pyvista as pv; print(f'PyVista version: {pv.__version__}')"

# Check if GPU acceleration is available (optional)
python -c "import pyvista as pv; pv.start_xvfb(); print('PyVista setup successful')"
```

### Test Project Setup
```bash
# Navigate to project root
cd /path/to/your/project

# Test basic import
python -c "from src.gvt import GVTApp; print('GVT import successful')"

# Run a simple test (if test data exists)
python -m src.gvt.app --list-samples
```

---

## Environment Management

### Daily Usage
```bash
# Activate environment
conda activate gvt-env

# Deactivate environment when done
conda deactivate
```

### Update Dependencies
```bash
# Update all packages
conda update --all

# Update specific package
conda update pyvista
```

### Remove Environment (if needed)
```bash
# Remove the entire environment
conda env remove -n gvt-env
```

---

## Platform-Specific Notes

### Windows
- Make sure to run commands in Anaconda Prompt or PowerShell
- If using PyVista with Jupyter, install: `conda install -c conda-forge ipywidgets`

### macOS
- On Apple Silicon Macs, ensure you're using the native conda installation
- May need to install XCode command line tools: `xcode-select --install`

### Linux
- Install system dependencies if needed:
  ```bash
  # Ubuntu/Debian
  sudo apt-get install libgl1-mesa-glx libegl1-mesa libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6
  
  # CentOS/RHEL/Fedora
  sudo yum install mesa-libGL-devel mesa-libEGL-devel
  ```

### For Headless Servers (Linux only)
```bash
# Install virtual display for headless environments
conda install -c conda-forge xvfb

# Set up virtual display in Python
python -c "import pyvista as pv; pv.start_xvfb()"
```

---

## Troubleshooting

### Common Issues

#### ImportError: No module named 'pyvista'
```bash
# Ensure environment is activated
conda activate gvt-env

# Reinstall PyVista
pip uninstall pyvista
pip install pyvista==0.45.2
```

#### OpenGL/Display Issues
```bash
# For remote connections or headless systems
export DISPLAY=:0.0

# Use software rendering
export MESA_GL_VERSION_OVERRIDE=3.3
```

#### Permission Issues
```bash
# On Unix systems, ensure proper permissions
chmod +x scripts/*
```

### Getting Help
- PyVista Documentation: [https://docs.pyvista.org/](https://docs.pyvista.org/)
- Conda Documentation: [https://docs.conda.io/](https://docs.conda.io/)
- Project Issues: Check the project's issue tracker