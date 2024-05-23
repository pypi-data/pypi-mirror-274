"""A Pydantic model for the DICOMSorter options."""

from typing import ClassVar, Final

from pydantic import BaseModel
from pydicom._dicom_dict import DicomDictionary
from rich.highlighter import RegexHighlighter

ALL_TAGS: Final[list[str]] = [value[4] for _, value in DicomDictionary.items()]


class DICOMSorterOptions(BaseModel):
    """A Pydantic model for the DICOMSorter options."""

    target_pattern: str = '%PatientID/%StudyID-{SeriesID}'
    delete_source: bool = False
    symlink: bool = False
    keep_going: bool = False
    dry_run: bool = False
    verbose: bool = False


# dataclass describing DICOMSorter options
class DicomKeyHighlighter(RegexHighlighter):
    """Highlight DICOM keys."""

    base_style = 'example.'
    # i.e in "%(PatientID)s" should highlight "PatientID"
    highlights: ClassVar[list[str]] = [
        r'%\((?P<DicomTag>[a-zA-Z0-9_]+)\)s',
    ]
