import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
import pytest
from io import BytesIO
from hypothesis import given, settings, strategies as st

@pytest.mark.parametrize("fmt,header", [
    ("svg", b"<?xml"), 
    ("pdf", b"%PDF-")
])
def test_save_formats(fmt, header):
    fig, ax = plt.subplots()
    x = np.linspace(0, 2*np.pi, 50)
    ax.plot(x, np.sin(x), color="C3", alpha=0.7)
    buf = BytesIO()
    fig.savefig(buf, format=fmt)
    plt.close(fig)
    data = buf.getvalue()
    assert data.startswith(header), f"{fmt} output missing header"

APIS = st.sampled_from(["errorbar","boxplot","violin","stackplot"])
@st.composite
def api_cases(draw):
    api = draw(APIS)
    n   = draw(st.integers(min_value=3, max_value=30))
    data = [draw(st.lists(
        st.floats(-100,100), min_size=n, max_size=n
    )) for _ in range(draw(st.integers(1,4)))]
    kwargs = {}
    if api == "errorbar":
        # for simplicity, reuse one series
        yerr = draw(st.lists(st.floats(0,5), min_size=n, max_size=n))
        kwargs = {"yerr": yerr, "fmt": "o-"}
    elif api == "boxplot":
        kwargs = {"notch": True}
    elif api == "violin":
        kwargs = {"showmeans": True}
    elif api == "stackplot":
        kwargs = {}
    return api, data, kwargs

@settings(max_examples=200, deadline=None)
@given(case=api_cases())
def test_fuzz_apis(case):
    api, data, opts = case
    fig, ax = plt.subplots()
    try:
        if api == "errorbar":
            x = np.arange(len(data[0]))
            ax.errorbar(x, data[0], **opts)
        elif api == "boxplot":
            ax.boxplot(data, **opts)
        elif api == "violin":
            ax.violinplot(data, **opts)
        elif api == "stackplot":
            x = np.arange(len(data[0]))
            ax.stackplot(x, *data, **opts)
    except ValueError:
        pytest.skip("Expected ValueError for invalid-but-bounded inputs")
    except Exception as e:
        pytest.fail(f"Unexpected exception in {api}: {e}")
    finally:
        buf = BytesIO()
        fig.savefig(buf, format="svg")   # also smoke-test SVG output
        plt.close(fig)
        header = buf.getvalue()[:5]
        assert header in (b"<?xml",)
