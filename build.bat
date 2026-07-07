@echo off

echo ===============================
echo Building BarcodeGen...
echo ===============================

call .venv\Scripts\activate.bat

rmdir /S /Q build 2>nul
rmdir /S /Q dist 2>nul

pyinstaller BarcodeGen.spec

echo.
echo ===============================
echo Build finished.
echo ===============================

pause