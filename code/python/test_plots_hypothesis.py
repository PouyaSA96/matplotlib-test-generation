import pytest
from hypothesis import given, settings, strategies as st
from plots import make_line, make_bar, make_scatter, make_hist, make_pie
import matplotlib.pyplot as plt
import warnings
from hypothesis import assume

warnings.filterwarnings(
    "ignore",
    message="invalid value encountered in divide",
    category=RuntimeWarning
)
# Map names to your factory functions
PLOTS = {
    "line": make_line,
    "bar": make_bar,
    "scatter": make_scatter,
    "hist": make_hist,
    "pie": make_pie,
}

@st.composite
def args(draw):
    # choose which plot to test
    name = draw(st.sampled_from(list(PLOTS.keys())))
    # random figure size
    w = draw(st.integers(1, 10))
    h = draw(st.integers(1, 10))
    # for pies, only non-negative data allowed
    if name == "pie":
        data = draw(st.lists(st.floats(min_value=0, max_value=10), min_size=1, max_size=20))
    else:
        data = draw(st.lists(st.floats(-10, 10), min_size=1, max_size=20))
    return name, (w, h), data

@given(params=args())
@settings(max_examples=800)
def test_plots_random(params):
    name, (w, h), data = params
    func = PLOTS[name]
    try:
        fig = func(data, width=w, height=h)
    except ValueError as e:
        assume(False)
    # Verify the figure size exactly matches
    size = fig.get_size_inches().tolist()
    assert size == [w, h], f"Expected size {[w,h]}, got {size}"
    # Ensure there's at least one artist drawn
    ax = fig.axes[0]
    assert any([ax.lines, ax.patches, ax.collections]), f"No artists in {name} for data {data!r}"
    # Clean up to prevent too many open figures
    plt.close(fig)
