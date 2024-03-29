from lib import functions as func
from config import constants as const
from matplotlib.colors import ListedColormap
from matplotlib.colors import LinearSegmentedColormap, BoundaryNorm
import matplotlib.pylab as plt
import os
import numpy as np
import seaborn as sns
sns.set_theme()


def ReadData():
    """
    Creates heatmap array with throughput data.
    """

    # Create empty array that can be populated with data.
    # array = [[np.nan for n in range(const.MAX_N + 1)] for k in range(const.MAX_K + 1)]
    array = [[np.nan for k in range(const.MAX_LRC_K + 1)] for r in range(const.MAX_LRC_R + 1)]

    lines = func.GetLines()
    for line in lines[1:]:
        k, l, r, p, throughput = line.split(",")
        k = int(k)
        l = int(l)
        r = int(r)
        p = int(p)
        if (l == 2) and (p == 1) and (k <= const.MAX_LRC_K) and (r <= const.MAX_LRC_R):
            throughput, _ = throughput.split("\n")
            # Populate array with throughput data.
            throughput = float(throughput) / 1000
            array[r][k] = 75 / throughput

    return array


def GenerateHeatmap(data):
    """
    Generates a heatmap given an array of data.
    """

    array = np.array(data, dtype=float)

    # print(np.nanmax(array))

    # Define custom colormap
    # colorlist = ['black', 'maroon', 'red', '#ff7200', '#FFAF00', 'yellow', 'lime', '#00AF00', 'darkgreen']
    colorlist = ['black', 'maroon', 'red', '#FF4000', '#FF8000', '#FFC000', 'yellow', '#E6FF00', '#B3FF00', 'lime', '#00D100', '#009500', 'darkgreen']
    colorlist.reverse()
    n_colors = 256  # number of colors in the colormap
    cmap = LinearSegmentedColormap.from_list("Custom", colorlist, N=n_colors)

    # Generate heatmap
    mask = np.isnan(array)
    plt.figure(figsize=(16, 6))
    ticks = [0, 20, 40, 60]
    vmax = 70
    vmin = 0
    cbar_kws = {"label": "Number of Cores", "drawedges": False, "shrink": 0.5, "spacing": "proportional", "ticks": ticks}
    ax = sns.heatmap(array, cmap=cmap, mask=mask, linewidths=0.5, cbar_kws=cbar_kws, square=True, vmax=vmax, vmin=vmin)

    # X-Y axis labels
    ax.set_ylabel("Global Parity Units R", fontsize=12)
    ax.set_xlabel("Global Data Units K", fontsize=12)
    ax.invert_yaxis()

    # Set axis label settings
    x_tick_positions = np.arange(0, len(data[0]), 5)
    x_tick_labels = [str(x) for x in x_tick_positions]
    ax.set_xticks(x_tick_positions)
    ax.set_xticklabels(x_tick_labels, rotation=0, va='center')

    y_tick_positions = np.arange(0, len(data), 2)
    y_tick_labels = [str(y) for y in y_tick_positions]
    ax.set_yticks(y_tick_positions)
    ax.set_yticklabels(y_tick_labels, rotation=0, va='center')

    # Set title
    ax.set_title("Number of Cores to Achieve 600 Gbps for LRC (X, 2, Y)", fontdict={'fontsize': 16}, y=1.08)

    # Set boundary around outside of heatmap
    for _, spine in ax.spines.items():
        spine.set_visible(True)
        spine.set_edgecolor('black')
        spine.set_linewidth(0.5)

    # Save and show heatmap.
    plt.savefig(const.HEATMAP_PATH)
    plt.show()


def main():
    func.Recalibrate()
    array = ReadData()
    GenerateHeatmap(array)


if __name__ == "__main__":
    main()
