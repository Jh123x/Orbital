import sys
import os
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
                    "optimize": 2,
                    "include_files": ["data", "images", "sounds", "screenshots", "settings.cfg", "icon"],
                    "excludes": ['matplotlib.tests','numpy.random._examples'],
                    
                    }

# GUI applications require a different base on Windows (the default is for a
# console application).

setup(name = "Space Defenders",
    version = "1.0",
    description = "Space Defenders Game",
    author = "Group Space Defenders",
    options = {"build_exe": build_exe_options},
    executables = [Executable("SpaceDefenders.py", base='Win32GUI' if sys.platform == 'win32' else None, icon=os.path.join("icon","icon.ico"))])