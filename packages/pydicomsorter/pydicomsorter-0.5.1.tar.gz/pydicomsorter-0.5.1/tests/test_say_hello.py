import pytest
from pydicomsorter.main import hello


def test_say_hello():
    assert hello() == (
       "Hello from pydicomsorter, [bold magenta]World[/bold magenta]!", ":vampire:"
    )


if __name__ == "__main__":
    pytest.main()
