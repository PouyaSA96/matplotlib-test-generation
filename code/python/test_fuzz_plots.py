import matplotlib
matplotlib.use('Agg')

import numpy as np
import pytest
import matplotlib.pyplot as plt
import random

# --- parameter domains ---
plot_types = ['line','scatter','bar','hist','pie']
sizes     = [2, 10, 100, 1000]
colors    = ['blue','C1','#00FF00']
alphas    = [0.3, 1.0]
linestyles= ['-','--',':']
markers   = ['o','s','^']
bar_widths= [0.2, 0.5, 1.0]
hist_bins = [5, 10, 20]
pie_ns    = [3, 5, 7]

# Build all valid (ptype, n, opts) combos
cases = []
for ptype in plot_types:
    domain = pie_ns if ptype == 'pie' else sizes
    for n in domain:
        for color in colors:
            for alpha in alphas:
                if ptype == 'line':
                    for ls in linestyles:
                        cases.append((ptype, n, dict(color=color, alpha=alpha, linestyle=ls)))
                elif ptype == 'scatter':
                    for m in markers:
                        cases.append((ptype, n, dict(color=color, alpha=alpha, marker=m)))
                elif ptype == 'bar':
                    for w in bar_widths:
                        cases.append((ptype, n, dict(color=color, alpha=alpha, width=w)))
                elif ptype == 'hist':
                    for bins in hist_bins:
                        cases.append((ptype, n, dict(color=color, alpha=alpha, bins=bins)))
                elif ptype == 'pie':
                    cases.append((ptype, n, dict(colors=colors[:n],
                                               labels=[str(i) for i in range(n)],
                                               autopct='%1.1f%%')))

# Sample exactly 300 cases
random.seed(42)
cases = random.sample(cases, 300)

# Pre-generate an ID for each case
ids = [f"{ptype}_{n}_{list(opts.keys())[0]}" for ptype, n, opts in cases]

@pytest.mark.parametrize("ptype,n,opts", cases, ids=ids)
def test_fuzz_plots(ptype, n, opts, tmp_path):
    x = np.linspace(0, 10, n)
    y = np.sin(x)

    fig, ax = plt.subplots()
    if ptype == 'line':
        ax.plot(x, y, **opts)
    elif ptype == 'scatter':
        ax.scatter(x, y, **opts)
    elif ptype == 'bar':
        ax.bar(x, y, **opts)
    elif ptype == 'hist':
        ax.hist(y, **opts)
    elif ptype == 'pie':
        ax.pie(np.abs(y), **opts)

    out = tmp_path / f"{ptype}_{n}.png"
    fig.savefig(out)
    plt.close(fig)
    assert out.exists() and out.stat().st_size > 0
