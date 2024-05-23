"""Dicomsort functionality."""

import difflib

from pydicom._dicom_dict import DicomDictionary
from rich.console import Console

from pydicomsorter.parser import PatternParser
from pydicomsorter.tags4format import tag_exists

all_dicom_tags: list[str] = [value[4] for key, value in DicomDictionary.items()]


class DICOMSorter:
    """Dicomsort class."""

    def __init__(self, destination_dir: str) -> None:
        """Initialize the DICOMSorter."""
        self.format, self.keys = PatternParser().parse(destination_dir)
        self.console = Console()

    def validate_keys(self) -> "DICOMSorter":
        """Validate the keys."""
        invalid_keys: list[str] = self.invalid_keys()
        for key in invalid_keys:
            self.console.print(f"Invalid key:{key}")
            closest_match = difflib.get_close_matches(key, all_dicom_tags, 3, 0.4)
            if closest_match:
                self.console.print("Closest matches:")
                [
                    self.console.print(f"\t[bold cyan]{match}[/bold cyan]")
                    for match in closest_match
                ]
            else:
                self.console.print("No close match found.")

        return self

    def invalid_keys(self) -> list[str]:
        """Validate the keys."""
        return [key for key in self.keys if not tag_exists(keyword=key)]
