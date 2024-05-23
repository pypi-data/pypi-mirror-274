"""Dicomsort functionality."""

import difflib
from pathlib import Path
from pydicomsorter.io import find_dicom_files
from pydicomsorter.parser import PatternParser
from pydicomsorter.tags4format import tag_exists, tag_for_keyword

from pydicom._dicom_dict import DicomDictionary

from rich.console import Console
from rich.highlighter import RegexHighlighter
from rich.theme import Theme
from pydantic import BaseModel

from rich.text import Text
from rich.tree import Tree
from rich import print

all_dicom_tags: list[str] = [value[4] for key, value in DicomDictionary.items()]


def print_dicom_path_tree(path: str, tree: Tree):  # pragma: no cover
    """Print a tree of the DICOM path."""
    if not path:
        return
    parts = path.split("/")
    if parts[0] in ["", ".", "/"]:
        parts = parts[1:]
    style = "dim" if parts[0].startswith("__") else ""

    highlighted_label = Text(parts[0], style=style)
    highlighted_label.highlight_regex(
        # highlight anything with curly braces
        r"\{[a-zA-Z0-9_]+\}",
        "bold magenta",
    )
    branch = tree.add(
        highlighted_label,
        style=style,
        guide_style=style,
    )
    print_dicom_path_tree("/".join(parts[1:]), branch)


# dataclass describing DICOMSorter options
class DicomKeyHighlighter(RegexHighlighter):
    """Highlight DICOM keys."""

    base_style = "example."
    # i.e in "%(PatientID)s" should highlight "PatientID"
    highlights = [
        r"%\((?P<DicomTag>[a-zA-Z0-9_]+)\)s",
    ]


class DICOMSorterOptions(BaseModel):
    targetPattern: str = "%PatientID/%StudyID-{SeriesID}"
    deleteSource: bool = False
    symlink: bool = False
    keepGoing: bool = False
    dryRun: bool = False
    verbose: bool = False


class DICOMSorter:
    """Class to sort DICOM files."""

    def __init__(self, options: DICOMSorterOptions):
        self.options: DICOMSorterOptions = options

        self.console = Console(
            highlighter=DicomKeyHighlighter(),
            theme=Theme({"example.DicomTag": "bold magenta"}),
        )
        self.dicom_files = []
        self.format, self.keys = PatternParser().parse(self.options.targetPattern)
        self.tree = Tree(
            ":file_folder: BASE_DIR",
            guide_style="bold bright_blue",
        )

        # make all keys in the string within
        replacements = dict(
            zip(self.keys, ["{{{0}}}".format(key) for key in self.keys])
        )
        self.new_format = self.format % replacements
        tree = Tree(
            ":file_folder: BASE_DIR",
            guide_style="bold bright_blue",
        )
        print_dicom_path_tree(self.new_format, tree)
        print(tree)

    def validate_keys(self) -> None:
        """Validate the keys."""
        invalid_keys: list[str] = self.invalid_keys()
        for key in invalid_keys:
            self.console.print(f"Invalid key:UID- {key}")
            closest_match = difflib.get_close_matches(key, all_dicom_tags, 3, 0.4)
            if closest_match:
                self.console.print("Closest matches:")
                [
                    self.console.print(f"\t[bold cyan]{match}[/bold cyan]")
                    for match in closest_match
                ]
            else:
                self.console.print("No close match found.")

    def print_format(self) -> None:
        """Print the format string."""
        self.console.print(f"Format: {self.format}")
        self.console.print(f"Keys: {self.keys}")

    def invalid_keys(self) -> list[str]:
        """Validate the keys."""
        return [key for key in self.keys if not tag_exists(keyword=key)]

    def __rich__(self) -> Text:
        """Rich output."""
        return Text.assemble(
            f"Target Pattern: {self.options.targetPattern}\n",
            f"Format: {self.format}\n",
            f"Keys: {self.keys}\n",
        )


if "__main__" == __name__:
    options = DICOMSorterOptions(
        targetPattern="/COLLECTION_ID/%PatientID/%StudyID/{SeriesInstanceUID}",
    )
    sorter = DICOMSorter(options)
    sorter.validate_keys()
