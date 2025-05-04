# code/python/test_property_plots.py

import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
import pytest
from io import BytesIO
from hypothesis import given, settings, strategies as st

# --- Plot types and valid style parameters ---
PLOT_TYPES       = ["line", "scatter", "bar", "hist", "pie"]
VALID_COLORS     = ["blue", "#00FF00", "C2"]
VALID_ALPHAS     = [0.3, 0.7, 1.0]
VALID_LINESTYLES = ["-", "--", ":"]
VALID_MARKERS    = ["o", "s", "^"]
VALID_BINS       = [5, 10, 20, 30]
VALID_WIDTHS     = [0.2, 0.5, 1.0]

@st.composite
def plot_cases(draw):
    # 1) choose a plot type
    ptype = draw(st.sampled_from(PLOT_TYPES))
    # 2) generate finite float data of length 2–50
    data = draw(st.lists(
        st.floats(min_value=-1e3, max_value=1e3, allow_nan=False, allow_infinity=False),
        min_size=2, max_size=50
    ))
    arr = np.array(data, dtype=float)

    # 3) build kwargs appropriate for that plot type
    if ptype == "pie":
        # pie needs a list of colors and labels matching data length
        colors = draw(st.lists(st.sampled_from(VALID_COLORS), min_size=len(arr), max_size=len(arr)))
        labels = [str(i) for i in range(len(arr))]
        opts = {
            "colors": colors,
            "labels": labels,
            "autopct": "%1.1f%%"
        }
    else:
        opts = {
            "color": draw(st.sampled_from(VALID_COLORS)),
            "alpha": draw(st.sampled_from(VALID_ALPHAS)),
        }
        if ptype == "line":
            opts["linestyle"] = draw(st.sampled_from(VALID_LINESTYLES))
        elif ptype == "scatter":
            opts["marker"]    = draw(st.sampled_from(VALID_MARKERS))
        elif ptype == "bar":
            opts["width"]     = draw(st.sampled_from(VALID_WIDTHS))
        elif ptype == "hist":
            opts["bins"]      = draw(st.sampled_from(VALID_BINS))

    return ptype, arr, opts

@settings(max_examples=500, deadline=None)
@given(case=plot_cases())
def test_property_plots(case):
    """
    For each randomly generated valid case:
      - Call the matching Matplotlib API.
      - Save to an in-memory buffer.
      - Assert the PNG header is correct.
      - Any exception is treated as a real bug.
    """
    ptype, data, opts = case
    fig, ax = plt.subplots()
    x = np.arange(data.size)

    # invoke the plot
    if ptype == "line":
        ax.plot(x, data, **opts)
    elif ptype == "scatter":
        ax.scatter(x, data, **opts)
    elif ptype == "bar":
        ax.bar(x, data, **opts)
    elif ptype == "hist":
        ax.hist(data, **opts)
    elif ptype == "pie":
        ax.pie(data, **opts)
    else:
        pytest.skip(f"Unknown plot type: {ptype}")

    # write to BytesIO and verify PNG header
    buf = BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    header = buf.read(8)
    assert header == b'\x89PNG\r\n\x1a\n', f"Invalid PNG header: {header}"
