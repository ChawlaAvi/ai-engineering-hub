#!/usr/bin/env python3
"""
Simple script to run the Video RAG Demo
"""

import subprocess
import sys
import os

def check_requirements():
    """Check if required packages are installed"""
    required_packages = [
        'streamlit',
        'google-generativeai',
        'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def run_streamlit():
    """Run the Streamlit application"""
    print("🚀 Starting Video RAG Demo...")
    print("📱 The app will open in your default browser")
    print("🔗 If it doesn't open automatically, go to: http://localhost:8501")
    print("\n" + "="*50)
    
    try:
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'video_rag_demo.py'])
    except KeyboardInterrupt:
        print("\n👋 Demo stopped by user")
    except Exception as e:
        print(f"❌ Error running demo: {e}")

def main():
    """Main function"""
    print("🎥 Video RAG with Gemini API - Demo Launcher")
    print("=" * 50)
    
    # Check if requirements.txt exists
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt not found!")
        print("Make sure you're running this script from the project directory.")
        return
    
    # Check if main app exists
    if not os.path.exists('video_rag_demo.py'):
        print("❌ video_rag_demo.py not found!")
        print("Make sure you're running this script from the project directory.")
        return
    
    # Check requirements
    missing = check_requirements()
    
    if missing:
        print(f"📋 Missing packages: {', '.join(missing)}")
        install_choice = input("Would you like to install them now? (y/n): ").lower().strip()
        
        if install_choice in ['y', 'yes']:
            if not install_requirements():
                print("❌ Installation failed. Please install manually:")
                print("pip install -r requirements.txt")
                return
        else:
            print("❌ Cannot run demo without required packages.")
            print("Please install them manually: pip install -r requirements.txt")
            return
    
    # Run the demo
    run_streamlit()

if __name__ == "__main__":
    main()

