@echo off
REM Batch file to compile Zork1 using ZILF/ZAPF
REM Output will be in the root directory to avoid overwriting COMPILED\zork1.z3

echo Compiling Zork1 with ZILF/ZAPF...
echo.

REM Set the ZILF path
set ZILF_PATH=C:\Program Files (x86)\ZILF\bin

REM Navigate to the zork1 directory
cd /d "%~dp0"

REM Compile with ZILF (creates .zap files)
echo Step 1: Running ZILF compiler...
"%ZILF_PATH%\zilf.exe" zork1.zil

if errorlevel 1 (
    echo.
    echo ERROR: ZILF compilation failed!
    pause
    exit /b 1
)

echo.
echo Step 2: Running ZAPF assembler...
REM Assemble with ZAPF (creates .z3 file)
"%ZILF_PATH%\zapf.exe" zork1.zap COMPILED\zork1-ignite.z3

if errorlevel 1 (
    echo.
    echo ERROR: ZAPF assembly failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Compilation successful!
echo Output file: COMPILED\zork1-ignite.z3
echo Original working version preserved in COMPILED\zork1.z3
echo ========================================
echo.
pause
