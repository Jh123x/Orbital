import os
import sys
import pygame

from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "optimize": 2,
    "include_files": ["data", "images", "sounds", "settings.cfg", "icon"],
    "excludes": ['numpy.random._examples'],
}

setup(name="Space Defenders",
      version="1.2",
      description="Space Defenders Game",
      author="Group Space Defenders",
      options={"build_exe": build_exe_options},
      executables=[Executable("SpaceDefenders.py", base='Win32GUI' if sys.platform == 'win32' else None,
                              icon=os.path.join("icon", "icon.ico"))])
