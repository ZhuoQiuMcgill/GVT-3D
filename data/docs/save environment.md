# Save Conda Environment

This guide shows how to export your conda environment for sharing or backup purposes.

## Export Options

### With Builds vs No Builds

- **With Builds**: Includes platform-specific build strings, ensuring exact package versions but less portable across different platforms
- **No Builds**: Excludes build strings, more portable across platforms but may install slightly different package versions

---

## Windows

### Export with Builds (Platform-specific)
```cmd
conda env export | findstr /v /c:"prefix:" > environment-with-builds.yml
```

### Export without Builds (Cross-platform compatible)
```cmd
conda env export --no-builds | findstr /v /c:"prefix:" > environment.yml
```

### Alternative using PowerShell
```powershell
# With builds
conda env export | Where-Object { $_ -notmatch "^prefix:" } | Out-File -FilePath environment-with-builds.yml -Encoding utf8

# Without builds
conda env export --no-builds | Where-Object { $_ -notmatch "^prefix:" } | Out-File -FilePath environment.yml -Encoding utf8
```

---

## Linux

### Export with Builds (Platform-specific)
```bash
conda env export | grep -v "^prefix:" > environment-with-builds.yml
```

### Export without Builds (Cross-platform compatible)
```bash
conda env export --no-builds | grep -v "^prefix:" > environment.yml
```

---

## macOS

### Export with Builds (Platform-specific)
```bash
conda env export | grep -v "^prefix:" > environment-with-builds.yml
```

### Export without Builds (Cross-platform compatible)
```bash
conda env export --no-builds | grep -v "^prefix:" > environment.yml
```

---

## Additional Export Options

### Export Only Direct Dependencies
```bash
# Cross-platform - exports only explicitly installed packages
conda env export --from-history > environment-minimal.yml
```

### Export Specific Channels
```bash
# Include specific conda channels
conda env export --no-builds --channel conda-forge > environment.yml
```

### Export with pip packages only
```bash
# Export only pip-installed packages
pip freeze > requirements.txt
```

---

## Usage Examples

### For Development Team Sharing (Recommended)
```bash
# Use no-builds version for cross-platform compatibility
conda env export --no-builds | grep -v "^prefix:" > environment.yml
```

### For Exact Reproduction (Same Platform)
```bash
# Use with-builds version for exact package versions
conda env export | grep -v "^prefix:" > environment-exact.yml
```

### For Minimal Environment File
```bash
# Export only directly installed packages
conda env export --from-history > environment-minimal.yml
```

---

## Restoring Environment

### From environment.yml
```bash
# Create environment from exported file
conda env create -f environment.yml

# Update existing environment
conda env update -f environment.yml
```

### From requirements.txt (pip only)
```bash
# Install pip packages in active environment
pip install -r requirements.txt
```

---

## Best Practices

1. **For team projects**: Use `--no-builds` for better cross-platform compatibility
2. **For production deployment**: Use specific version with builds for reproducibility
3. **Regular backups**: Export environment files before major updates
4. **Version control**: Include environment.yml in your repository
5. **Documentation**: Add setup instructions in README.md

### Recommended Workflow
```bash
# 1. Export cross-platform version for team
conda env export --no-builds | grep -v "^prefix:" > environment.yml

# 2. Export exact version for production
conda env export | grep -v "^prefix:" > environment-production.yml

# 3. Export minimal version for reference
conda env export --from-history > environment-minimal.yml
```