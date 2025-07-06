#!/usr/bin/env python3
"""
AgentZ Installation Script
Automated setup for AgentZ AI Co-founder Assistant
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ AgentZ requires Python 3.8 or higher")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version {sys.version.split()[0]} is compatible")
    return True

def check_dependencies():
    """Check if required dependencies are available"""
    print("\n📋 Checking dependencies...")
    
    # Check pip
    if not shutil.which("pip"):
        print("❌ pip not found. Please install pip first.")
        return False
    print("✅ pip is available")
    
    return True

def install_requirements():
    """Install Python requirements"""
    requirements_file = "requirements.txt"
    
    if not os.path.exists(requirements_file):
        print(f"❌ {requirements_file} not found!")
        return False
    
    return run_command(
        f"{sys.executable} -m pip install -r {requirements_file}",
        "Installing Python dependencies"
    )

def setup_env_file():
    """Set up .env file"""
    env_source = "agentz/.env"
    
    if os.path.exists(env_source):
        print("✅ .env file already exists")
        return True
    
    print("📝 Creating .env file template...")
    
    env_template = """# AgentZ Configuration
# Replace with your actual API keys

# Groq API Key (get from https://console.groq.com/)
GROQ_API_KEY=your_groq_api_key_here

# OpenAI API Key (for embeddings)
OPENAI_API_KEY=your_openai_api_key_here

# PromptLayer API Key (optional - get from https://promptlayer.com/)
PROMPTLAYER_API_KEY=your_promptlayer_api_key_here

# Model Configuration
GROQ_MODEL=mixtral-8x7b-32768
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# ChromaDB Configuration
CHROMA_PERSIST_DIRECTORY=./chroma_db

# Optional PromptLayer Tracking
ENABLE_PROMPTLAYER=false"""
    
    try:
        with open(env_source, 'w') as f:
            f.write(env_template)
        print("✅ .env file created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def print_setup_instructions():
    """Print post-installation setup instructions"""
    instructions = """
🎉 AgentZ Installation Complete!

📋 Next Steps:

1. 🔑 Set up your API keys:
   Edit agentz/.env and add your API keys:
   
   GROQ_API_KEY=your_actual_groq_api_key
   OPENAI_API_KEY=your_actual_openai_api_key
   
   Get API keys from:
   • Groq: https://console.groq.com/
   • OpenAI: https://platform.openai.com/

2. 🚀 Run AgentZ:
   python run_agentz.py
   
   Or manually:
   cd agentz && python main.py

3. 💬 Start chatting:
   Type your business questions or use commands like:
   • /help - Show help
   • /tools - List research tools
   • /research <topic> - Quick research

📖 For detailed instructions, see README.md

🤝 Need help? Create an issue on GitHub

Happy building! 🚀
"""
    print(instructions)

def main():
    """Main installation process"""
    print("🚀 AgentZ Installation Script")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Install requirements
    print("\n📦 Installing dependencies...")
    if not install_requirements():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Setup .env file
    print("\n⚙️ Setting up configuration...")
    if not setup_env_file():
        print("❌ Failed to setup configuration")
        sys.exit(1)
    
    # Print setup instructions
    print_setup_instructions()

if __name__ == "__main__":
    main()