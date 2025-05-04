#reported https://github.com/matplotlib/matplotlib/issues/30007

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
# all-zero slices → triggers the NaN→int bug
ax.pie([0, 0], labels=["A", "B"])
fig.savefig("out.png")