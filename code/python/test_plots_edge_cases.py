import pytest
from plots import make_hist, make_pie

@pytest.mark.parametrize("data,bins", [
    (list(range(5)), 0),    # zero bins
    (list(range(5)), -5),   # negative bins
])
def test_hist_invalid_bins_raises(data, bins):
   
    with pytest.raises(ValueError):
        make_hist(data, bins=bins, width=4, height=3)

def test_pie_zero_sum_raises():
  
    with pytest.raises(ZeroDivisionError):
        make_pie([0, 0, 0], width=5, height=5)
