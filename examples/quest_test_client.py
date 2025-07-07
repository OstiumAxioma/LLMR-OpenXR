#!/usr/bin/env python3
"""
Quest Device Test Client
Used to simulate Quest device sending data to test server

Features:
1. Simulate sending camera environment information
2. Simulate sending microphone audio information
3. Receive and confirm text messages
"""

import argparse
import json
import time
import base64
import threading
import requests
import numpy as np
from datetime import datetime
from typing import Dict, Any
import cv2

class QuestTestClient:
    def __init__(self, server_url: str = "http://localhost:8888"):
        self.server_url = server_url
        self.running = False
        
        # Counters
        self.camera_frame_count = 0
        self.audio_frame_count = 0
        self.text_message_count = 0
        
        # Threads
        self.camera_thread = None
        self.audio_thread = None
        self.text_thread = None
    
    def test_server_connection(self) -> bool:
        """Test server connection"""
        try:
            response = requests.get(f"{self.server_url}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Server connection successful: {data['status']}")
                return True
            else:
                print(f"❌ Server connection failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Cannot connect to server: {e}")
            return False
    
    def generate_test_camera_frame(self, width: int = 1920, height: int = 1080) -> Dict[str, Any]:
        """Generate test camera frame data"""
        # Create test image (checkerboard pattern)
        image = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Create checkerboard
        square_size = 100
        for y in range(0, height, square_size):
            for x in range(0, width, square_size):
                # Alternate black and white squares
                is_white = ((x // square_size) + (y // square_size)) % 2 == 0
                color = 255 if is_white else 0
                image[y:y+square_size, x:x+square_size] = [color, color, color]
        
        # Add some colored elements
        # Red circle
        center_x, center_y = width // 2, height // 2
        radius = 200
        y_coords, x_coords = np.ogrid[:height, :width]
        mask = (x_coords - center_x)**2 + (y_coords - center_y)**2 <= radius**2
        image[mask] = [255, 0, 0]  # Red
        
        # Blue rectangle
        rect_x1, rect_y1 = 100, 100
        rect_x2, rect_y2 = 400, 300
        image[rect_y1:rect_y2, rect_x1:rect_x2] = [0, 0, 255]  # Blue
        
        # Convert to RGB format and encode to base64
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        frame_data = base64.b64encode(rgb_image.tobytes()).decode('utf-8')
        
        return {
            "width": width,
            "height": height,
            "format": "RGB",
            "data": frame_data,
            "timestamp": datetime.now().isoformat()
        }
    
    def generate_test_audio_frame(self, sample_rate: int = 16000, duration_ms: float = 100.0) -> Dict[str, Any]:
        """Generate test audio frame data"""
        # Generate sine wave test audio
        duration_sec = duration_ms / 1000.0
        samples = int(sample_rate * duration_sec)
        
        # Generate 440Hz sine wave
        frequency = 440  # A4 note
        t = np.linspace(0, duration_sec, samples, False)
        audio_data = np.sin(2 * np.pi * frequency * t)
        
        # Convert to 16-bit integer
        audio_data = (audio_data * 32767).astype(np.int16)
        
        # Encode to base64
        audio_bytes = base64.b64encode(audio_data.tobytes()).decode('utf-8')
        
        return {
            "sample_rate": sample_rate,
            "channels": 1,
            "format": "PCM",
            "data": audio_bytes,
            "duration_ms": duration_ms,
            "timestamp": datetime.now().isoformat()
        }
    
    def send_camera_frame(self, frame_data: Dict[str, Any]) -> bool:
        """Send camera frame to server"""
        try:
            response = requests.post(
                f"{self.server_url}/camera/frame",
                json=frame_data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"📷 Camera frame sent successfully: {result['frame_id']}")
                return True
            else:
                print(f"❌ Camera frame send failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error sending camera frame: {e}")
            return False
    
    def send_audio_frame(self, audio_data: Dict[str, Any]) -> bool:
        """Send audio frame to server"""
        try:
            response = requests.post(
                f"{self.server_url}/audio/frame",
                json=audio_data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"🎤 Audio frame sent successfully: {result['frame_id']}")
                return True
            else:
                print(f"❌ Audio frame send failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error sending audio frame: {e}")
            return False
    
    def send_text_message(self, content: str) -> bool:
        """Send text message to server"""
        try:
            response = requests.post(
                f"{self.server_url}/text/send",
                json={"content": content},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"📝 Text message sent successfully: {result['message_id']}")
                return True
            else:
                print(f"❌ Text message send failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error sending text message: {e}")
            return False
    
    def confirm_text_received(self, message_id: str, status: str = "delivered") -> bool:
        """Confirm text message reception"""
        try:
            response = requests.post(
                f"{self.server_url}/text/confirm",
                json={"message_id": message_id, "status": status},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Text message confirmation successful: {result['message_id']} -> {result['new_status']}")
                return True
            else:
                print(f"❌ Text message confirmation failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error confirming text message: {e}")
            return False
    
    def camera_loop(self):
        """Camera data sending loop"""
        while self.running:
            try:
                # Generate test camera frame
                frame_data = self.generate_test_camera_frame()
                
                # Send to server
                if self.send_camera_frame(frame_data):
                    self.camera_frame_count += 1
                
                # Wait 1 second
                time.sleep(1.0)
                
            except Exception as e:
                print(f"❌ Camera loop error: {e}")
                time.sleep(1.0)
    
    def audio_loop(self):
        """Audio data sending loop"""
        while self.running:
            try:
                # Generate test audio frame
                audio_data = self.generate_test_audio_frame()
                
                # Send to server
                if self.send_audio_frame(audio_data):
                    self.audio_frame_count += 1
                
                # Wait 100 milliseconds
                time.sleep(0.1)
                
            except Exception as e:
                print(f"❌ Audio loop error: {e}")
                time.sleep(1.0)
    
    def text_loop(self):
        """Text message sending loop"""
        while self.running:
            try:
                # Send test text message
                message_content = f"Test message #{self.text_message_count + 1} - {datetime.now().strftime('%H:%M:%S')}"
                
                if self.send_text_message(message_content):
                    self.text_message_count += 1
                    
                    # Simulate delivery confirmation
                    time.sleep(0.5)
                    self.confirm_text_received(f"msg_{self.text_message_count:06d}", "delivered")
                    
                    # Simulate read confirmation
                    time.sleep(0.5)
                    self.confirm_text_received(f"msg_{self.text_message_count:06d}", "read")
                
                # Wait 5 seconds
                time.sleep(5.0)
                
            except Exception as e:
                print(f"❌ Text loop error: {e}")
                time.sleep(1.0)
    
    def start(self):
        """Start client"""
        print("🚀 Starting Quest test client...")
        
        # Test server connection
        if not self.test_server_connection():
            print("❌ Cannot connect to server, please ensure server is running")
            return
        
        self.running = True
        
        # Start threads
        self.camera_thread = threading.Thread(target=self.camera_loop, daemon=True)
        self.audio_thread = threading.Thread(target=self.audio_loop, daemon=True)
        self.text_thread = threading.Thread(target=self.text_loop, daemon=True)
        
        self.camera_thread.start()
        self.audio_thread.start()
        self.text_thread.start()
        
        print("✅ Client started, sending test data...")
        print("📷 Camera frames: 1 per second")
        print("🎤 Audio frames: 10 per second")
        print("📝 Text messages: 1 every 5 seconds")
        print("Press Ctrl+C to stop")
        
        try:
            # Main loop
            while self.running:
                time.sleep(1.0)
                
        except KeyboardInterrupt:
            print("\n🛑 Received stop signal, shutting down client...")
            self.stop()
    
    def stop(self):
        """Stop client"""
        self.running = False
        
        # Wait for threads to finish
        if self.camera_thread:
            self.camera_thread.join(timeout=2.0)
        if self.audio_thread:
            self.audio_thread.join(timeout=2.0)
        if self.text_thread:
            self.text_thread.join(timeout=2.0)
        
        print("✅ Client stopped")
        print(f"📊 Statistics:")
        print(f"  Camera frames: {self.camera_frame_count}")
        print(f"  Audio frames: {self.audio_frame_count}")
        print(f"  Text messages: {self.text_message_count}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Quest Device Test Client')
    parser.add_argument('--server', default='http://localhost:8888', help='Server URL (default: http://localhost:8888)')
    
    args = parser.parse_args()
    
    # Create and start client
    client = QuestTestClient(server_url=args.server)
    client.start()

if __name__ == '__main__':
    main() 