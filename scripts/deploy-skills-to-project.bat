@echo off
REM SpecMap Skills Deployment Script for Windows
REM Automatically creates all SpecMap skills in your project

echo ======================================================
echo   SpecMap Skills Deployment
echo ======================================================
echo.

REM Get target project directory
if "%~1"=="" (
    echo Usage: deploy-skills-to-project.bat C:\path\to\your\project
    echo.
    echo Example:
    echo   deploy-skills-to-project.bat C:\Users\YourName\vortxx
    echo.
    exit /b 1
)

set PROJECT_DIR=%~1

REM Verify project directory exists
if not exist "%PROJECT_DIR%" (
    echo Error: Directory not found: %PROJECT_DIR%
    exit /b 1
)

echo Target project: %PROJECT_DIR%
echo.

REM Create skills directory
set SKILLS_DIR=%PROJECT_DIR%\.claude\skills
if not exist "%SKILLS_DIR%" mkdir "%SKILLS_DIR%"

echo Created skills directory: %SKILLS_DIR%
echo.
echo Creating skill files...
echo.

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0
set SOURCE_SKILLS_DIR=%SCRIPT_DIR%..\. claude\skills

REM Check if source skills exist
if exist "%SOURCE_SKILLS_DIR%" (
    echo Copying skills from: %SOURCE_SKILLS_DIR%
    xcopy "%SOURCE_SKILLS_DIR%\*" "%SKILLS_DIR%\" /E /I /Y >nul
    echo Skills copied successfully!
) else (
    echo Source skills directory not found. Creating skills from templates...
    echo.
    echo To get the skills, either:
    echo 1. Clone the SpecMap repository:
    echo    git clone https://github.com/bsifflard77/specmap-mcp.git
    echo    cd specmap-mcp
    echo    xcopy .claude\skills\* %SKILLS_DIR%\ /E /I
    echo.
    echo 2. Or copy the skills folder manually from the SpecMap repository
    exit /b 1
)

echo.
echo ======================================================
echo   Deployment Complete!
echo ======================================================
echo.
echo Skills installed in: %SKILLS_DIR%
echo.
echo Installed skills:
dir /b "%SKILLS_DIR%\*.md"
echo.
echo Next steps:
echo 1. Open your project in Claude Code Desktop
echo 2. Try: /skill specmap-reviewer
echo 3. See docs\VORTXX-DEPLOYMENT-PLAN.md for usage guide
echo.
