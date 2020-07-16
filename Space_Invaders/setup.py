import os
import sys
from cx_Freeze import setup, Executable
exe = Executable(
    script=os.path.join(os.path.dirname(__file__), "__main__.py"),
    base = 'Win32GUI' if sys.platform=='win32' else None,
    )

build_options = {
                 "includes":['classes', 'numpy', 'torch', 'pygame', 'cv2', 'scipy', 'matplotlib'],
                 "include_files" : ['data', 'images', 'screenshots', 'sounds', 'model', os.path.join(os.path.dirname(__file__),'settings.cfg')],
                }

setup(
    name = "Space Defenders",
    version = "0.2",
    description = "Space Defenders game by group Space Defenders: More information at https://github.com/Jh123x/Orbital/",
    author="Space Defenders",
    options = {'build_exe': build_options},
    executables = [exe]
    )

