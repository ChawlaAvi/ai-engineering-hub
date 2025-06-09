"""
Test script to verify the Video RAG Demo setup
"""

import sys
import os

def test_imports():
    """Test if all required packages can be imported"""
    print("🧪 Testing package imports...")
    
    packages = {
        'streamlit': 'streamlit',
        'google-generativeai': 'google.generativeai',
        'requests': 'requests',
        'Pillow': 'PIL'
    }
    
    failed_imports = []
    
    for package_name, import_name in packages.items():
        try:
            __import__(import_name)
            print(f"✅ {package_name}: OK")
        except ImportError as e:
            print(f"❌ {package_name}: FAILED - {e}")
            failed_imports.append(package_name)
    
    return failed_imports

def test_files():
    """Test if all required files exist"""
    print("\n📁 Testing file structure...")
    
    required_files = [
        'video_rag_demo.py',
        'config.py',
        'requirements.txt',
        'README.md',
        'example_usage.py',
        'run_demo.py'
    ]
    
    missing_files = []
    
    for file_name in required_files:
        if os.path.exists(file_name):
            print(f"✅ {file_name}: OK")
        else:
            print(f"❌ {file_name}: MISSING")
            missing_files.append(file_name)
    
    return missing_files

def test_config():
    """Test configuration file"""
    print("\n⚙️ Testing configuration...")
    
    try:
        from config import (
            GEMINI_MODELS, DEFAULT_MODEL, SUPPORTED_VIDEO_FORMATS,
            SAMPLE_QUESTIONS, ERROR_MESSAGES, SUCCESS_MESSAGES
        )
        
        print(f"✅ Available models: {len(GEMINI_MODELS)}")
        print(f"✅ Default model: {DEFAULT_MODEL}")
        print(f"✅ Supported formats: {len(SUPPORTED_VIDEO_FORMATS)}")
        print(f"✅ Sample questions: {len(SAMPLE_QUESTIONS)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_streamlit_syntax():
    """Test if the main Streamlit app has valid syntax"""
    print("\n🔍 Testing Streamlit app syntax...")
    
    try:
        import ast
        
        with open('video_rag_demo.py', 'r') as f:
            content = f.read()
        
        ast.parse(content)
        print("✅ Streamlit app syntax: OK")
        return True
        
    except SyntaxError as e:
        print(f"❌ Syntax error in video_rag_demo.py: {e}")
        return False
    except Exception as e:
        print(f"❌ Error checking syntax: {e}")
        return False

def main():
    """Main test function"""
    print("🎥 Video RAG Demo - Setup Test")
    print("=" * 40)
    
    # Run all tests
    failed_imports = test_imports()
    missing_files = test_files()
    config_ok = test_config()
    syntax_ok = test_streamlit_syntax()
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 TEST SUMMARY")
    print("=" * 40)
    
    if not failed_imports and not missing_files and config_ok and syntax_ok:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Your Video RAG Demo is ready to run!")
        print("\n🚀 To start the demo, run:")
        print("   python run_demo.py")
        print("   OR")
        print("   streamlit run video_rag_demo.py")
    else:
        print("❌ SOME TESTS FAILED!")
        
        if failed_imports:
            print(f"\n📦 Install missing packages:")
            print("   pip install -r requirements.txt")
        
        if missing_files:
            print(f"\n📁 Missing files: {', '.join(missing_files)}")
        
        if not config_ok:
            print("\n⚙️ Configuration issues detected")
        
        if not syntax_ok:
            print("\n🔍 Syntax errors in main app")
    
    print("\n" + "=" * 40)

if __name__ == "__main__":
    main()

