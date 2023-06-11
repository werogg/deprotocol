import sys
import os

# Get the parent directory of the current file (main.py)
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.dirname(current_dir)
deprotocol_dir = os.path.dirname(app_dir)

# Add the necessary directories to the sys.path
sys.path.insert(0, app_dir)
sys.path.insert(0, deprotocol_dir)

from deprotocol.app.application import DeProtocol


def main():
    deprotocol = DeProtocol()
    deprotocol.on_start()


if __name__ == '__main__':
    main()
