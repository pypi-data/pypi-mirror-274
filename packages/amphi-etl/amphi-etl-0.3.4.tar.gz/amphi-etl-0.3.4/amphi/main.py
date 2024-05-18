import subprocess
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description='Amphi ETL Command Line Interface')
    parser.add_argument('command', choices=['start'], help='Command to execute')
    parser.add_argument('-w', '--workspace', default='.', help='Workspace directory for JupyterLab')

    args = parser.parse_args()

    # Debugging logs
    print(f"Received command: {args.command}")
    print(f"Workspace directory: {args.workspace}")

    if args.command == 'start':
        jupyter_command = [sys.executable, '-m', 'jupyter', 'lab', f'--notebook-dir={args.workspace}']
        print(f"Running JupyterLab command: {' '.join(jupyter_command)}")
        try:
            subprocess.check_call(jupyter_command)
        except subprocess.CalledProcessError as e:
            print(f"Failed to start Amphi: {e}")

if __name__ == '__main__':
    main()