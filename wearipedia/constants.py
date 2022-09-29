import os

__all__ = ["PACKAGE_PATH"]

path = __file__
PACKAGE_PATH = os.path.dirname(path)
