@echo off
setlocal
cd /d "%~dp0"
set PY=

py -3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)" 2>nul
if %ERRORLEVEL%==0 set PY=py -3

if not defined PY (
  python -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)" 2>nul
  if %ERRORLEVEL%==0 set PY=python
)

if not defined PY (
  echo Python 3.10+ not found. The Windows "python" shortcut that opens the Microsoft Store does not count.
  echo Install from https://www.python.org/downloads/ and check "Add python.exe to PATH".
  echo Then: py -3 -m pip install -r requirements.txt
  exit /b 1
)

%PY% build_pdfs.py %*
exit /b %ERRORLEVEL%
