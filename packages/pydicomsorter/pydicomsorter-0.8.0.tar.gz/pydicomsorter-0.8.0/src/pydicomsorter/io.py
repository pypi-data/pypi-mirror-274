"""I/O utilities."""

from pathlib import Path

from pydicom import dcmread
from pydicom.errors import InvalidDicomError

def find_dicom_files(source_dir: Path) -> list[Path]:
    """Find all DICOM files in the source directory."""
    return [file.resolve() for file in source_dir.glob('**/*.dcm') if file.is_file()]


def read_all(file: Path, tags: list[str]) -> dict[str, str]:
    """Read all tags from the DICOM file."""
    try:
        dicom = dcmread(file, stop_before_pixels=True)
    except TypeError as te:
        raise TypeError(f'Type error reading DICOM file: {file}') from te
    except InvalidDicomError as ide:
        raise InvalidDicomError(f'Invalid DICOM file: {file}') from ide
    except ValueError as ve:
        raise ValueError(f'Value error reading DICOM file: {file}') from ve
    return {tag: str(dicom.get(tag, '')) for tag in tags}


def read_tags(file: Path, tags: list[str]) -> dict[str, str]:
    """Read the specified tags from the DICOM file."""
    try:
        dicom = dcmread(file, specific_tags=tags, stop_before_pixels=True)
    except TypeError as te:
        raise TypeError(f'Type error reading DICOM file: {file}') from te
    except InvalidDicomError as ide:
        raise InvalidDicomError(f'Invalid DICOM file: {file}') from ide
    except ValueError as ve:
        raise ValueError(f'Value error reading DICOM file: {file}') from ve
    return {tag: str(dicom.get(tag, '')) for tag in tags}
