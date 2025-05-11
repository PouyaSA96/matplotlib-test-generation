#issue 29912

import pytest
import matplotlib.font_manager as fm

def test_get_fontext_synonyms_woff_support():
    # This should *not* KeyError; at minimum, it should include 'woff'
    exts = fm.get_fontext_synonyms("woff")
    assert "woff" in exts, f"'woff' not in supported extensions: {exts}"
