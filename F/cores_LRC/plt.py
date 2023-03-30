from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pylab as plt
import os
import numpy as np
import seaborn as sns
sns.set_theme()

MAX_LRC_K = 50
MAX_LRC_R = 10
INPUT_PATH = "lrc.dat"

def GetLines():
    """
    Fetches the lines in the output file.
    """
    file_exists = os.path.exists(INPUT_PATH)
    if file_exists:
        with open(INPUT_PATH, "r") as f:
            lines = f.readlines()
            return lines

def ReadData():
    """
    Creates heatmap array with throughput data.
    """

    # Create empty array that can be populated with data.
    array = [[np.nan for k in range(MAX_LRC_K + 1)] for r in range(MAX_LRC_R + 1)]

    lines = GetLines()
    for line in lines[1:]:
        k, l, r, p, throughput = line.split("\t")
        k = int(k)
        l = int(l)
        r = int(r)
        p = int(p)
        if (l == 2) and (p == 1) and (k <= MAX_LRC_K) and (r <= MAX_LRC_R):
            throughput, _ = throughput.split("\n")
            if (throughput == ""):
                continue
            # Populate array with throughput data.
            throughput = float(throughput) / 1000
            array[r][k] = 75 / throughput

    return array


def GenerateHeatmap(data):
    """
    Generates a heatmap given an array of data.
    """

    array = np.array(data, dtype=float)

    # Define custom colormap
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
    plt.savefig("figure.eps",  bbox_inches="tight")
    plt.show()


def main():
    array = ReadData()
    GenerateHeatmap(array)


if __name__ == "__main__":
    main()
