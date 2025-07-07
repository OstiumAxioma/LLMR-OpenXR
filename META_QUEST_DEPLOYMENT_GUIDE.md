# Meta Quest OpenXR 部署指南

## 📋 概述

本指南将帮助你将OpenXR Hello_XR项目部署到Meta Quest设备并进行测试。

## 🛠️ 环境要求

### 必需软件
- **Android Studio** (最新版本)
- **Android SDK** (API 34)
- **Android NDK** (版本 23.2.8568313)
- **Meta Quest Developer Hub** (用于设备连接和调试)
- **ADB** (Android Debug Bridge)

### 硬件要求
- **Meta Quest 2/3/Pro** 设备
- **USB-C数据线** (用于设备连接)
- **开发者模式** 已启用

## 🔧 构建配置

### 1. 项目结构确认
```
OpenXR-SDK-Source/
├── src/tests/hello_xr/          # Hello_XR应用
│   ├── build.gradle             # Android构建配置
│   ├── AndroidManifest.xml      # Android清单文件
│   ├── CMakeLists.txt           # CMake构建配置
│   └── ...
├── examples/                    # 测试服务器
│   ├── quest_test_server.py     # Quest测试服务器
│   └── quest_test_client.py     # Quest测试客户端
└── ...
```

### 2. 构建配置检查

#### build.gradle 关键配置
```gradle
android {
    compileSdk 34
    ndkVersion "23.2.8568313"
    buildToolsVersion = "34.0.0"
    
    defaultConfig {
        minSdkVersion 24          // Quest要求最低API 24
        targetSdkVersion 34
        // ...
    }
}
```

#### AndroidManifest.xml 关键权限
```xml
<!-- OpenXR权限 -->
<uses-permission android:name="org.khronos.openxr.permission.OPENXR" />
<uses-permission android:name="org.khronos.openxr.permission.OPENXR_SYSTEM" />

<!-- VR头显追踪 -->
<uses-feature
    android:name="android.hardware.vr.headtracking"
    android:required="false"
    android:version="1" />
```

## 🚀 构建步骤

### 方法1: 使用Android Studio

1. **打开项目**
   ```bash
   # 在Android Studio中打开
   File -> Open -> 选择 src/tests/hello_xr 目录
   ```

2. **同步项目**
   - 等待Gradle同步完成
   - 确保所有依赖下载成功

3. **选择构建变体**
   - 选择 `Vulkan` 或 `OpenGLES` 变体
   - 推荐使用 `Vulkan` 变体以获得更好性能

4. **构建APK**
   - Build -> Build Bundle(s) / APK(s) -> Build APK(s)
   - 等待构建完成

### 方法2: 使用命令行

1. **进入项目目录**
   ```bash
   cd src/tests/hello_xr
   ```

2. **构建Vulkan版本**
   ```bash
   ./gradlew assembleVulkanDebug
   ```

3. **构建OpenGLES版本**
   ```bash
   ./gradlew assembleOpenGLESDebug
   ```

## 📱 设备准备

### 1. 启用开发者模式

1. **在Quest设备上**
   - 打开设置
   - 进入"关于"页面
   - 连续点击"版本号"7次
   - 启用开发者模式

2. **在Meta Quest Developer Hub中**
   - 连接设备
   - 确认设备状态为"已连接"

### 2. 设备连接

1. **USB连接**
   ```bash
   # 检查设备连接
   adb devices
   ```

2. **无线连接** (可选)
   ```bash
   # 启用无线调试
   adb tcpip 5555
   adb connect <设备IP>:5555
   ```

## 📦 部署步骤

### 1. 安装APK

```bash
# 安装Vulkan版本
adb install app-vulkan-debug.apk

# 或安装OpenGLES版本
adb install app-opengles-debug.apk
```

### 2. 验证安装

