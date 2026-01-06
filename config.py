"""
配置文件
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Google API配置（用于 Gemini AI 和语音识别）
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")  # 使用 gemini-2.5-flash 或 gemini-2.5-pro

# ElevenLabs API配置（用于文本转语音）
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")

# 语音识别配置
MICROPHONE_INDEX = None  # None表示使用默认麦克风
SAMPLE_RATE = 16000
CHUNK_SIZE = 1024
RECORD_TIMEOUT = 1.0  # 秒
PHRASE_TIMEOUT = 3.0  # 秒

# 文件路径
RECORDINGS_DIR = "recordings"
OUTPUT_DIR = "output"

