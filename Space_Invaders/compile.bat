@echo off
py setup.py build_exe --excludes=matplotlib.tests,numpy.random._examples
echo Script finished
pause