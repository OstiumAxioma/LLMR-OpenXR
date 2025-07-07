@echo off
echo ========================================
echo Android Environment Setup Script
echo ========================================
echo.

:: Check if Android Studio is installed
echo Checking for Android Studio installation...

:: Common Android Studio installation paths
set ANDROID_STUDIO_PATHS=^
"C:\Program Files\Android\Android Studio" ^
"C:\Program Files (x86)\Android\Android Studio" ^
"%LOCALAPPDATA%\Google\AndroidStudio" ^
"%USERPROFILE%\AppData\Local\Google\AndroidStudio"

:: Common Android SDK paths
set ANDROID_SDK_PATHS=^
"%LOCALAPPDATA%\Android\Sdk" ^
"%USERPROFILE%\AppData\Local\Android\Sdk" ^
"C:\Android\Sdk" ^
"C:\Users\%USERNAME%\AppData\Local\Android\Sdk"

:: Find Android Studio
set ANDROID_STUDIO_FOUND=0
for %%p in (%ANDROID_STUDIO_PATHS%) do (
    if exist "%%p" (
        echo Found Android Studio at: %%p
        set ANDROID_STUDIO_FOUND=1
        goto :found_studio
    )
)

:found_studio
if %ANDROID_STUDIO_FOUND%==0 (
    echo.
    echo Android Studio not found in common locations.
    echo Please install Android Studio first:
    echo 1. Download from: https://developer.android.com/studio
    echo 2. Run the installer
    echo 3. Complete the setup wizard
    echo 4. Run this script again
    echo.
    pause
    exit /b 1
)

:: Find Android SDK
set ANDROID_SDK_FOUND=0
for %%s in (%ANDROID_SDK_PATHS%) do (
    if exist "%%s" (
        echo Found Android SDK at: %%s
        set ANDROID_SDK_PATH=%%s
        set ANDROID_SDK_FOUND=1
        goto :found_sdk
    )
)

:found_sdk
if %ANDROID_SDK_FOUND%==0 (
    echo.
    echo Android SDK not found. Please:
    echo 1. Open Android Studio
    echo 2. Go to File -> Settings -> Appearance & Behavior -> System Settings -> Android SDK
    echo 3. Note the Android SDK Location path
    echo 4. Run this script again
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setting up environment variables...
echo ========================================

:: Set ANDROID_HOME
setx ANDROID_HOME "%ANDROID_SDK_PATH%"
if errorlevel 1 (
    echo Error: Failed to set ANDROID_HOME
    pause
    exit /b 1
)

:: Add platform-tools to PATH
setx PATH "%PATH%;%ANDROID_SDK_PATH%\platform-tools"
if errorlevel 1 (
    echo Error: Failed to update PATH
    pause
    exit /b 1
)

:: Add tools to PATH
setx PATH "%PATH%;%ANDROID_SDK_PATH%\tools"
if errorlevel 1 (
    echo Error: Failed to update PATH
    pause
    exit /b 1
)

echo.
echo ========================================
echo Environment setup completed!
echo ========================================
echo.
echo ANDROID_HOME set to: %ANDROID_SDK_PATH%
echo PATH updated with platform-tools and tools
echo.
echo Please restart your terminal/command prompt
echo for the changes to take effect.
echo.
echo Next steps:
echo 1. Restart your terminal
echo 2. Run: adb version (to verify ADB is available)
echo 3. Run: build_android.bat (to build the APK)
echo.

pause 