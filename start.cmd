@echo off
setlocal EnableExtensions
chcp 65001 >nul
cd /d "%~dp0"
title AutoApply Local

set "BUNDLED_PY=C:\Users\Redmi Book\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"

if exist "%BUNDLED_PY%" goto use_bundled

where py.exe >nul 2>nul
if not errorlevel 1 goto use_launcher

where python.exe >nul 2>nul
if not errorlevel 1 goto use_python

echo.
echo [ERROR] Python 3 was not found.
echo Install Python 3.10 or newer, then run this file again.
echo.
pause
exit /b 1

:use_bundled
"%BUNDLED_PY%" app.py %*
set "APP_EXIT=%ERRORLEVEL%"
goto finished

:use_launcher
py -3 app.py %*
set "APP_EXIT=%ERRORLEVEL%"
goto finished

:use_python
python app.py %*
set "APP_EXIT=%ERRORLEVEL%"
goto finished

:finished
if "%APP_EXIT%"=="0" exit /b 0
echo.
echo [ERROR] AutoApply failed to start. Exit code: %APP_EXIT%
echo Please keep this window open and send a screenshot of the error.
echo.
pause
exit /b %APP_EXIT%
