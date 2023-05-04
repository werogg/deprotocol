import os
import sys

# Add 'src' directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from deprotocol.app.application import DeProtocol


def main():
    deprotocol = DeProtocol()
    deprotocol.on_start()


if __name__ == '__main__':
    main()
