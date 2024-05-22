"""Main module of the package."""

from rich import print


def hello() -> tuple[str, str]:
    """Return a greeting message and an emoji."""
    return 'Hello from pydicomsorter, [bold magenta]World[/bold magenta]!', ':vampire:'


def main() -> None:
    """Print a greeting message and an emoji."""
    print(*hello())


if __name__ == '__main__':
    main()
