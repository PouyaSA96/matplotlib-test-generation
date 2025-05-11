import pytest
import matplotlib.font_manager as fm
from hypothesis import given, settings, strategies as st

@settings(max_examples=100, deadline=None)
@given(ext=st.text(min_size=1, max_size=8))
def test_get_fontext_synonyms_fuzz(ext):
    try:
        exts = fm.get_fontext_synonyms(ext)
        assert isinstance(exts, (list, tuple)), f"Bad return type for {ext}: {type(exts)}"
        for e in exts:
            assert isinstance(e, str), f"Non‐str in synonyms for {ext}: {e!r}"
    except KeyError:
        pytest.skip(f"Unsupported extension: {ext!r}")
    except Exception as e:
        pytest.fail(f"Unexpected exception for {ext!r}: {e}")

def test_get_fontext_synonyms_woff():
    with pytest.raises(KeyError):
        fm.get_fontext_synonyms("woff")
