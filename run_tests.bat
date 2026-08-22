@echo off
REM Wrapper to run pytest using the project's virtual environment
SET "VENV_DIR=%~dp0\.venv"
"%VENV_DIR%\Scripts\python.exe" -m pytest -vv
