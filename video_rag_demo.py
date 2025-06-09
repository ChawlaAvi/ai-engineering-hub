import streamlit as st
import google.generativeai as genai
import tempfile
import os
import requests
from urllib.parse import urlparse
import time
from typing import Optional
import io
from config import (
    GEMINI_MODELS, DEFAULT_MODEL, SUPPORTED_VIDEO_FORMATS,
    MAX_VIDEO_SIZE_MB, API_TIMEOUT, CHUNK_SIZE,
    STREAMLIT_CONFIG, SAMPLE_QUESTIONS,
    ERROR_MESSAGES, SUCCESS_MESSAGES,
    validate_video_url, is_supported_format
)

# Configure page
st.set_page_config(**STREAMLIT_CONFIG)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    .user-message {
        background-color: #f0f2f6;
        border-left-color: #667eea;
    }
    
    .assistant-message {
        background-color: #e8f4fd;
        border-left-color: #1f77b4;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

def initialize_gemini():
    """Initialize Gemini API with API key"""
    api_key = st.session_state.get('gemini_api_key')
    if not api_key:
        return False
    
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        st.error(f"Failed to initialize Gemini API: {str(e)}")
        return False

def download_video_from_url(url: str) -> Optional[str]:
    """Download video from URL and save to temporary file"""
    try:
        # Validate URL
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            st.error("Please provide a valid URL")
            return None
        
        # Show progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("Downloading video...")
        
        # Download video
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Get file extension from URL or content type
        content_type = response.headers.get('content-type', '')
        if 'video/mp4' in content_type:
            ext = '.mp4'
        elif 'video/avi' in content_type:
            ext = '.avi'
        elif 'video/mov' in content_type:
            ext = '.mov'
        else:
            # Try to get extension from URL
            ext = os.path.splitext(parsed_url.path)[1] or '.mp4'
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
        
        # Download with progress
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                temp_file.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    progress = downloaded / total_size
                    progress_bar.progress(progress)
                    status_text.text(f"Downloading video... {progress:.1%}")
        
        temp_file.close()
        progress_bar.progress(1.0)
        status_text.text("Video downloaded successfully!")
        
        return temp_file.name
        
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to download video: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return None

def upload_video_to_gemini(video_path: str):
    """Upload video to Gemini API"""
    try:
        status_text = st.empty()
        progress_bar = st.progress(0)
        
        status_text.text("Uploading video to Gemini API...")
        progress_bar.progress(0.3)
        
        # Upload video file
        video_file = genai.upload_file(path=video_path)
        progress_bar.progress(0.6)
        
        status_text.text("Processing video...")
        
        # Wait for video to be processed
        while video_file.state.name == "PROCESSING":
            time.sleep(2)
            video_file = genai.get_file(video_file.name)
            progress_bar.progress(0.8)
        
        if video_file.state.name == "FAILED":
            st.error("Video processing failed")
            return None
        
        progress_bar.progress(1.0)
        status_text.text("Video uploaded and processed successfully!")
        
        return video_file
        
    except Exception as e:
        st.error(f"Failed to upload video to Gemini: {str(e)}")
        return None

def chat_with_video(video_file, question: str, model_name: str = "gemini-1.5-pro"):
    """Chat with the video using Gemini API"""
    try:
        model = genai.GenerativeModel(model_name)
        
        # Create prompt with video and question
        prompt = [video_file, question]
        
        # Generate response
        response = model.generate_content(prompt)
        
        return response.text
        
    except Exception as e:
        st.error(f"Failed to generate response: {str(e)}")
        return None

def main():
    # Header
    st.markdown('<h1 class="main-header">🎥 Video RAG with Gemini API</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    Welcome to the Video RAG Demo! This application allows you to:
    - Upload a video via URL
    - Ask questions about the video content
    - Get AI-powered responses using Google's Gemini API
    """)
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("��️ Configuration")
        
        # API Key input
        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            help="Enter your Google Gemini API key",
            placeholder="Enter your API key here..."
        )
        
        if api_key:
            st.session_state['gemini_api_key'] = api_key
            if initialize_gemini():
                st.success("✅ API Key configured successfully!")
            else:
                st.error("❌ Invalid API Key")
        
        # Model selection
        model_options = [
            "gemini-1.5-pro",
            "gemini-1.5-flash",
            "gemini-1.0-pro"
        ]
        
        selected_model = st.selectbox(
            "Select Model",
            GEMINI_MODELS,
            index=GEMINI_MODELS.index(DEFAULT_MODEL),
            help="Choose the Gemini model to use"
        )
        
        st.session_state['selected_model'] = selected_model
        
        # Instructions
        st.markdown("---")
        st.markdown("### 📋 Instructions")
        st.markdown("""
        1. Enter your Gemini API key above
        2. Provide a video URL
        3. Wait for the video to be processed
        4. Start asking questions about the video!
        """)
        
        # API Key help
        st.markdown("---")
        st.markdown("### 🔑 Get API Key")
        st.markdown("""
        Get your free Gemini API key from:
        [Google AI Studio](https://makersuite.google.com/app/apikey)
        """)
    
    # Main content area
    if not st.session_state.get('gemini_api_key'):
        st.warning("⚠️ Please enter your Gemini API key in the sidebar to continue.")
        return
    
    # Video URL input
    st.header("📹 Video Input")
    video_url = st.text_input(
        "Video URL",
        placeholder="https://example.com/video.mp4",
        help="Enter a direct URL to a video file (MP4, AVI, MOV supported)"
    )
    
    # Process video button
    if st.button("🚀 Process Video", disabled=not video_url):
        if video_url:
            with st.spinner("Processing video..."):
                # Download video
                video_path = download_video_from_url(video_url)
                
                if video_path:
                    # Upload to Gemini
                    video_file = upload_video_to_gemini(video_path)
                    
                    if video_file:
                        st.session_state['video_file'] = video_file
                        st.session_state['video_url'] = video_url
                        st.success("🎉 Video processed successfully! You can now ask questions about it.")
                        
                        # Display video info
                        st.info(f"📊 Video Info: {video_file.display_name}")
                    
                    # Clean up temporary file
                    try:
                        os.unlink(video_path)
                    except:
                        pass
    
    # Chat interface
    if st.session_state.get('video_file'):
        st.header("💬 Chat with Your Video")
        
        # Display current video
        st.info(f"🎥 Current video: {st.session_state.get('video_url', 'Unknown')}")
        
        # Initialize chat history
        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = []
        
        # Chat input
        question = st.text_input(
            "Ask a question about the video:",
            placeholder="What happens in this video?",
            key="question_input"
        )
        
        # Sample questions
        st.markdown("### 💡 Sample Questions")
        sample_cols = st.columns(2)
        
        for i, sample_q in enumerate(SAMPLE_QUESTIONS[:6]):  # Show first 6 questions
            col = sample_cols[i % 2]
            if col.button(f"📝 {sample_q[:30]}...", key=f"sample_{i}"):
                st.session_state['question_input'] = sample_q
                st.rerun()
        
        # Send button
        if st.button("📤 Send Question", disabled=not question):
            if question:
                # Add user message to history
                st.session_state['chat_history'].append({
                    'role': 'user',
                    'content': question
                })
                
                # Get AI response
                with st.spinner("Generating response..."):
                    response = chat_with_video(
                        st.session_state['video_file'],
                        question,
                        st.session_state.get('selected_model', 'gemini-1.5-pro')
                    )
                    
                    if response:
                        # Add AI response to history
                        st.session_state['chat_history'].append({
                            'role': 'assistant',
                            'content': response
                        })
        
        # Display chat history
        if st.session_state['chat_history']:
            st.markdown("### 💭 Conversation History")
            
            for i, message in enumerate(st.session_state['chat_history']):
                if message['role'] == 'user':
                    st.markdown(f"""
                    <div class="chat-message user-message">
                        <strong>🧑 You:</strong><br>
                        {message['content']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-message assistant-message">
                        <strong>🤖 AI Assistant:</strong><br>
                        {message['content']}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Clear chat button
        if st.session_state.get('chat_history'):
            if st.button("🗑️ Clear Chat History"):
                st.session_state['chat_history'] = []
                st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        Built with ❤️ using Streamlit and Google Gemini API<br>
        <small>Make sure to use appropriate video URLs and respect content policies</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
