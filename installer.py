import subprocess
import sys
import os
import helper

def in_main():
    # 1. Install requirements
    try:
        # NO QUOTES around sys.executable
        # Added "-m", "pip" so it knows what to do with the install command
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Pip error: {e}")
        return # Stop if install fails

    # 2. Start main.py and quit this script
    print("Starting main.py...")
    os.execv(sys.executable, [sys.executable, "main.py"])

if __name__ == "__main__":
    in_main()