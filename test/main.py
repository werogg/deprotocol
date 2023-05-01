import os
import sys
from behave.__main__ import main as behave_main


def main():
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

    behave_main()


if __name__ == "__main__":
    main()
