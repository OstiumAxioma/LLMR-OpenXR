@echo off
setlocal enabledelayedexpansion

echo ========================================
echo OpenXR Hello_XR Build and Run Script
echo ========================================
echo.
echo Press any key to start the build process...
pause >nul

REM Check if build directory exists, create if not
if not exist "build" (
    echo [Step 1] Creating build directory...
    mkdir build
    echo [OK] build directory created successfully
) else (
    echo [Step 1] build directory already exists
)

REM Check if win64 directory exists, create if not
if not exist "build\win64" (
    echo [Step 2] Creating build\win64 directory...
    mkdir build\win64
    echo [OK] build\win64 directory created successfully
) else (
    echo [Step 2] build\win64 directory already exists
)

echo.
echo [Step 3] Entering build\win64 directory...
cd build\win64
echo [OK] Current directory: %CD%

echo.
echo [Step 4] Generating Visual Studio 2022 project files...
echo Command: cmake -G "Visual Studio 17 2022" -A x64 ../..
echo.
echo Please wait, this may take several minutes...
echo.

REM Run CMake to generate project files
cmake -G "Visual Studio 17 2022" -A x64 ../..

REM Check if CMake was successful
if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] CMake configuration failed!
    echo Error code: %ERRORLEVEL%
    echo.
    echo Please check the following possible issues:
    echo 1. Is Visual Studio 2022 installed?
    echo 2. Is CMake installed and added to PATH?
    echo 3. Are you running this script from the correct OpenXR-SDK-Source directory?
    echo 4. Do you have enough disk space?
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

echo.
echo [OK] CMake configuration successful!
echo.
echo [Step 5] Building hello_xr project...
echo Command: cmake --build . --target hello_xr --config Release
echo.
echo Build process may take 5-15 minutes, please be patient...
echo.

REM Build hello_xr project using CMake (Release configuration)
cmake --build . --target hello_xr --config Release

REM Check if build was successful
if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] Build failed!
    echo Error code: %ERRORLEVEL%
    echo.
    echo Please check the build error messages. Common issues:
    echo 1. Missing required dependencies
    echo 2. Incompatible compiler version
    echo 3. Insufficient memory
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

echo.
echo [OK] Build successful!
echo.

REM Check if executable exists
if not exist "src\tests\hello_xr\Release\hello_xr.exe" (
    echo [ERROR] Executable not found!
    echo Expected location: src\tests\hello_xr\Release\hello_xr.exe
    echo.
    echo Possible reasons:
    echo 1. Build process encountered errors
    echo 2. Incorrect output path
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

echo [Step 6] Found executable: src\tests\hello_xr\Release\hello_xr.exe
echo.
echo [Step 7] Starting Hello_XR application...
echo Using graphics API: Vulkan
echo.
echo If Vulkan is not available, the program may fail
echo Press any key to continue and run the application...
pause >nul

REM Run hello_xr application - try the manual way that works
echo [Step 7a] Running from Release directory (manual method)...
cd src\tests\hello_xr\Release
echo Command: .\hello_xr.exe -g Vulkan
echo Current working directory: %CD%
echo.

REM Clear any conflicting environment variables
echo [Step 7b] Clearing environment variables to use system defaults...
set XR_RUNTIME_JSON=
echo Cleared XR_RUNTIME_JSON environment variable
echo.

echo Note: If this fails, please try running manually:
echo 1. Open Command Prompt
echo 2. Navigate to: %CD%
echo 3. Run: .\hello_xr.exe -g Vulkan
echo.
.\hello_xr.exe -g Vulkan

REM Check if run was successful
if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] Application run failed!
    echo Error code: %ERRORLEVEL%
    echo.
    echo Possible solutions:
    echo 1. Try other graphics API: hello_xr.exe --graphics d3d11
    echo 2. Check if Vulkan drivers are installed
    echo 3. Check if system supports VR devices
    echo 4. Check if VR runtime is available (SteamVR, Oculus, etc.)
    echo.
    echo Do you want to try D3D11 graphics API? (Y/N)
    set /p choice=
    if /i "!choice!"=="Y" (
        echo.
        echo Trying D3D11 graphics API...
        hello_xr.exe --graphics d3d11
    )
)

echo.
echo ========================================
echo Build and run process completed
echo ========================================
echo.
echo Press any key to exit...
pause >nul 