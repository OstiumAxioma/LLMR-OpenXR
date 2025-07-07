# Quest设备测试服务器使用说明

## 🎯 功能概述

这个测试服务器专门用于测试Meta Quest设备的以下功能：

1. **📷 相机数据接收** - 接收Quest设备的相机环境信息（不包括UI，只包括摄像头获取的内容）
2. **🎤 麦克风数据接收** - 接收Quest设备的麦克风语音信息（只有麦克风，不包括其它虚拟声音）
3. **📝 文字消息通信** - 发送文字到Quest设备并确认Quest接收该文字数据成功

## 🚀 快速开始

### 方法1：使用启动脚本（推荐）

#### 启动服务器
```bash
# Windows
start_quest_test.bat

# 或手动启动
python quest_test_server.py --save-data
```

#### 启动测试客户端
```bash
# Windows
start_quest_client.bat

# 或手动启动
python quest_test_client.py
```

### 方法2：手动启动

#### 1. 安装依赖
```bash
pip install flask flask-cors opencv-python numpy requests
```

#### 2. 启动服务器
```bash
cd examples
python quest_test_server.py --save-data
```

#### 3. 测试服务器
```bash
# 在另一个终端中
python quest_test_client.py
```

## 📡 API接口

### 基础接口
- `GET /health` - 健康检查
- `GET /status` - 获取服务器状态

### 相机数据
- `POST /camera/frame` - 接收相机帧
- `GET /camera/frames` - 获取相机帧列表

### 音频数据
- `POST /audio/frame` - 接收音频帧
- `GET /audio/frames` - 获取音频帧列表

### 文字消息
- `POST /text/send` - 发送文字消息
- `POST /text/confirm` - 确认文字接收
- `GET /text/messages` - 获取文字消息列表

## 📊 数据格式

### 相机帧格式
```json
{
  "width": 1920,
  "height": 1080,
  "format": "RGB",
  "data": "base64编码的图像数据",
  "timestamp": "2024-01-15T10:30:00.123456"
}
```

### 音频帧格式
```json
{
  "sample_rate": 16000,
  "channels": 1,
  "format": "PCM",
  "data": "base64编码的音频数据",
  "duration_ms": 100.0,
  "timestamp": "2024-01-15T10:30:00.123456"
}
```

### 文字消息格式
```json
{
  "content": "要发送的文字消息"
}
```

## 💾 数据存储

如果启用了数据保存，数据将保存在以下目录：
```
quest_test_data/
├── camera/     # 相机帧图像 (.jpg)
├── audio/      # 音频帧文件 (.wav)
└── text/       # 文字消息 (.json)
```

## 🧪 测试方法

### 1. 基本测试
```bash
# 启动服务器
python quest_test_server.py --save-data

# 在另一个终端启动客户端
python quest_test_client.py
```

### 2. 手动测试
```bash
# 健康检查
curl http://localhost:9999/health

# 发送测试文字
curl -X POST http://localhost:9999/text/send \
  -H "Content-Type: application/json" \
  -d '{"content": "测试消息"}'
```

### 3. 监控数据
```bash
# 查看实时状态
curl http://localhost:9999/status

# 查看日志
tail -f quest_test_server.log
```

## 📁 文件说明

- `quest_test_server.py` - 主服务器程序
- `quest_test_client.py` - 测试客户端程序
- `start_quest_test.bat` - Windows服务器启动脚本
- `start_quest_client.bat` - Windows客户端启动脚本
- `QUEST_TEST_SERVER_README.md` - 详细文档

## 🔧 配置选项

### 命令行参数
```bash
python quest_test_server.py [选项]

选项:
  --port PORT         服务器端口 (默认: 9999)
  --save-data         保存接收到的数据到文件
  --no-save           不保存数据到文件
  -h, --help          显示帮助信息
```

### 客户端选项
```bash
python quest_test_client.py [选项]

选项:
  --server URL        服务器地址 (默认: http://localhost:9999)
  -h, --help          显示帮助信息
```

## 🐛 常见问题

### 1. 端口被占用
```bash
# 查找占用进程
netstat -ano | findstr :9999

# 杀死进程
taskkill /PID <进程ID> /F

# 或使用不同端口
python quest_test_server.py --port 9998
```

### 2. 依赖包缺失
```bash
pip install flask flask-cors opencv-python numpy requests
```

### 3. 网络连接问题
- 确保防火墙允许端口9999
- 检查网络连接
- 验证服务器IP地址

## 📈 性能指标

### 预期性能
- **相机帧率**: 30 FPS
- **音频帧率**: 100 FPS (10Hz)
- **文字消息**: 每5秒1条
- **内存使用**: < 500MB
- **CPU使用**: < 30%

### 监控命令
```bash
# 实时统计
curl http://localhost:9999/status | jq '.stats'

# 日志监控
tail -f quest_test_server.log
```

## 📚 详细文档

更多详细信息请参考：
- [QUEST_TEST_SERVER_README.md](QUEST_TEST_SERVER_README.md) - 完整API文档和配置说明

---

**注意**: 本服务器仅用于测试目的，不建议在生产环境中使用。 