```bash
# 检查应用是否安装成功
adb shell pm list packages | grep openxr

# 应该看到: org.khronos.openxr.hello_xr.vulkan
# 或: org.khronos.openxr.hello_xr.opengles
```

## 🧪 测试流程

### 1. 启动测试服务器

```bash
# 在开发机器上启动服务器
cd examples
python quest_test_server.py --save-data
```

### 2. 配置网络连接

确保Quest设备和开发机器在同一网络：

```bash
# 获取开发机器IP
ipconfig  # Windows
ifconfig  # Linux/Mac

# 在Quest上测试连接
adb shell ping <开发机器IP>
```

### 3. 运行Hello_XR应用

1. **在Quest设备上**
   - 打开应用库
   - 找到"Hello XR (Vulkan)"或"Hello XR (OpenGL ES)"
   - 启动应用

2. **观察应用行为**
   - 应该显示OpenXR初始化信息
   - 显示3D场景和控制器
   - 检查日志输出

### 4. 查看日志

```bash
# 实时查看应用日志
adb logcat | grep hello_xr

# 或查看OpenXR相关日志
adb logcat | grep -i openxr
```

## 🔍 测试检查清单

### ✅ 基础功能测试
- [ ] 应用成功安装
- [ ] 应用正常启动
- [ ] OpenXR运行时初始化成功
- [ ] 图形API (Vulkan/OpenGLES) 正常工作
- [ ] 头显追踪功能正常
- [ ] 控制器输入响应正常

### ✅ 性能测试
- [ ] 帧率稳定 (60+ FPS)
- [ ] 延迟低 (<20ms)
- [ ] 内存使用合理
- [ ] 电池消耗正常

### ✅ 集成测试
- [ ] 与测试服务器通信正常
- [ ] 相机数据采集正常
- [ ] 音频数据采集正常
- [ ] 文字消息功能正常

## 🐛 常见问题解决

### 构建问题

1. **NDK版本不匹配**
   ```bash
   # 在build.gradle中确认NDK版本
   ndkVersion "23.2.8568313"
   ```

2. **依赖下载失败**
   ```bash
   # 清理并重新同步
   ./gradlew clean
   ./gradlew --refresh-dependencies
   ```

### 部署问题

1. **设备未识别**
   ```bash
   # 重新连接设备
   adb kill-server
   adb start-server
   adb devices
   ```

2. **权限问题**
   ```bash
   # 重新安装应用
   adb uninstall org.khronos.openxr.hello_xr.vulkan
   adb install app-vulkan-debug.apk
   ```

### 运行时问题

1. **OpenXR初始化失败**
   - 检查设备是否支持OpenXR
   - 确认Meta Quest运行时已安装

2. **图形API错误**
   - 尝试切换Vulkan/OpenGLES版本
   - 检查设备驱动更新

## 📊 性能基准

### 预期性能指标
- **启动时间**: <5秒
- **帧率**: 60-90 FPS
- **延迟**: <20ms
- **内存使用**: <200MB
- **CPU使用**: <30%

### 测试工具
```bash
# 性能监控
adb shell dumpsys gfxinfo org.khronos.openxr.hello_xr.vulkan

# 内存使用
adb shell dumpsys meminfo org.khronos.openxr.hello_xr.vulkan
```

## 🔗 相关资源

- [OpenXR官方文档](https://www.khronos.org/openxr/)
- [Meta Quest开发者文档](https://developer.oculus.com/)
- [Android NDK文档](https://developer.android.com/ndk)
- [Vulkan文档](https://www.khronos.org/vulkan/)

## 📝 测试记录模板

### 测试日期: _____________
### 测试设备: _____________
### 测试版本: _____________
### 构建变体: _____________

### 测试结果
- [ ] 基础功能测试通过
- [ ] 性能测试通过
- [ ] 集成测试通过

### 问题记录
- 问题1: _____________
- 解决方案: _____________

### 下次测试注意事项
- _____________
- _____________ 