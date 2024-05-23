"""This is a docstring for the public package."""

from .cli import main
from .io import find_dicom_files

version = "0.9.1"

__all__ = [
    "find_dicom_files",
    "main",
    "version",
]
