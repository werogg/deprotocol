import os
import sys


def before_all(context):
    # Get the path to the "src" directory relative to the current file
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
