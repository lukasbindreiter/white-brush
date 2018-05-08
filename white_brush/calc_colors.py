from sklearn import cluster
import numpy as np


def choose_representative_colors(colors: np.ndarray, n=8):
    """
    Calculates representative colors of a given array of colors. Furthermore
    it is improving the colors by rescaling the minimum and maximum intensity
    values to 0 and 255.

    Args:
        colors: A list of rgb color values.
        n: Specifies how many representative colors will be chosen from the color set

    Returns: A 2-tuple. The first element is a list with 8 elements which specifies the 8 different colors.
        The second element is a list with size colors.length which specifies which of the eight colors is used.
    """
    model = cluster.k_means(colors, n)
    colors = model[0]
    colors = colors.transpose()

    for x in range(0, 2):
        minvalue = min(colors[x])
        maxvalue = max(colors[x])

        if maxvalue - minvalue != 0:
            colors[x] = (colors[x] - minvalue) / (maxvalue - minvalue) * 255

    colors = colors.transpose()

    pixelAssignments = model[1]
    return (colors, pixelAssignments)
