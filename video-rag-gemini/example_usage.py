"""
Example usage of Video RAG with Gemini API
This script demonstrates the core functionality without Streamlit UI
"""

import google.generativeai as genai
import tempfile
import os
import requests
from urllib.parse import urlparse
import time

def setup_gemini_api(api_key: str):
    """Configure Gemini API"""
    genai.configure(api_key=api_key)
    print("✅ Gemini API configured successfully!")

def download_video(url: str) -> str:
    """Download video from URL"""
    print(f"📥 Downloading video from: {url}")
    
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    # Create temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    
    for chunk in response.iter_content(chunk_size=8192):
        if chunk:
            temp_file.write(chunk)
    
    temp_file.close()
    print("✅ Video downloaded successfully!")
    return temp_file.name

def upload_and_process_video(video_path: str):
    """Upload video to Gemini and wait for processing"""
    print("📤 Uploading video to Gemini API...")
    
    # Upload video file
    video_file = genai.upload_file(path=video_path)
    print(f"📊 Video uploaded: {video_file.display_name}")
    
    # Wait for processing
    print("⏳ Processing video...")
    while video_file.state.name == "PROCESSING":
        print(".", end="", flush=True)
        time.sleep(2)
        video_file = genai.get_file(video_file.name)
    
    print("\n✅ Video processed successfully!")
    
    if video_file.state.name == "FAILED":
        raise Exception("Video processing failed")
    
    return video_file

def ask_question(video_file, question: str, model_name: str = "gemini-1.5-pro"):
    """Ask a question about the video"""
    print(f"\n❓ Question: {question}")
    print("🤔 Thinking...")
    
    model = genai.GenerativeModel(model_name)
    response = model.generate_content([video_file, question])
    
    print(f"\n🤖 Answer: {response.text}")
    return response.text

def main():
    """Main example function"""
    print("🎥 Video RAG with Gemini API - Example Usage\n")
    
    # Configuration
    API_KEY = "YOUR_GEMINI_API_KEY_HERE"  # Replace with your actual API key
    VIDEO_URL = "https://example.com/sample-video.mp4"  # Replace with actual video URL
    
    if API_KEY == "YOUR_GEMINI_API_KEY_HERE":
        print("❌ Please set your Gemini API key in the script!")
        return
    
    try:
        # Setup API
        setup_gemini_api(API_KEY)
        
        # Download video
        video_path = download_video(VIDEO_URL)
        
        # Upload and process
        video_file = upload_and_process_video(video_path)
        
        # Ask questions
        questions = [
            "What is happening in this video?",
            "Describe the main subjects or objects in the video.",
            "What is the setting or environment?",
            "Summarize the key events or actions."
        ]
        
        for question in questions:
            ask_question(video_file, question)
            print("-" * 50)
        
        # Cleanup
        os.unlink(video_path)
        print("\n🧹 Temporary files cleaned up!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()

