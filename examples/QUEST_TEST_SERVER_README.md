# Quest设备测试服务器文档

## 📋 概述

Quest设备测试服务器是一个专门用于测试Meta Quest设备功能的Python服务器，支持以下核心功能：

1. **相机数据接收** - 接收Quest设备的相机环境信息（不包括UI，只包括摄像头获取的内容）
2. **麦克风数据接收** - 接收Quest设备的麦克风语音信息（只有麦克风，不包括其它虚拟声音）
3. **文字消息通信** - 发送文字到Quest设备并确认Quest接收该文字数据成功

## 🚀 快速开始

### 1. 环境准备

#### 安装Python依赖
```bash
pip install flask flask-cors opencv-python numpy requests
```

#### 验证安装
```bash
python -c "import flask, cv2, numpy, requests; print('依赖安装成功')"
```

### 2. 启动服务器

#### 基本启动
```bash
cd examples
python quest_test_server.py
```

#### 带参数启动
```bash
# 指定端口
python quest_test_server.py --port 9999

# 保存数据到文件
python quest_test_server.py --save-data

# 不保存数据
python quest_test_server.py --no-save
```

### 3. 测试服务器

#### 使用测试客户端
```bash
# 在另一个终端中运行
python quest_test_client.py
```

#### 手动测试
```bash
# 健康检查
curl http://localhost:9999/health

# 获取状态
curl http://localhost:9999/status
```

## 📡 API接口文档

### 基础接口

#### 健康检查
```
GET /health
```
**响应示例：**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.123456",
  "uptime": 3600.5,
  "stats": {
    "camera_frames": 100,
    "audio_frames": 1000,
    "text_messages": 20,
    "camera_bytes": 622080000,
    "audio_bytes": 32000000,
    "last_camera_frame": "2024-01-15T10:29:59.123456",
    "last_audio_frame": "2024-01-15T10:29:59.987654",
    "last_text_message": "2024-01-15T10:29:55.123456"
  }
}
```

#### 获取服务器状态
```
GET /status
```
**响应示例：**
```json
{
  "camera_frames": 100,
  "audio_frames": 1000,
  "text_messages": 20,
  "stats": { ... },
  "save_data": true
}
```

### 相机数据接口

#### 接收相机帧
```
POST /camera/frame
```
**请求体：**
```json
{
  "width": 1920,
  "height": 1080,
  "format": "RGB",
  "data": "base64编码的图像数据",
  "timestamp": "2024-01-15T10:30:00.123456"
}
```
**响应：**
```json
{
  "status": "success",
  "frame_id": 100,
  "timestamp": "2024-01-15T10:30:00.123456"
}
```

#### 获取相机帧列表
```
GET /camera/frames?limit=10
```
**响应：**
```json
[
  {
    "timestamp": "2024-01-15T10:30:00.123456",
    "width": 1920,
    "height": 1080,
    "format": "RGB",
    "data": "base64编码的数据",
    "frame_id": 100
  }
]
```

### 音频数据接口

#### 接收音频帧
```
POST /audio/frame
```
**请求体：**
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
**响应：**
```json
{
  "status": "success",
  "frame_id": 1000,
  "timestamp": "2024-01-15T10:30:00.123456"
}
```

#### 获取音频帧列表
```
GET /audio/frames?limit=10
```
**响应：**
```json
[
  {
    "timestamp": "2024-01-15T10:30:00.123456",
    "sample_rate": 16000,
    "channels": 1,
    "format": "PCM",
    "data": "base64编码的数据",
    "duration_ms": 100.0,
    "frame_id": 1000
  }
]
```

### 文字消息接口

#### 发送文字消息
```
POST /text/send
```
**请求体：**
```json
{
  "content": "要发送的文字消息"
}
```
**响应：**
```json
{
  "status": "success",
  "message_id": "msg_000001",
  "timestamp": "2024-01-15T10:30:00.123456"
}
```

#### 确认文字接收
```
POST /text/confirm
```
**请求体：**
```json
{
  "message_id": "msg_000001",
  "status": "delivered"  // delivered, read
}
```
**响应：**
```json
{
  "status": "success",
  "message_id": "msg_000001",
  "new_status": "delivered"
}
```

#### 获取文字消息列表
```
GET /text/messages?limit=10
```
**响应：**
```json
[
  {
    "timestamp": "2024-01-15T10:30:00.123456",
    "message_id": "msg_000001",
    "content": "测试消息",
    "status": "read"
  }
]
```

## 📊 数据格式说明

### 相机数据格式

#### 支持的格式
- **RGB**: 24位RGB格式，每个像素3字节
- **BGR**: 24位BGR格式，每个像素3字节
- **YUV**: YUV格式（需要特殊处理）

#### 数据编码
- 图像数据使用base64编码传输
- 服务器会自动解码并保存为JPEG格式

#### 推荐参数
- **分辨率**: 1920x1080 (推荐)
- **帧率**: 30 FPS
- **格式**: RGB

### 音频数据格式

#### 支持的格式
- **PCM**: 原始PCM音频数据
- **WAV**: WAV格式（服务器会自动转换）

#### 推荐参数
- **采样率**: 16000 Hz (16kHz)
- **通道数**: 1 (单声道)
- **位深度**: 16位
- **帧长度**: 100ms

#### 数据编码
- 音频数据使用base64编码传输
- 服务器会自动解码并保存为WAV格式

### 文字消息格式

#### 消息状态
- **sent**: 已发送
- **delivered**: 已送达
- **read**: 已读

#### 消息ID格式
- 格式: `msg_XXXXXX` (6位数字)
- 示例: `msg_000001`, `msg_000123`

## 💾 数据存储

### 存储目录结构
```
quest_test_data/
├── camera/           # 相机帧图像
│   ├── camera_frame_000001_2024-01-15T10-30-00.jpg
│   └── ...
├── audio/            # 音频帧文件
│   ├── audio_frame_000001_2024-01-15T10-30-00.wav
│   └── ...
└── text/             # 文字消息
    ├── text_message_msg_000001_2024-01-15T10-30-00.json
    └── ...
