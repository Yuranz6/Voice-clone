"""
实时语音录制模块
"""
try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False
    pyaudio = None

import wave
import os
from datetime import datetime
from typing import Optional
import threading
import queue

class VoiceRecorder:
    """实时语音录制器"""
    
    def __init__(self, sample_rate=16000, chunk_size=1024, channels=1):
        if not PYAUDIO_AVAILABLE:
            raise ImportError(
                "pyaudio is not available. "
                "Install it with: pip install pyaudio (requires PortAudio system library). "
                "Note: Web app doesn't need pyaudio as it uses browser Web Speech API."
            )
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.channels = channels
        self.audio_format = pyaudio.paInt16
        self.frames = []
        self.is_recording = False
        self.audio_queue = queue.Queue()
        self.audio = pyaudio.PyAudio()
        
    def start_recording(self):
        """开始录制"""
        self.is_recording = True
        self.frames = []
        
        def audio_callback(in_data, frame_count, time_info, status):
            if self.is_recording:
                self.audio_queue.put(in_data)
            return (None, pyaudio.paContinue)
        
        self.stream = self.audio.open(
            format=self.audio_format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size,
            stream_callback=audio_callback
        )
        
        self.stream.start_stream()
        
    def stop_recording(self):
        """停止录制"""
        self.is_recording = False
        if hasattr(self, 'stream'):
            self.stream.stop_stream()
            self.stream.close()
    
    def save_recording(self, filepath: str):
        """保存录制的音频"""
        # 收集所有音频数据
        frames = []
        while not self.audio_queue.empty():
            frames.append(self.audio_queue.get())
        
        if not frames:
            return False
            
        # 确保目录存在
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # 保存为WAV文件
        wf = wave.open(filepath, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.audio.get_sample_size(self.audio_format))
        wf.setframerate(self.sample_rate)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        return True
    
    def cleanup(self):
        """清理资源"""
        self.stop_recording()
        self.audio.terminate()

