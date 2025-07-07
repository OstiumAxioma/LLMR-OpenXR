#!/usr/bin/env python3
"""
Quest Device Test Server
Specialized for testing Meta Quest device camera, microphone and text communication functions

Features:
1. Receive Quest device camera environment information
2. Receive Quest device microphone audio information  
3. Send text to Quest device and confirm successful reception
"""

import argparse
import json
import logging
import os
import time
import threading
import wave
import base64
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict

try:
    from flask import Flask, request, jsonify, Response
    from flask_cors import CORS
    import cv2
    import numpy as np
except ImportError as e:
    print(f"缺少依赖包: {e}")
    print("请安装: pip install flask flask-cors opencv-python numpy")
    exit(1)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('quest_test_server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class CameraFrame:
    """Camera frame data structure"""
    timestamp: str
    width: int
    height: int
    format: str  # RGB, BGR, YUV, etc.
    data: bytes
    frame_id: int

@dataclass
class AudioFrame:
    """Audio frame data structure"""
    timestamp: str
    sample_rate: int
    channels: int
    format: str  # PCM, WAV, etc.
    data: bytes
    duration_ms: float
    frame_id: int

@dataclass
class TextMessage:
    """Text message structure"""
    timestamp: str
    message_id: str
    content: str
    status: str  # sent, delivered, read

class QuestTestServer:
    def __init__(self, port: int = 8888, save_data: bool = False):
        self.port = port
        self.save_data = save_data
        self.start_time = time.time()
        
        # Data storage
        self.camera_frames: List[CameraFrame] = []
        self.audio_frames: List[AudioFrame] = []
        self.text_messages: List[TextMessage] = []
        
        # Counters
        self.camera_frame_count = 0
        self.audio_frame_count = 0
        self.text_message_count = 0
        
        # Create save directories
        if self.save_data:
            self.data_dir = Path("quest_test_data")
            self.data_dir.mkdir(exist_ok=True)
            
            self.camera_dir = self.data_dir / "camera"
            self.audio_dir = self.data_dir / "audio"
            self.text_dir = self.data_dir / "text"
            
            self.camera_dir.mkdir(exist_ok=True)
            self.audio_dir.mkdir(exist_ok=True)
            self.text_dir.mkdir(exist_ok=True)
            
            logger.info(f"Data will be saved to: {self.data_dir.absolute()}")
        
        # Initialize Flask application
        self.app = Flask(__name__)
        CORS(self.app)  # Allow cross-origin requests
        
        # Register routes
        self.register_routes()
        
        # Statistics
        self.stats = {
            "camera_frames": 0,
            "audio_frames": 0,
            "text_messages": 0,
            "camera_bytes": 0,
            "audio_bytes": 0,
            "uptime": 0.0,
            "last_camera_frame": None,
            "last_audio_frame": None,
            "last_text_message": None
        }
    
    def register_routes(self):
        """Register API routes"""
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            """Health check"""
            self.stats["uptime"] = time.time() - self.start_time
            return jsonify({
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "uptime": self.stats["uptime"],
                "stats": self.stats
            })
        
        @self.app.route('/camera/frame', methods=['POST'])
        def receive_camera_frame():
            """Receive Quest camera frame data"""
            try:
                # Get request data
                data = request.get_json()
                if not data:
                    return jsonify({"error": "No JSON data received"}), 400
                
                # Parse camera frame data
                camera_frame = self.parse_camera_frame(data)
                if camera_frame is None:
                    return jsonify({"error": "Invalid camera frame data"}), 400
                
                # Process camera frame data
                self.process_camera_frame(camera_frame)
                
                # Update statistics
                self.update_camera_stats(len(camera_frame.data))
                
                return jsonify({
                    "status": "success",
                    "frame_id": camera_frame.frame_id,
                    "timestamp": camera_frame.timestamp
                })
                
            except Exception as e:
                logger.error(f"Error processing camera frame data: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/audio/frame', methods=['POST'])
        def receive_audio_frame():
            """Receive Quest microphone audio data"""
            try:
                # Get request data
                data = request.get_json()
                if not data:
                    return jsonify({"error": "No JSON data received"}), 400
                
                # Parse audio frame data
                audio_frame = self.parse_audio_frame(data)
                if audio_frame is None:
                    return jsonify({"error": "Invalid audio frame data"}), 400
                
                # Process audio frame data
                self.process_audio_frame(audio_frame)
                
                # Update statistics
                self.update_audio_stats(len(audio_frame.data))
                
                return jsonify({
                    "status": "success",
                    "frame_id": audio_frame.frame_id,
                    "timestamp": audio_frame.timestamp
                })
                
            except Exception as e:
                logger.error(f"Error processing audio frame data: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/text/send', methods=['POST'])
        def send_text_message():
            """Send text message to Quest device"""
            try:
                data = request.get_json()
                if not data:
                    return jsonify({"error": "No JSON data received"}), 400
                
                content = data.get('content')
                if not content:
                    return jsonify({"error": "No content provided"}), 400
                
                # Create text message
                message = TextMessage(
                    timestamp=datetime.now().isoformat(),
                    message_id=f"msg_{self.text_message_count:06d}",
                    content=content,
                    status="sent"
                )
                
                # Process text message
                self.process_text_message(message)
                
                return jsonify({
                    "status": "success",
                    "message_id": message.message_id,
                    "timestamp": message.timestamp
                })
                
            except Exception as e:
                logger.error(f"Error sending text message: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/text/confirm', methods=['POST'])
        def confirm_text_received():
            """Confirm Quest device received text message"""
            try:
                data = request.get_json()
                if not data:
                    return jsonify({"error": "No JSON data received"}), 400
                
                message_id = data.get('message_id')
                status = data.get('status', 'delivered')  # delivered, read
                
                if not message_id:
                    return jsonify({"error": "No message_id provided"}), 400
                
                # Update message status
                self.update_text_message_status(message_id, status)
                
                return jsonify({
                    "status": "success",
                    "message_id": message_id,
                    "new_status": status
                })
                
            except Exception as e:
                logger.error(f"Error confirming text message: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/status', methods=['GET'])
        def get_status():
            """Get server status"""
            return jsonify({
                "camera_frames": len(self.camera_frames),
                "audio_frames": len(self.audio_frames),
                "text_messages": len(self.text_messages),
                "stats": self.stats,
                "save_data": self.save_data
            })
        
        @self.app.route('/camera/frames', methods=['GET'])
        def get_camera_frames():
            """Get camera frames list"""
            limit = request.args.get('limit', 10, type=int)
            frames = self.camera_frames[-limit:] if self.camera_frames else []
            return jsonify([asdict(frame) for frame in frames])
        
        @self.app.route('/audio/frames', methods=['GET'])
        def get_audio_frames():
            """Get audio frames list"""
            limit = request.args.get('limit', 10, type=int)
            frames = self.audio_frames[-limit:] if self.audio_frames else []
            return jsonify([asdict(frame) for frame in frames])
        
        @self.app.route('/text/messages', methods=['GET'])
        def get_text_messages():
            """Get text messages list"""
            limit = request.args.get('limit', 10, type=int)
            messages = self.text_messages[-limit:] if self.text_messages else []
            return jsonify([asdict(msg) for msg in messages])
    
    def parse_camera_frame(self, data: Dict[str, Any]) -> Optional[CameraFrame]:
        """Parse camera frame data"""
        try:
            # Check required fields
            required_fields = ['width', 'height', 'data', 'format']
            for field in required_fields:
                if field not in data:
                    logger.error(f"Camera frame missing required field: {field}")
                    return None
            
            # Parse data
            width = data['width']
            height = data['height']
            format_type = data['format']
            frame_data = data['data']
            timestamp = data.get('timestamp', datetime.now().isoformat())
            
            # Decode base64 data
            if isinstance(frame_data, str):
                frame_data = base64.b64decode(frame_data)
            
            # Validate data size
            expected_size = width * height * 3  # RGB format
            if len(frame_data) != expected_size:
                logger.warning(f"Camera frame data size mismatch: expected {expected_size}, actual {len(frame_data)}")
            
            return CameraFrame(
                timestamp=timestamp,
                width=width,
                height=height,
                format=format_type,
                data=frame_data,
                frame_id=self.camera_frame_count
            )
            
        except Exception as e:
            logger.error(f"Error parsing camera frame data: {e}")
            return None
    
    def parse_audio_frame(self, data: Dict[str, Any]) -> Optional[AudioFrame]:
        """Parse audio frame data"""
        try:
            # Check required fields
            required_fields = ['sample_rate', 'channels', 'data', 'format']
            for field in required_fields:
                if field not in data:
                    logger.error(f"Audio frame missing required field: {field}")
                    return None
            
            # Parse data
            sample_rate = data['sample_rate']
            channels = data['channels']
            format_type = data['format']
            audio_data = data['data']
            duration_ms = data.get('duration_ms', 0.0)
            timestamp = data.get('timestamp', datetime.now().isoformat())
            
            # Decode base64 data
            if isinstance(audio_data, str):
                audio_data = base64.b64decode(audio_data)
            
            return AudioFrame(
                timestamp=timestamp,
                sample_rate=sample_rate,
                channels=channels,
                format=format_type,
                data=audio_data,
                duration_ms=duration_ms,
                frame_id=self.audio_frame_count
            )
            
        except Exception as e:
            logger.error(f"Error parsing audio frame data: {e}")
            return None
    
    def process_camera_frame(self, camera_frame: CameraFrame):
        """Process camera frame data"""
        try:
            # Add to memory storage
            self.camera_frames.append(camera_frame)
            self.camera_frame_count += 1
            
            # Limit number of frames in memory (keep latest 100 frames)
            if len(self.camera_frames) > 100:
                self.camera_frames.pop(0)
            
            # Save to file (if enabled)
            if self.save_data:
                self.save_camera_frame(camera_frame)
            
            logger.info(f"Processed camera frame: {camera_frame.width}x{camera_frame.height}, "
                       f"format: {camera_frame.format}, size: {len(camera_frame.data)} bytes")
            
        except Exception as e:
            logger.error(f"Error processing camera frame: {e}")
            raise
    
    def process_audio_frame(self, audio_frame: AudioFrame):
        """Process audio frame data"""
        try:
            # Add to memory storage
            self.audio_frames.append(audio_frame)
            self.audio_frame_count += 1
            
            # Limit number of frames in memory (keep latest 100 frames)
            if len(self.audio_frames) > 100:
                self.audio_frames.pop(0)
            
            # Save to file (if enabled)
            if self.save_data:
                self.save_audio_frame(audio_frame)
            
            logger.info(f"Processed audio frame: {audio_frame.sample_rate}Hz, "
                       f"channels: {audio_frame.channels}, duration: {audio_frame.duration_ms}ms, "
                       f"size: {len(audio_frame.data)} bytes")
            
        except Exception as e:
            logger.error(f"Error processing audio frame: {e}")
            raise
    
    def process_text_message(self, message: TextMessage):
        """Process text message"""
        try:
            # Add to memory storage
            self.text_messages.append(message)
            self.text_message_count += 1
            
            # Limit number of messages in memory (keep latest 100 messages)
            if len(self.text_messages) > 100:
                self.text_messages.pop(0)
            
            # Save to file (if enabled)
            if self.save_data:
                self.save_text_message(message)
            
            logger.info(f"Sent text message: {message.message_id}, content: {message.content[:50]}...")
            
        except Exception as e:
            logger.error(f"Error processing text message: {e}")
            raise
    
    def update_text_message_status(self, message_id: str, status: str):
        """Update text message status"""
        for message in self.text_messages:
            if message.message_id == message_id:
                message.status = status
                logger.info(f"Updated message status: {message_id} -> {status}")
                return
        
        logger.warning(f"Message not found: {message_id}")
    
    def save_camera_frame(self, camera_frame: CameraFrame):
        """Save camera frame to file"""
        try:
            # Convert to numpy array
            data = np.frombuffer(camera_frame.data, dtype=np.uint8)
            
            # Reshape to image format
            if camera_frame.format.upper() == 'RGB':
                image = data.reshape(camera_frame.height, camera_frame.width, 3)
                # Convert to BGR format for OpenCV save
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            else:
                image = data.reshape(camera_frame.height, camera_frame.width, 3)
            
            # Save image
            filename = f"camera_frame_{camera_frame.frame_id:06d}_{camera_frame.timestamp.replace(':', '-')}.jpg"
            filepath = self.camera_dir / filename
            cv2.imwrite(str(filepath), image)
            
        except Exception as e:
            logger.error(f"Error saving camera frame: {e}")
    
    def save_audio_frame(self, audio_frame: AudioFrame):
        """Save audio frame to file"""
        try:
            # Save as WAV file
            filename = f"audio_frame_{audio_frame.frame_id:06d}_{audio_frame.timestamp.replace(':', '-')}.wav"
            filepath = self.audio_dir / filename
            
            with wave.open(str(filepath), 'wb') as wav_file:
                wav_file.setnchannels(audio_frame.channels)
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(audio_frame.sample_rate)
                wav_file.writeframes(audio_frame.data)
            
        except Exception as e:
            logger.error(f"Error saving audio frame: {e}")
    
    def save_text_message(self, message: TextMessage):
        """Save text message to file"""
        try:
            # Save as JSON file
            filename = f"text_message_{message.message_id}_{message.timestamp.replace(':', '-')}.json"
            filepath = self.text_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(asdict(message), f, ensure_ascii=False, indent=2)
            
        except Exception as e:
            logger.error(f"Error saving text message: {e}")
    
    def update_camera_stats(self, bytes_received: int):
        """Update camera statistics"""
        self.stats["camera_frames"] += 1
        self.stats["camera_bytes"] += bytes_received
        self.stats["last_camera_frame"] = datetime.now().isoformat()
    
    def update_audio_stats(self, bytes_received: int):
        """Update audio statistics"""
        self.stats["audio_frames"] += 1
        self.stats["audio_bytes"] += bytes_received
        self.stats["last_audio_frame"] = datetime.now().isoformat()
    
    def run(self):
        """Run server"""
        logger.info(f"Starting Quest test server, port: {self.port}")
        logger.info(f"Data saving: {'enabled' if self.save_data else 'disabled'}")
        logger.info("API endpoints:")
        logger.info("  GET  /health - Health check")
        logger.info("  POST /camera/frame - Receive camera frame")
        logger.info("  POST /audio/frame - Receive audio frame")
        logger.info("  POST /text/send - Send text message")
        logger.info("  POST /text/confirm - Confirm text reception")
        logger.info("  GET  /status - Get server status")
        logger.info("  GET  /camera/frames - Get camera frames list")
        logger.info("  GET  /audio/frames - Get audio frames list")
        logger.info("  GET  /text/messages - Get text messages list")
        
        self.app.run(host='0.0.0.0', port=self.port, debug=False)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Quest Device Test Server')
    parser.add_argument('--port', type=int, default=8888, help='Server port (default: 8888)')
    parser.add_argument('--save-data', action='store_true', help='Save received data to files')
    parser.add_argument('--no-save', action='store_true', help='Do not save data to files')
    
    args = parser.parse_args()
    
    # Default to save data unless explicitly specified not to save
    save_data = not args.no_save if args.save_data or not args.no_save else False
    
    # Create and run server
    server = QuestTestServer(port=args.port, save_data=save_data)
    server.run()

if __name__ == '__main__':
    main() 