# 🎥 Video RAG with Gemini API

A Streamlit demo application that enables you to chat with videos using Google's Gemini API. Upload a video file directly and ask questions about its content to get AI-powered responses.

## ✨ Features

- **Video File Upload**: Upload videos directly from your device (MP4, AVI, MOV, MKV, WEBM formats)
- **AI-Powered Analysis**: Uses Google Gemini API for video understanding
- **Interactive Chat**: Ask questions and get detailed responses about video content
- **Multiple Models**: Support for different Gemini models (Pro, Flash, etc.)
- **Beautiful UI**: Clean and responsive Streamlit interface
- **Chat History**: Keep track of your conversation with the video

## 🚀 Quick Start

### Prerequisites

1. **Gemini API Key**: Get your free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Python 3.8+**: Make sure you have Python installed

### Installation

1. Navigate to this directory:
```bash
cd video-rag-gemini
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Streamlit app:
```bash
streamlit run video_rag_demo.py
```

4. Open your browser and navigate to `http://localhost:8501`

## 🎯 How to Use

1. **Configure API Key**: Enter your Gemini API key in the sidebar
2. **Select Model**: Choose your preferred Gemini model
3. **Input Video File**: Provide a video file from your device
4. **Process Video**: Click "Process Video" and wait for upload/processing
5. **Start Chatting**: Ask questions about the video content
6. **View Responses**: Get detailed AI-generated responses about the video

## 📋 Supported Video Formats

- MP4 (recommended)
- AVI
- MOV
- MKV
- WEBM
- Other formats supported by Gemini API

## 🔧 Configuration Options

### Model Selection
- **gemini-1.5-pro**: Best quality, slower processing
- **gemini-1.5-flash**: Faster processing, good quality
- **gemini-1.0-pro**: Basic model

### Video Requirements
- Direct file upload from your device
- Reasonable file size (check Gemini API limits)
- Supported video formats

## 💡 Example Questions

Try asking questions like:
- "What is happening in this video?"
- "Describe the main characters or objects"
- "What is the setting or location?"
- "Summarize the key events"
- "What emotions or mood does this video convey?"
- "Are there any text or signs visible?"

## 🛠️ Technical Details

### Architecture
- **Frontend**: Streamlit for the web interface
- **AI Engine**: Google Gemini API for video understanding
- **Video Processing**: Direct file upload and processing with Gemini
- **State Management**: Streamlit session state for chat history

### API Integration
- Uses `google-generativeai` Python SDK
- Handles video upload and processing
- Manages API rate limits and errors
- Supports multiple model variants

## 🔒 Privacy & Security

- API keys are handled securely (not stored permanently)
- Videos are processed through Google's Gemini API
- Temporary files are cleaned up after processing
- No video content is stored locally

## 🚨 Limitations

- Video file size limits (check Gemini API documentation)
- Processing time depends on video length and complexity
- Requires stable internet connection for video download
- API rate limits may apply

## 🆘 Troubleshooting

### Common Issues

1. **"Invalid API Key"**
   - Verify your Gemini API key is correct
   - Check if the API key has proper permissions

2. **"Failed to download video"**
   - Ensure you have selected a valid video file
   - Check if the video format is supported
   - Verify the file size is within limits

3. **"Video processing failed"**
   - Video might be too large or in unsupported format
   - Try with a smaller or different video file

4. **Slow processing**
   - Large videos take more time to process
   - Consider using gemini-1.5-flash for faster processing
   - Try compressing the video file to reduce size

## 📚 Resources

- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [Video Understanding Guide](https://ai.google.dev/gemini-api/docs/video-understanding)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Google AI Studio](https://makersuite.google.com/)

---

**Built with ❤️ using Streamlit and Google Gemini API**
