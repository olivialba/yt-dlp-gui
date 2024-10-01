@echo off
REM Check if Python is installed
py --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not added to PATH.
    pause
    exit /b 1
)

REM Download FFmpeg using PowerShell
powershell -command "Invoke-WebRequest -Uri 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z' -OutFile 'ffmpeg-git-full.7z'"
echo Download complete.

REM Check if FFMPEG_PATH is already in the PATH
SET "FFMPEG_PATH=C:\ffmpeg\bin"
echo %PATH% | findstr /C:"%FFMPEG_PATH%" >nul
if %errorlevel%==0 (
    echo The path is already in the PATH variable.
) else (
    REM Add FFMPEG_PATH to the PATH
    setx PATH "%PATH%;%FFMPEG_PATH%"
    echo Added %FFMPEG_PATH% to the PATH variable.
)

REM Upgrade pip to the latest version (optional but recommended)
py -m pip install --upgrade pip

REM Install packages from requirements.txt
py -m pip install -r requirements.txt

echo.
echo All packages have been installed.
pause
