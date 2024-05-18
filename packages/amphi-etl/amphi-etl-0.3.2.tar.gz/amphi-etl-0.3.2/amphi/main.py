# amphi/main.py

import subprocess
import sys

def main():
    try:
        subprocess.check_call([sys.executable, '-m', 'jupyter', 'lab'])
    except subprocess.CalledProcessError as e:
        print(f"Failed to start JupyterLab: {e}")