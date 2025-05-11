import pytest
from collections import Counter
import matplotlib.pyplot as plt
from plots import make_line, make_bar, make_scatter, make_hist, make_pie

# 5 cases × 20 = 100 tests
MATRIX = [
    (make_line,    [1,2,3],             (4,3)),
    (make_bar,     [0,5,0],             (5,2)),
    (make_scatter, [1,1,2,2,3,3],       (6,4)),
    (make_hist,    list(range(5)),      (3,3)),
    (make_pie,     [1,2,3],             (4,4)),
] * 20

@pytest.mark.parametrize("func,data,size", MATRIX)
def test_plot_matrix(func, data, size):
    fig = func(data, width=size[0], height=size[1])
    assert fig.axes

    plt.close(fig)
