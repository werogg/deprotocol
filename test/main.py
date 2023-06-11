import os
import sys
from behave.__main__ import main as behave_main


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)

    steps_path = os.path.join(parent_dir, 'features', 'steps')
    app_path = os.path.join(parent_dir, 'src')

    sys.path.insert(0, steps_path)
    sys.path.insert(0, app_path)

    behave_main(['-k', 'test/features'])


if __name__ == "__main__":
    main()
