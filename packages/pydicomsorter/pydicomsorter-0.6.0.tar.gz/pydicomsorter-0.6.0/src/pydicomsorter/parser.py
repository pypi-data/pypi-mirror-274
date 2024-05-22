"""This module contains functions for parsing DICOM keys from a target pattern."""

import re
from typing import List, Match, Pattern, Tuple

# A custom exception to throw when a pattern is valid but there arent any % or {} in it
class NoPlaceholdersError(Exception):
    """Custom exception to throw when a pattern is valid but there arent any % or {} in it."""

    def __init__(self, message: str = 'No placeholders found in the target pattern.') -> None:
        """Initialize the NoPlaceholdersError.

        Args:
            message (str, optional): The error message.
            Defaults to "No placeholders found in the target pattern.".
        """
        super().__init__(message)


class PatternParser:
    """Class to parse keys from a target pattern."""

    def __init__(self) -> None:
        """Initialize the PatternParser."""
        self.pattern: Pattern[str] = self.compile_pattern()

    @staticmethod
    def compile_pattern() -> Pattern[str]:
        """Compile the regex pattern to match placeholders.

        Returns:
            Pattern[str]: The compiled regex pattern.
        """
        return re.compile(r'%([A-Za-z]+)|\{([A-Za-z]+)\}')

    def replace(self, match: Match[str]) -> str:
        """Replace the match with a formatted string and store the key.

        Args:
            match (Match[str]): The regex match object.

        Returns:
            str: The formatted string with named placeholders.
        """
        key = match.group(1) or match.group(2)
        self.keys.append(key)
        return f'%({key})s'

    def parse(self, target_pattern: str) -> Tuple[str, List[str]]:
        """Parse the target pattern to extract keys and create a format string.

        The target pattern is a string with placeholders matching '%<DICOMKey>' or '{DICOMKey}'.
        This method converts placeholders into a format string with named placeholders
        and creates a list of keys contained within the placeholders.

        Args:
            target_pattern (str): The target pattern string.

        Returns:
            Tuple[str, List[str]]: A tuple containing the format string and a list of keys.

        Raises:
            ValueError: If the target pattern is None or empty.

        Example usage:
            target_pattern = "%PatientID/%StudyID-{SeriesID}"
            fmt, keys = parse(target_pattern)
            print(fmt)  # "%(PatientID)s/%(StudyID)s-%(SeriesID)s"
            print(keys)
        """
        if not target_pattern:
            raise ValueError('The target pattern cannot be None or empty.')

        if not self.pattern.search(target_pattern):
            raise NoPlaceholdersError()

        self.keys: List[str] = []
        formatted_pattern: str = self.pattern.sub(self.replace, target_pattern)

        return formatted_pattern, self.keys
