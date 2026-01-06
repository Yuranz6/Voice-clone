"""
语音转文字模块
支持实时转录和离线转录
"""
import speech_recognition as sr
from typing import Optional, List
import os

class SpeechToText:
    """语音转文字处理器"""
    
    def __init__(self, google_api_key: Optional[str] = None):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        self.google_api_key = google_api_key
        
    def transcribe_file(self, audio_file: str, language: str = "zh-CN") -> Optional[str]:
        """
        转录音频文件
        
        Args:
            audio_file: 音频文件路径
            language: 语言代码，默认中文
            
        Returns:
            转录文本，失败返回None
        """
        try:
            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)
            
            # 使用Google Speech Recognition
            try:
                if self.google_api_key:
                    text = self.recognizer.recognize_google(audio, language=language, key=self.google_api_key)
                else:
                    text = self.recognizer.recognize_google(audio, language=language)
                return text
            except sr.UnknownValueError:
                print("无法识别音频内容")
                return None
            except sr.RequestError as e:
                print(f"语音识别服务错误: {e}")
                return None
                
        except Exception as e:
            print(f"转录错误: {e}")
            return None
    
    def transcribe_realtime(self, microphone_index: Optional[int] = None) -> str:
        """
        实时语音转录（使用麦克风）
        
        Args:
            microphone_index: 麦克风设备索引，None使用默认
            
        Returns:
            转录文本
        """
        try:
            import pyaudio
        except ImportError:
            raise ImportError(
                "pyaudio is required for real-time transcription. "
                "Install it with: pip install pyaudio (requires PortAudio system library). "
                "Note: Web app uses browser Web Speech API instead."
            )
        
        text_parts = []
        
        with sr.Microphone(device_index=microphone_index) as source:
            # 调整环境噪音
            print("正在调整环境噪音，请保持安静...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("开始录音，说话即可...")
            
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                if self.google_api_key:
                    text = self.recognizer.recognize_google(audio, language="zh-CN", key=self.google_api_key)
                else:
                    text = self.recognizer.recognize_google(audio, language="zh-CN")
                return text
            except sr.WaitTimeoutError:
                return ""
            except sr.UnknownValueError:
                return ""
            except sr.RequestError as e:
                print(f"语音识别服务错误: {e}")
                return ""
    
    def transcribe_stream(self, audio_data: bytes, sample_rate: int = 16000) -> Optional[str]:
        """
        转录音频流数据
        
        Args:
            audio_data: 音频字节数据
            sample_rate: 采样率
            
        Returns:
            转录文本
        """
        try:
            audio = sr.AudioData(audio_data, sample_rate, 2)
            if self.google_api_key:
                text = self.recognizer.recognize_google(audio, language="zh-CN", key=self.google_api_key)
            else:
                text = self.recognizer.recognize_google(audio, language="zh-CN")
            return text
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            print(f"语音识别服务错误: {e}")
            return None

