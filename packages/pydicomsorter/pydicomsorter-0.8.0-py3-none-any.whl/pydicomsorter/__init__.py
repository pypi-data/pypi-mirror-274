"""This is a docstring for the public package."""

from .cli import main
from .io import find_dicom_files

version = '0.1.0'

__version__ = version


__all__ = [
    'find_dicom_files',
    'main',
    'version',
]
