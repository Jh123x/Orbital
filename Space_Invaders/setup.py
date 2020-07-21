import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
                    "optimize": 2,
                    "include_files": ["data", "images", "sounds", "screenshots", "settings.cfg"]
                    }

# GUI applications require a different base on Windows (the default is for a
# console application).

setup(name = "Space Defenders",
    version = "0.3",
    description = "Space Defenders Game",
    options = {"build_exe": build_exe_options},
    executables = [Executable("__main__.py", base='Win32GUI')])