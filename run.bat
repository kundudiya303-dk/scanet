@echo off
setlocal
cd /d "%~dp0"
title scanet - Cybersecurity Reconnaissance Platform

if exist "backend\.venv\Scripts\python.exe" goto use_venv

where py >nul 2>nul
if errorlevel 1 goto check_python
py -3 --version >nul 2>nul
if not errorlevel 1 goto use_py

:check_python
where python >nul 2>nul
if errorlevel 1 goto missing_python
python --version >nul 2>nul
if not errorlevel 1 goto use_python

:use_py
py -3 run.py %*
if errorlevel 1 goto launcher_error
exit /b 0

:use_venv
"backend\.venv\Scripts\python.exe" run.py %*
if errorlevel 1 goto launcher_error
exit /b 0

:use_python
python run.py %*
if errorlevel 1 goto launcher_error
exit /b 0

:launcher_error
echo [!] scanet exited with an error. Review the messages above.
pause
exit /b 1

:missing_python
echo [!] Python 3.10 or newer was not found.
echo     Install Python from https://www.python.org/downloads/
echo     During installation, enable "Add python.exe to PATH", then run run.bat again.
pause
exit /b 1
