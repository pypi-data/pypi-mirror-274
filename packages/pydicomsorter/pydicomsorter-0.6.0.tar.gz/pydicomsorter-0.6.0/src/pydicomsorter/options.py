"""A Pydantic model for the DICOMSorter options."""

from pydantic import BaseModel

class DICOMSorterOptions(BaseModel):
    """A Pydantic model for the DICOMSorter options."""

    target_pattern: str = "%PatientID/%StudyID-{SeriesID}"
    delete_source: bool = False
    symlink: bool = False
    keep_going: bool = False
    dry_run: bool = False
    verbose: bool = False
