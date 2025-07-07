@echo off
echo ========================================
echo Meta Quest Deployment Script
echo ========================================
echo.

:: Check if ADB is available
adb version >nul 2>&1
if errorlevel 1 (
    echo Error: ADB not found. Please install Android SDK and add platform-tools to PATH
    pause
    exit /b 1
)

:: Check device connection
echo Checking device connection...
adb devices
echo.

:: Check if device is connected
adb devices | find "device$" >nul
if errorlevel 1 (
    echo Error: No Quest device connected. Please:
    echo 1. Connect your Quest device via USB
    echo 2. Enable developer mode
    echo 3. Allow USB debugging when prompted
    pause
    exit /b 1
)

echo Device connected successfully!
echo.

:: Show available APK files
echo Available APK files:
set apk_found=0

if exist "src\tests\hello_xr\build\outputs\apk\vulkan\debug\app-vulkan-debug.apk" (
    echo 1. Vulkan Debug APK
    set apk_found=1
)
if exist "src\tests\hello_xr\build\outputs\apk\vulkan\release\app-vulkan-release.apk" (
    echo 2. Vulkan Release APK
    set apk_found=1
)
if exist "src\tests\hello_xr\build\outputs\apk\opengles\debug\app-opengles-debug.apk" (
    echo 3. OpenGLES Debug APK
    set apk_found=1
)
if exist "src\tests\hello_xr\build\outputs\apk\opengles\release\app-opengles-release.apk" (
    echo 4. OpenGLES Release APK
    set apk_found=1
)

if %apk_found%==0 (
    echo No APK files found. Please build the project first using build_android.bat
    pause
    exit /b 1
)

echo.
set /p choice="Select APK to install (1-4): "

if "%choice%"=="1" (
    set apk_path=src\tests\hello_xr\build\outputs\apk\vulkan\debug\app-vulkan-debug.apk
    set package_name=org.khronos.openxr.hello_xr.vulkan
) else if "%choice%"=="2" (
    set apk_path=src\tests\hello_xr\build\outputs\apk\vulkan\release\app-vulkan-release.apk
    set package_name=org.khronos.openxr.hello_xr.vulkan
) else if "%choice%"=="3" (
    set apk_path=src\tests\hello_xr\build\outputs\apk\opengles\debug\app-opengles-debug.apk
    set package_name=org.khronos.openxr.hello_xr.opengles
) else if "%choice%"=="4" (
    set apk_path=src\tests\hello_xr\build\outputs\apk\opengles\release\app-opengles-release.apk
    set package_name=org.khronos.openxr.hello_xr.opengles
) else (
    echo Invalid choice
    pause
    exit /b 1
)

:: Uninstall existing app if present
echo Uninstalling existing app...
adb uninstall %package_name% >nul 2>&1

:: Install new APK
echo Installing APK...
adb install "%apk_path%"

if errorlevel 1 (
    echo Error: Failed to install APK
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation completed successfully!
echo ========================================
echo.

:: Verify installation
echo Verifying installation...
adb shell pm list packages | find "%package_name%"
if errorlevel 1 (
    echo Warning: App not found in package list
) else (
    echo App installed successfully!
)

echo.
echo Next steps:
echo 1. Start the test server: cd examples && python quest_test_server.py
echo 2. On your Quest device, find and launch the Hello XR app
echo 3. Check the logs: adb logcat ^| find "hello_xr"
echo.

:: Ask if user wants to start the app
set /p start_app="Do you want to start the app now? (y/n): "
if /i "%start_app%"=="y" (
    echo Starting Hello XR app...
    adb shell am start -n %package_name%/android.app.NativeActivity
    echo App started! Check your Quest device.
)

echo.
echo Deployment completed! Check META_QUEST_DEPLOYMENT_GUIDE.md for testing instructions.
pause 