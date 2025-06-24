## Save Conda Environment

---
### Windows
```
conda env export --no-builds | findstr /v /c:"prefix:" > environment.yml
```
### Linux
```
conda env export --no-builds | grep -v "^prefix:" > environment.yml
```