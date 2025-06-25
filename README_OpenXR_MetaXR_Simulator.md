# OpenXR hello_xr + Meta XR Simulator 使用指南

本项目记录如何在 Windows 环境下编译 Khronos 官方的 OpenXR 示例项目 `hello_xr`，并通过 **Meta XR Simulator**（无需实体 Quest 设备）完成模拟运行测试。

---

## ✅ 系统要求

- Windows 10 / 11 64-bit
- Visual Studio 2022（安装时勾选 “使用 C++ 的桌面开发”）
- CMake ≥ 3.22
- Git
- Vulkan SDK ≥ 1.3（推荐：1.4.313.2）  
  👉 [下载地址](https://vulkan.lunarg.com/sdk/home)
- Meta XR Simulator 已解压至：
  ```
  C:\Users\<用户名>\AppData\Local\MetaXR\MetaXrSimulator\77\
  ```

---

## 📦 安装 Vulkan SDK

安装后应自动设置环境变量 `VULKAN_SDK`，你可验证：

```powershell
echo $env:VULKAN_SDK
# 应输出：C:\VulkanSDK\1.4.313.2\
```

---

## 🧱 编译 hello_xr 示例项目

### 1. 克隆源码

```bash
git clone https://github.com/KhronosGroup/OpenXR-SDK-Source.git
cd OpenXR-SDK-Source
```

### 2. 创建 build 目录

```bash
rmdir /s /q build
mkdir build
cd build
```

### 3. 配置 CMake（显式指定 Vulkan SDK 路径）

```bash
cmake .. -G "Visual Studio 17 2022" -A x64 ^
  -DBUILD_TESTS=ON ^
  -DBUILD_LOADER=ON ^
  -DVulkan_INCLUDE_DIR="C:/VulkanSDK/1.4.313.2/Include" ^
  -DVulkan_LIBRARY="C:/VulkanSDK/1.4.313.2/Lib/vulkan-1.lib"
```

### 4. 编译 Release 版本

```bash
cmake --build . --config Release
```

---

## 🧰 设置 Meta XR Simulator 为 OpenXR Runtime

### 注册模拟器为系统默认运行时：

```powershell
reg add "HKLM\SOFTWARE\Khronos\OpenXR\1" /v ActiveRuntime /t REG_SZ /d "C:\Users\<你的用户名>\AppData\Local\MetaXR\MetaXrSimulator\77\meta_openxr_simulator.json" /f
```

确认设置成功：

```powershell
reg query "HKLM\SOFTWARE\Khronos\OpenXR\1"
```

---

## 🚀 运行 hello_xr 示例

进入编译输出目录：

```bash
cd src\tests\hello_xr\Release
.\hello_xr.exe -g Vulkan
```

---

## ✅ 运行成功标志

- 控制台输出：

  ```
  Using OpenXR runtime: Meta
  Press any key to shutdown...
  ```

- 出现窗口：灰背景、头部追踪、控制器模拟

- 任务管理器中存在：

  ```
  SceneRecorderServer.exe
  SyntheticEnvironmentServer.exe
  ```

---

## 🔁 如需恢复 Quest Runtime（若你未来连接真机）

```powershell
reg add "HKLM\SOFTWARE\Khronos\OpenXR\1" /v ActiveRuntime /t REG_SZ /d "C:\Program Files\Oculus\Support\oculus-runtime\oculus_openxr_64.json" /f
```

---

## 📌 附加说明

- 示例程序只支持指定已启用图形后端（如 Vulkan），运行前请确保你已使用 Vulkan 构建。
- Meta XR Simulator 不支持 OpenGL。
- 如运行时仍提示 `Unsupported graphics API 'Vulkan'`，请确认你使用的是包含 Vulkan 模块构建的 `hello_xr.exe`。

---

## ✨ 接下来你可以...

- 加入自定义场景/对话
- 集成 Gemini、RAG 或其他 AI 对话逻辑
- 构建你自己的 XR 应用原型（无需实体 Quest）
