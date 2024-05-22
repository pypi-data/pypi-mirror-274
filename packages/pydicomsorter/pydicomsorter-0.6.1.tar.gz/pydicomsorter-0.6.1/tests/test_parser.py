import pytest
from pydicomsorter.parser import PatternParser, NoPlaceholdersError


@pytest.fixture
def parser():
    return PatternParser()
  
@pytest.mark.parametrize(
    "target_pattern, expected_fmt, expected_keys",
    [
        ("%PatientID/%StudyID-{SeriesID}", "%(PatientID)s/%(StudyID)s-%(SeriesID)s", ["PatientID", "StudyID", "SeriesID"]),
        ("{PatientID}/%StudyID-{SeriesID}", "%(PatientID)s/%(StudyID)s-%(SeriesID)s", ["PatientID", "StudyID", "SeriesID"]),
        ("{PatientID}/%StudyID-{SeriesID}", "%(PatientID)s/%(StudyID)s-%(SeriesID)s", ["PatientID", "StudyID", "SeriesID"]),
        ("/%PatientID/%StudyID-{SeriesID}", "/%(PatientID)s/%(StudyID)s-%(SeriesID)s", ["PatientID", "StudyID", "SeriesID"]),
        ("/%PatientID/%StudyID-{SeriesID}", "/%(PatientID)s/%(StudyID)s-%(SeriesID)s", ["PatientID", "StudyID", "SeriesID"]),
    ],
)
def test_parse_valid_pattern(parser, target_pattern, expected_fmt, expected_keys):
    fmt, keys = parser.parse(target_pattern)
    assert fmt == expected_fmt
    assert keys == expected_keys

def test_parse_empty_pattern(parser):
    with pytest.raises(ValueError):
        parser.parse("")

def test_parse_none_pattern(parser):
    with pytest.raises(ValueError):
        parser.parse(None)  # type: ignore

def test_NoPlaceholdersError():
    with pytest.raises(NoPlaceholdersError):
        raise NoPlaceholdersError()
      
def test_NoPlaceholdersError_works(parser):
    with pytest.raises(NoPlaceholdersError):
        parser.parse("No placeholders here!")

if __name__ == "__main__":
    pytest.main()