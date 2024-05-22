"""I/O utilities."""

from pathlib import Path


def find_dicom_files(source_dir: Path) -> list[Path]:
    """Find all DICOM files in the source directory."""
    return [file for file in source_dir.glob('**/*.dcm') if file.is_file()]


if '__main__' == __name__:
    files = find_dicom_files(Path('data'))

    print(f'Length of files: {len(files)}')
    print(f'First file: {files[0]}')

    print(f'Permission in octal: {files[0].stat().st_mode & 0o777}')
