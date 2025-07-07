Write-Host "========================================" -ForegroundColor Green
Write-Host "Android Environment Setup Script" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Check if Android Studio is installed
Write-Host "Checking for Android Studio installation..." -ForegroundColor Yellow

# Common Android Studio installation paths
$androidStudioPaths = @(
    "C:\Program Files\Android\Android Studio",
    "C:\Program Files (x86)\Android\Android Studio",
    "$env:LOCALAPPDATA\Google\AndroidStudio",
    "$env:USERPROFILE\AppData\Local\Google\AndroidStudio"
)

# Common Android SDK paths
$androidSdkPaths = @(
    "$env:LOCALAPPDATA\Android\Sdk",
    "$env:USERPROFILE\AppData\Local\Android\Sdk",
    "C:\Android\Sdk",
    "C:\Users\$env:USERNAME\AppData\Local\Android\Sdk"
)

# Find Android Studio
$androidStudioFound = $false
foreach ($path in $androidStudioPaths) {
    if (Test-Path $path) {
        Write-Host "Found Android Studio at: $path" -ForegroundColor Green
        $androidStudioFound = $true
        break
    }
}

if (-not $androidStudioFound) {
    Write-Host ""
    Write-Host "Android Studio not found in common locations." -ForegroundColor Red
    Write-Host "Please install Android Studio first:" -ForegroundColor Yellow
    Write-Host "1. Download from: https://developer.android.com/studio" -ForegroundColor Yellow
    Write-Host "2. Run the installer" -ForegroundColor Yellow
    Write-Host "3. Complete the setup wizard" -ForegroundColor Yellow
    Write-Host "4. Run this script again" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to continue"
    exit 1
}

# Find Android SDK
$androidSdkFound = $false
$androidSdkPath = ""
foreach ($path in $androidSdkPaths) {
    if (Test-Path $path) {
        Write-Host "Found Android SDK at: $path" -ForegroundColor Green
        $androidSdkPath = $path
        $androidSdkFound = $true
        break
    }
}

if (-not $androidSdkFound) {
    Write-Host ""
    Write-Host "Android SDK not found. Please:" -ForegroundColor Red
    Write-Host "1. Open Android Studio" -ForegroundColor Yellow
    Write-Host "2. Go to File -> Settings -> Appearance & Behavior -> System Settings -> Android SDK" -ForegroundColor Yellow
    Write-Host "3. Note the Android SDK Location path" -ForegroundColor Yellow
    Write-Host "4. Run this script again" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to continue"
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Setting up environment variables..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# Set ANDROID_HOME
try {
    [Environment]::SetEnvironmentVariable("ANDROID_HOME", $androidSdkPath, "User")
    Write-Host "ANDROID_HOME set to: $androidSdkPath" -ForegroundColor Green
} catch {
    Write-Host "Error: Failed to set ANDROID_HOME" -ForegroundColor Red
    Read-Host "Press Enter to continue"
    exit 1
}

# Add platform-tools to PATH
try {
    $currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
    $platformToolsPath = "$androidSdkPath\platform-tools"
    if ($currentPath -notlike "*$platformToolsPath*") {
        $newPath = "$currentPath;$platformToolsPath"
        [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
        Write-Host "Added platform-tools to PATH" -ForegroundColor Green
    } else {
        Write-Host "platform-tools already in PATH" -ForegroundColor Yellow
    }
} catch {
    Write-Host "Error: Failed to update PATH with platform-tools" -ForegroundColor Red
}

# Add tools to PATH
try {
    $currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
    $toolsPath = "$androidSdkPath\tools"
    if ($currentPath -notlike "*$toolsPath*") {
        $newPath = "$currentPath;$toolsPath"
        [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
        Write-Host "Added tools to PATH" -ForegroundColor Green
    } else {
        Write-Host "tools already in PATH" -ForegroundColor Yellow
    }
} catch {
    Write-Host "Error: Failed to update PATH with tools" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Environment setup completed!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "ANDROID_HOME set to: $androidSdkPath" -ForegroundColor Cyan
Write-Host "PATH updated with platform-tools and tools" -ForegroundColor Cyan
Write-Host ""
Write-Host "Please restart your terminal/PowerShell" -ForegroundColor Yellow
Write-Host "for the changes to take effect." -ForegroundColor Yellow
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Restart your terminal" -ForegroundColor Yellow
Write-Host "2. Run: adb version (to verify ADB is available)" -ForegroundColor Yellow
Write-Host "3. Run: .\build_android.bat (to build the APK)" -ForegroundColor Yellow
Write-Host ""

Read-Host "Press Enter to continue" 