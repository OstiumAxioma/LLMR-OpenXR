# 端口配置说明

## 📋 端口分配

为了避免端口冲突，不同服务器使用不同的端口：

### 🎯 现有服务器
- **相机后端服务器**: 端口 8888
  - 用于OpenXR项目的相机数据接收
  - 文件: `camera_backend_server.py` (如果存在)
  - 用途: 接收Quest设备的相机环境信息

### 🆕 新创建的服务器
- **Quest测试服务器**: 端口 9999
  - 用于测试Quest设备的完整功能
  - 文件: `quest_test_server.py`
  - 用途: 接收相机、音频和文字数据

## 🔧 端口配置

### Quest测试服务器配置
```bash
# 默认端口: 9999
python quest_test_server.py

# 自定义端口
python quest_test_server.py --port 9998

# 客户端连接
python quest_test_client.py --server http://localhost:9999
```

### 现有相机服务器配置
```bash
# 默认端口: 8888
python camera_backend_server.py

# 客户端连接
# 在OpenXR应用中使用端口8888
```

## 🚀 同时运行两个服务器

您可以同时运行两个服务器，它们使用不同的端口：

```bash
# 终端1: 启动现有相机服务器
python camera_backend_server.py --port 8888

# 终端2: 启动Quest测试服务器
python quest_test_server.py --port 9999

# 终端3: 启动Quest测试客户端
python quest_test_client.py --server http://localhost:9999
```

## 📊 端口使用情况

| 服务器 | 端口 | 状态 | 用途 |
|--------|------|------|------|
| 相机后端服务器 | 8888 | 现有 | 相机数据接收 |
| Quest测试服务器 | 9999 | 新建 | 完整功能测试 |

## 🔍 检查端口占用

### Windows
```bash
# 检查端口8888
netstat -ano | findstr :8888

# 检查端口9999
netstat -ano | findstr :9999
```

### Linux/Mac
```bash
# 检查端口8888
lsof -i :8888

# 检查端口9999
lsof -i :9999
```

## 🛠️ 修改端口配置

如果需要修改端口配置：

### 1. 修改Quest测试服务器端口
```bash
# 方法1: 命令行参数
python quest_test_server.py --port 9998

# 方法2: 修改代码中的默认值
# 在 quest_test_server.py 中修改默认端口
```

### 2. 修改客户端连接地址
```bash
# 方法1: 命令行参数
python quest_test_client.py --server http://localhost:9998

# 方法2: 修改代码中的默认值
# 在 quest_test_client.py 中修改默认地址
```

## 📝 注意事项

1. **端口冲突**: 确保不同服务器使用不同端口
2. **防火墙设置**: 确保防火墙允许相应端口
3. **网络配置**: 如果从其他设备访问，确保网络配置正确
4. **服务管理**: 建议使用不同的终端窗口管理不同服务器

## 🔄 迁移指南

如果您想将现有服务器迁移到新端口：

1. **备份现有配置**
2. **修改端口配置**
3. **更新客户端连接**
4. **测试功能**
5. **更新文档**

---

**总结**: Quest测试服务器使用端口9999，与现有的相机后端服务器（端口8888）不会冲突。 