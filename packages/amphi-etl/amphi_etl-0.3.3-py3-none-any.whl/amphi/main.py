# amphi/main.py

import subprocess
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description='Amphi ETL Command Line Interface')
    parser.add_argument('command', choices=['start'], help='Command to execute')
    parser.add_argument('-w', '--workspace', default='.', help='Workspace directory for JupyterLab')

    args = parser.parse_args()

    if args.command == 'start':
        try:
            subprocess.check_call([sys.executable, '-m', 'jupyter', 'lab', f'--notebook-dir={args.workspace}'])
        except subprocess.CalledProcessError as e:
            print(f"Failed to start Amphi: {e}")

if __name__ == '__main__':
    main()