@echo off
echo ========================================
echo OpenXR Android Build Script for Meta Quest
echo ========================================
echo.

:: Check if we're in the right directory
if not exist "src\tests\hello_xr\build.gradle" (
    echo Error: Please run this script from the OpenXR-SDK-Source root directory
    pause
    exit /b 1
)

:: Check if Android SDK is available
if not defined ANDROID_HOME (
    echo Warning: ANDROID_HOME not set, trying to find Android SDK...
    if exist "%LOCALAPPDATA%\Android\Sdk" (
        set ANDROID_HOME=%LOCALAPPDATA%\Android\Sdk
    ) else if exist "%USERPROFILE%\AppData\Local\Android\Sdk" (
        set ANDROID_HOME=%USERPROFILE%\AppData\Local\Android\Sdk
    ) else (
        echo Error: Android SDK not found. Please install Android Studio and set ANDROID_HOME
        pause
        exit /b 1
    )
)

echo Android SDK found at: %ANDROID_HOME%
echo.

:: Find local Gradle installation
set GRADLE_HOME=
for /d %%i in ("%USERPROFILE%\.gradle\wrapper\dists\gradle-8.5-bin\*") do (
    if exist "%%i\gradle-8.5\bin\gradle.bat" (
        set GRADLE_HOME=%%i\gradle-8.5
        goto :found_gradle
    )
)

:found_gradle
if not defined GRADLE_HOME (
    echo Error: Local Gradle installation not found
    echo Please ensure Gradle 8.5 is downloaded to: %USERPROFILE%\.gradle\wrapper\dists\gradle-8.5-bin\
    pause
    exit /b 1
)

echo Local Gradle found at: %GRADLE_HOME%
echo.

:: Change to hello_xr directory
cd src\tests\hello_xr

:: Show build options
echo Please select build variant:
echo 1. Vulkan Debug (Recommended for testing)
echo 2. Vulkan Release (For production)
echo 3. OpenGLES Debug
echo 4. OpenGLES Release
echo 5. Build all variants
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo Building Vulkan Debug APK...
    call "%GRADLE_HOME%\bin\gradle.bat" assembleVulkanDebug
) else if "%choice%"=="2" (
    echo Building Vulkan Release APK...
    call "%GRADLE_HOME%\bin\gradle.bat" assembleVulkanRelease
) else if "%choice%"=="3" (
    echo Building OpenGLES Debug APK...
    call "%GRADLE_HOME%\bin\gradle.bat" assembleOpenGLESDebug
) else if "%choice%"=="4" (
    echo Building OpenGLES Release APK...
    call "%GRADLE_HOME%\bin\gradle.bat" assembleOpenGLESRelease
) else if "%choice%"=="5" (
    echo Building all variants...
    call "%GRADLE_HOME%\bin\gradle.bat" assembleVulkanDebug
    call "%GRADLE_HOME%\bin\gradle.bat" assembleVulkanRelease
    call "%GRADLE_HOME%\bin\gradle.bat" assembleOpenGLESDebug
    call "%GRADLE_HOME%\bin\gradle.bat" assembleOpenGLESRelease
) else (
    echo Invalid choice
    pause
    exit /b 1
)

if errorlevel 1 (
    echo.
    echo Build failed! Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build completed successfully!
echo ========================================
echo.

:: Show APK locations
echo APK files created:
if exist "build\outputs\apk\vulkan\debug\app-vulkan-debug.apk" (
    echo - Vulkan Debug: build\outputs\apk\vulkan\debug\app-vulkan-debug.apk
)
if exist "build\outputs\apk\vulkan\release\app-vulkan-release.apk" (
    echo - Vulkan Release: build\outputs\apk\vulkan\release\app-vulkan-release.apk
)
if exist "build\outputs\apk\opengles\debug\app-opengles-debug.apk" (
    echo - OpenGLES Debug: build\outputs\apk\opengles\debug\app-opengles-debug.apk
)
if exist "build\outputs\apk\opengles\release\app-opengles-release.apk" (
    echo - OpenGLES Release: build\outputs\apk\opengles\release\app-opengles-release.apk
)

echo.
echo Next steps:
echo 1. Connect your Meta Quest device via USB
echo 2. Enable developer mode on the device
echo 3. Run: adb install build\outputs\apk\vulkan\debug\app-vulkan-debug.apk
echo 4. Start the test server: cd examples && python quest_test_server.py
echo 5. Launch the app on your Quest device
echo.
echo For detailed instructions, see META_QUEST_DEPLOYMENT_GUIDE.md
echo.

pause 