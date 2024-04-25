@echo off
echo Activating Conda environment...
call conda activate distri
echo Conda environment activated.
echo.
echo Starting CServer.py...
start python CServer.py
echo CServer.py started.
echo.
echo Starting BServer.py...
start python BServer.py
echo BServer.py started.
echo.
pause
