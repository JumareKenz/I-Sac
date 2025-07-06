#!/usr/bin/env python3
"""
AgentZ Runner Script
Simple script to run AgentZ from project root
"""

import os
import sys
import subprocess

def main():
    """Run AgentZ application"""
    
    # Get the directory of this script (project root)
    project_root = os.path.dirname(os.path.abspath(__file__))
    agentz_dir = os.path.join(project_root, "agentz")
    
    # Check if agentz directory exists
    if not os.path.exists(agentz_dir):
        print("❌ Error: agentz directory not found!")
        print(f"Expected location: {agentz_dir}")
        sys.exit(1)
    
    # Check if main.py exists
    main_script = os.path.join(agentz_dir, "main.py")
    if not os.path.exists(main_script):
        print("❌ Error: main.py not found in agentz directory!")
        print(f"Expected location: {main_script}")
        sys.exit(1)
    
    # Check if .env file exists
    env_file = os.path.join(agentz_dir, ".env")
    if not os.path.exists(env_file):
        print("⚠️  Warning: .env file not found!")
        print(f"Please create {env_file} with your API keys.")
        print("See README.md for setup instructions.")
        print()
        
        # Ask if user wants to continue anyway
        response = input("Continue anyway? (y/N): ").strip().lower()
        if response not in ['y', 'yes']:
            print("Setup your .env file first, then run again.")
            sys.exit(1)
    
    print("🚀 Starting AgentZ...")
    print(f"Working directory: {agentz_dir}")
    print()
    
    try:
        # Change to agentz directory and run main.py
        os.chdir(agentz_dir)
        subprocess.run([sys.executable, "main.py"], check=True)
        
    except KeyboardInterrupt:
        print("\n👋 AgentZ stopped by user")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running AgentZ: {e}")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()