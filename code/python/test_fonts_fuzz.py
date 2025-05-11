import pytest
from hypothesis import given, strategies as st
from font import get_font_synonyms

@given(ext=st.text(min_size=1, max_size=8))
def test_font_fuzz(ext):
    try:
        syns = get_font_synonyms(ext)
        assert isinstance(syns, list)
    except KeyError:
        pytest.skip(f"Unsupported extension {ext!r}")

@pytest.mark.parametrize("ext,should_raise", [
    ("ttf", False),
    ("woff", False),
    ("unknown", True),
])
def test_font_extensions(ext, should_raise):
    if should_raise:
        with pytest.raises(KeyError):
            get_font_synonyms(ext)
    else:
        syns = get_font_synonyms(ext)
        assert isinstance(syns, list) and syns
