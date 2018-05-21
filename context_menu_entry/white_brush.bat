@echo off
REM This file will be used by the context menu entry to start white brushing
REM an image. For this purpose, it will be copied to %APPDATA%/white_brush,
REM since registry entries in Windows only work with absolute paths.
start pythonw.exe -m white_brush %1
