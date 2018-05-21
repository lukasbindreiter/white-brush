from sklearn import cluster
import numpy as np


def choose_representative_colors(colors: np.ndarray, n=8):
    """
    Calculates representative colors of a given array of colors.
    Furthermore it is improving the colors by rescaling the minimum
    and maximum intensity values to 0 and 255.

    Args:
        colors: A list of rgb color values.
        n: Specifies how many representative colors will be chosen
            from the color set

    Returns:
        A 2-tuple. The first element is a list with `n` elements which
        specifies the 8 different colors. The second element is a list
        with size `len(colors)` which specifies which of the eight
        colors is used.

    """
    width, depth = colors.shape
    reshaped_raster = np.reshape(colors, (width, depth))
    model = cluster.KMeans(n_clusters=n)
    labels = model.fit_predict(reshaped_raster)
    palette = model.cluster_centers_
    
    return (palette, labels)
