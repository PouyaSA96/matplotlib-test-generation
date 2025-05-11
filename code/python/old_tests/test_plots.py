import matplotlib
matplotlib.use('Agg')

import pytest
import numpy as np
import matplotlib.pyplot as plt

plot_types = ["line", "scatter", "bar", "hist", "pie"]
sizes     = [0, 1, 10, 50, 100, 500, 1000, 5000, 10000, 50000, 100000, -10]

functions = [
    ("sin",    lambda x: np.sin(x)),
    ("cos",    lambda x: np.cos(x)),
    ("tan",    lambda x: np.tan(x)),
    ("exp",    lambda x: np.exp(x)),
    ("random", lambda x: np.random.rand(x.size)),
]

@pytest.mark.parametrize("ptype", plot_types)
@pytest.mark.parametrize("n", sizes)
@pytest.mark.parametrize("fname, func", functions)
def test_plot_variations(ptype, n, fname, func, tmp_path):
    x = np.linspace(0, 10, n)
    y = func(x)

    fig, ax = plt.subplots(figsize=(4,3))
    if ptype == "line":
        ax.plot(x, y)
    elif ptype == "scatter":
        ax.scatter(x, y)
    elif ptype == "bar":
        ax.bar(x[:50], y[:50])
    elif ptype == "hist":
        ax.hist(y, bins=20)
    elif ptype == "pie":
        data = np.abs(y[:5])
        ax.pie(data, labels=[f"{i}" for i in range(5)])

    out = tmp_path / f"{ptype}_{fname}_{n}.png"
    fig.savefig(out)
    plt.close(fig)

    # sanity checks
    assert out.exists()
    assert out.stat().st_size > 500
