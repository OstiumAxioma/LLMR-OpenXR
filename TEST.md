# OpenXR Hello_XR 完整测试流程

## 📋 测试环境准备

### 必需软件
- ✅ Android Studio (已安装)
- ✅ Android SDK (已配置)
- ✅ Java JDK (已安装)
- ✅ Python 3.x (已安装)
- ✅ ADB (已配置)

### 环境变量
```cmd
ANDROID_HOME=C:\Users\Ostiu\AppData\Local\Android\Sdk
```

## 🏗️ 第一步：构建APK

### 1.1 进入项目根目录
```cmd
cd E:\Desktop\LLARDemo\OpenXR-SDK-Source
```

### 1.2 运行构建脚本
```cmd
.\build_android.bat
```

### 1.3 选择构建变体
- 选择 `1` (Vulkan Debug) - 推荐用于测试

### 1.4 构建输出
```
BUILD SUCCESSFUL in 3m 34s
39 actionable tasks: 39 executed
```

### 1.5 APK文件位置
```
src\tests\hello_xr\build\outputs\apk\vulkan\debug\hello_xr-Vulkan-debug.apk
```

## 📱 第二步：安装APK到Quest设备

### 2.1 连接Quest设备
- 通过USB连接Meta Quest设备
- 确保设备已启用开发者模式
- 确认ADB连接正常

### 2.2 安装APK
```cmd
adb install src\tests\hello_xr\build\outputs\apk\vulkan\debug\hello_xr-Vulkan-debug.apk
```

### 2.3 安装输出
```
Performing Streamed Install
Success
```

## 🖥️ 第三步：启动测试服务器

### 3.1 进入examples目录
```cmd
cd examples
```

### 3.2 启动测试服务器
```cmd
.\start_quest_test.bat
```

### 3.3 服务器信息
- 端口: 8888
- 健康检查: http://localhost:8888/health
- 状态页面: http://localhost:8888/status
- 数据保存: 启用

## 🎮 第四步：在Quest上运行应用

### 4.1 启动应用
- 在Quest设备上找到"Hello XR (Vulkan)"应用
- 点击启动应用

### 4.2 观察应用行为
- OpenXR初始化
- 3D场景显示
- 相机系统初始化
- 与测试服务器通信

## 📊 第五步：验证测试结果

### 5.1 检查服务器日志
```
2025-07-07 08:48:04,248 - INFO - Processed audio frame: 16000Hz, channels: 1, duration: 100.0ms, size: 3200 bytes
2025-07-07 08:48:04,358 - INFO - Processed camera frame: 1920x1080, format: RGB, size: 6220800 bytes
2025-07-07 08:48:04,248 - INFO - Sent text message: msg_000000, content: Test message #1
```

### 5.2 检查数据文件
```
examples/quest_test_data/
├── camera_frames/
│   ├── frame_001.jpg
│   ├── frame_002.jpg
│   └── ...
├── audio_frames/
│   ├── audio_001.wav
│   ├── audio_002.wav
│   └── ...
└── text_messages/
    ├── msg_000000.txt
    ├── msg_000001.txt
    └── ...
```

### 5.3 验证功能
- ✅ 相机帧数据接收正常
- ✅ 音频帧数据接收正常
- ✅ 文字消息发送正常
- ✅ 图像质量符合预期
- ✅ 音频质量符合预期

## 🔧 故障排除

### 构建问题
- **Gradle下载失败**: 使用本地Gradle，避免网络问题
- **Android SDK未找到**: 检查ANDROID_HOME环境变量
- **编译错误**: 检查依赖和配置

### 安装问题
- **设备未连接**: 检查USB连接和开发者模式
- **权限错误**: 确保设备已授权ADB调试
- **安装失败**: 检查APK文件完整性

### 服务器问题
- **端口冲突**: 检查8888端口是否被占用
- **Python依赖**: 运行 `pip install flask requests`
- **网络连接**: 确保Quest设备能访问服务器IP

### 应用问题
- **OpenXR初始化失败**: 检查Quest系统版本
- **相机权限**: 确保应用有相机访问权限
- **网络通信**: 检查防火墙设置

## 📝 测试记录

### 测试日期: 2025-07-07
### 测试环境: Windows 10 + Meta Quest
### 测试结果: ✅ 成功
### 问题记录: 
- 初始版本无法退出应用
- 初始版本是纯VR，没有相机访问功能
- 已修复：添加了退出机制和相机权限

### 性能数据
- 构建时间: 6秒（增量构建）
- APK大小: ~XX MB
- 启动时间: ~X秒
- 帧率: 60+ FPS

### 修复内容
- ✅ 添加了相机权限（AndroidManifest.xml）
- ✅ 改进了退出机制（30秒超时 + 控制器退出）
- ✅ 添加了应用销毁时的退出处理
- ✅ 为MR功能预留了相机访问接口
- ⚠️ 尝试移除青灰色背景失败，导致程序卡死
- ✅ 已回滚到安全状态，应用可以正常启动

## 🔄 下次测试注意事项

1. 确保所有环境变量正确设置
2. 检查Quest设备电量充足
3. 验证网络连接稳定
4. 准备测试数据对比

---

**最后更新**: 2025-07-07
**测试状态**: 完成
**下次测试**: _____________ 