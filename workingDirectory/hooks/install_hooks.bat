@REM
@REM  Copyright (c) 2018-2024 M. Schuler, TTZ-EMO, Technical University of
@REM  Applied Sciences Wuerzburg-Schweinfurt.
@REM
@REM  This file is part of PyEMMO
@REM  (see https://gitlab.ttz-emo.thws.de/ag-em/pyemmo).
@REM
@REM  This program is free software: you can redistribute it and/or modify
@REM  it under the terms of the GNU General Public License as published by
@REM  the Free Software Foundation, either version 3 of the License, or
@REM  (at your option) any later version.
@REM
@REM  This program is distributed in the hope that it will be useful,
@REM  but WITHOUT ANY WARRANTY; without even the implied warranty of
@REM  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
@REM  GNU General Public License for more details.
@REM
@REM  You should have received a copy of the GNU General Public License
@REM  along with this program. If not, see <http://www.gnu.org/licenses/>.
@REM

REM Check if MSG command is available and session is interactive
where msg >nul 2>&1
if %ERRORLEVEL%==0 (
    if not "%SESSIONNAME%"=="" (
        MSG %USERNAME% "Make sure to update the Python path in workingDirectory\hooks\pre-commit to your preferred python version and pre-commit is installed there (install with: pip install pre-commit)"
    )
)

@echo off
setlocal

REM Define directories
set HOOKS_DIR=%~dp0
set GIT_HOOKS_DIR=%~dp0..\..\.git\hooks

@REM echo %~dp0
@REM echo %HOOKS_DIR%
@REM echo %GIT_HOOKS_DIR%


REM Ensure the .git/hooks directory exists
if not exist "%GIT_HOOKS_DIR%" (
    mkdir "%GIT_HOOKS_DIR%"
)

REM Copy all hook scripts from hooks directory to .git/hooks
echo Copy hooks to "%GIT_HOOKS_DIR%"
copy /Y "%HOOKS_DIR%\pre*" "%GIT_HOOKS_DIR%"

echo Hooks installed.
endlocal
