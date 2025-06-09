"""
Configuration settings for Video RAG Demo
"""

import os
from typing import Dict, List

# Gemini API Configuration
GEMINI_MODELS: List[str] = [
    "gemini-1.5-pro",
    "gemini-1.5-flash", 
    "gemini-1.0-pro"
]

DEFAULT_MODEL: str = "gemini-1.5-pro"

# Supported video formats
SUPPORTED_VIDEO_FORMATS: List[str] = [
    ".mp4",
    ".avi", 
    ".mov",
    ".mkv",
    ".webm"
]

# File size limits (in MB)
MAX_VIDEO_SIZE_MB: int = 100

# API Configuration
API_TIMEOUT: int = 300  # 5 minutes
CHUNK_SIZE: int = 8192

# UI Configuration
STREAMLIT_CONFIG: Dict = {
    "page_title": "Video RAG with Gemini API",
    "page_icon": "🎥",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Sample questions for users
SAMPLE_QUESTIONS: List[str] = [
    "What is happening in this video?",
    "Describe the main characters or objects in the video.",
    "What is the setting or location shown?",
    "Summarize the key events or actions.",
    "What emotions or mood does this video convey?",
    "Are there any text, signs, or written content visible?",
    "What colors dominate the video?",
    "Is there any audio or music? Describe it.",
    "What time of day does this appear to be?",
    "What can you tell me about the camera work or filming style?"
]

# Error messages
ERROR_MESSAGES: Dict[str, str] = {
    "no_api_key": "⚠️ Please enter your Gemini API key in the sidebar to continue.",
    "invalid_url": "❌ Please provide a valid video URL.",
    "download_failed": "❌ Failed to download video. Please check the URL and try again.",
    "upload_failed": "❌ Failed to upload video to Gemini API.",
    "processing_failed": "❌ Video processing failed. The file might be too large or in an unsupported format.",
    "generation_failed": "❌ Failed to generate response. Please try again.",
    "invalid_api_key": "❌ Invalid API key. Please check your Gemini API key."
}

# Success messages
SUCCESS_MESSAGES: Dict[str, str] = {
    "api_configured": "✅ API Key configured successfully!",
    "video_downloaded": "✅ Video downloaded successfully!",
    "video_uploaded": "✅ Video uploaded to Gemini API!",
    "video_processed": "🎉 Video processed successfully! You can now ask questions about it.",
    "response_generated": "✅ Response generated successfully!"
}

def get_api_key() -> str:
    """Get API key from environment variable"""
    return os.getenv("GEMINI_API_KEY", "")

def validate_video_url(url: str) -> bool:
    """Validate if URL is properly formatted"""
    from urllib.parse import urlparse
    
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def get_file_extension(url: str) -> str:
    """Extract file extension from URL"""
    from urllib.parse import urlparse
    import os
    
    parsed_url = urlparse(url)
    return os.path.splitext(parsed_url.path)[1].lower()

def is_supported_format(url: str) -> bool:
    """Check if video format is supported"""
    extension = get_file_extension(url)
    return extension in SUPPORTED_VIDEO_FORMATS or extension == ""  # Allow unknown extensions

