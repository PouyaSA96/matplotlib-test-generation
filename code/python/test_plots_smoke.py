import pytest
from collections import Counter
from plots import make_line, make_bar, make_scatter
import matplotlib.pyplot as plt

SMOKE_MATRIX = [
    (make_line,    [1,2,3,4],    4, 3, {"Line2D": 1}),
    (make_bar,     [0,5,0,5],    5, 2, {"Rectangle": 1}),
    (make_scatter, [1,1,2,2,3,3], 6, 4, {"PathCollection": 1}),
]

@pytest.mark.parametrize("func,data,width,height,expected", SMOKE_MATRIX)
def test_plots_smoke(func, data, width, height, expected):
    # Render the figure
    fig = func(data, width=width, height=height)
    ax = fig.axes[0]

    # Count each artist type on the axes
    children = ax.get_children()
    artists = Counter(type(child).__name__ for child in children)

    # Assert we have at least as many of each expected artist
    for artist, count in expected.items():
        assert artists.get(artist, 0) >= count, (
            f"Expected at least {count} {artist}(s), found {artists.get(artist,0)}"
        )

    # Clean up to avoid too many open figures
    plt.close(fig)
