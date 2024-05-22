"""Module for comparing two dicom files and returning the differences between them."""

import difflib
from typing import Any, Callable, LiteralString, Optional

from rich.console import Console

valid_words = ['PatientID', 'StudyID', 'SeriesID']


def typo_checker_decorator(func: Callable) -> Callable[..., Any]:
    """Decorator to check for typos in the arguments."""

    def wrapper(*args: LiteralString) -> str:
        for arg in args:
            if arg not in valid_words:
                closest_match: list[str] | None
                closest_match = difflib.get_close_matches(arg, valid_words, 1, 0.4)
                print_nice_did_you_mean(arg, closest_match[0] if closest_match else None)

        return func(*args)

    return wrapper


def print_nice_did_you_mean(original_arg: str, closest_match: Optional[str]) -> None:
    """Print a nice message for the user and get user response."""
    console = Console()
    richColors = {
        'PatientID': 'red',
        'StudyID': 'red',
        'SeriesID': 'red',
    }
    if closest_match:
        console.print(
            f'\t\tDid you mean: [{richColors[closest_match]}] {closest_match}?',
            style='bold',
        )
        response = input('Enter y/n: ')
        if response.lower() == 'y':
            # Do something if user selects "y"
            console.print(f'Processing Fruits: {closest_match}')
        else:
            # Do something if user selects "n"
            console.print(f'[bold red]Invalid argument[bold red]: {original_arg}', style='bold')
    else:
        console.print(f'[bold red]Invalid argument[bold red]: {original_arg}', style='bold')


class FruitProcessor:
    """Class to process fruits."""

    @staticmethod
    @typo_checker_decorator
    def process(*fruits: LiteralString) -> str:
        """Process the fruits and return the processed string."""
        print(f"Processing Fruits: {''.join(fruits)}")
        return 'Fruits Processed!'


if __name__ == '__main__':
    fruit_processor = FruitProcessor()
    fruit_processor.process('PatientID', 'StudyID', 'SeriesID')
    fruit_processor.process('PatientID', 'StudyID', 'SeriesID', 'PatientID', 'Stud', 'SeriesID')