```

### 文件命名规则
- **相机帧**: `camera_frame_{frame_id:06d}_{timestamp}.jpg`
- **音频帧**: `audio_frame_{frame_id:06d}_{timestamp}.wav`
- **文字消息**: `text_message_{message_id}_{timestamp}.json`

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

### 环境变量
```bash
# 设置服务器端口
export QUEST_SERVER_PORT=9999

# 设置数据保存路径
export QUEST_DATA_DIR=/path/to/data

# 设置日志级别
export QUEST_LOG_LEVEL=INFO
```

## 🧪 测试工具

### 测试客户端
```bash
# 启动测试客户端
python quest_test_client.py

# 指定服务器地址
python quest_test_client.py --server http://192.168.1.100:9999
```

### 手动测试命令
```bash
# 测试健康检查
curl http://localhost:9999/health

# 测试相机帧发送
curl -X POST http://localhost:9999/camera/frame \
  -H "Content-Type: application/json" \
  -d '{"width": 640, "height": 480, "format": "RGB", "data": "..."}'

# 测试音频帧发送
curl -X POST http://localhost:9999/audio/frame \
  -H "Content-Type: application/json" \
  -d '{"sample_rate": 16000, "channels": 1, "format": "PCM", "data": "..."}'

# 测试文字消息发送
curl -X POST http://localhost:9999/text/send \
  -H "Content-Type: application/json" \
  -d '{"content": "测试消息"}'
```

## 📈 性能监控

### 实时统计
```bash
# 获取实时统计信息
curl http://localhost:9999/status | jq '.stats'

# 监控相机帧率
watch -n 1 'curl -s http://localhost:9999/status | jq ".stats.camera_frames"'

# 监控音频帧率
watch -n 1 'curl -s http://localhost:9999/status | jq ".stats.audio_frames"'
```

### 日志监控
```bash
# 查看实时日志
tail -f quest_test_server.log

# 过滤相机相关日志
tail -f quest_test_server.log | grep "相机"

# 过滤音频相关日志
tail -f quest_test_server.log | grep "音频"
```

## 🐛 故障排除

### 常见问题

#### 1. 服务器启动失败
**问题**: `Address already in use`
**解决**: 
```bash
# 查找占用端口的进程
netstat -ano | findstr :9999

# 杀死进程
taskkill /PID <进程ID> /F

# 或使用不同端口
python quest_test_server.py --port 9998
```

#### 2. 依赖包缺失
**问题**: `ModuleNotFoundError`
**解决**:
```bash
pip install flask flask-cors opencv-python numpy requests
```

#### 3. 数据保存失败
**问题**: 权限错误或磁盘空间不足
**解决**:
```bash
# 检查磁盘空间
df -h

# 检查目录权限
ls -la quest_test_data/

# 使用不同目录
export QUEST_DATA_DIR=/tmp/quest_data
```

#### 4. 网络连接问题
**问题**: Quest设备无法连接到服务器
**解决**:
```bash
# 检查防火墙设置
# 确保端口9999未被阻止

# 检查网络连接
ping <服务器IP>

# 测试端口连通性
telnet <服务器IP> 9999
```

### 调试模式
```bash
# 启用详细日志
export QUEST_LOG_LEVEL=DEBUG

# 启动服务器
python quest_test_server.py
```

## 📚 扩展开发

### 添加新的数据格式支持
1. 在`parse_camera_frame`或`parse_audio_frame`中添加新格式处理
2. 在`save_camera_frame`或`save_audio_frame`中添加新格式保存逻辑
3. 更新API文档

### 添加新的API端点
1. 在`register_routes`中添加新的路由
2. 实现对应的处理函数
3. 更新文档和测试

### 集成到Quest应用
1. 在Quest应用中实现HTTP客户端
2. 按照API格式发送数据
3. 处理服务器响应

## 📄 许可证

本项目基于Apache 2.0许可证开源。

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个测试服务器。

---

**注意**: 本服务器仅用于测试目的，不建议在生产环境中使用。 