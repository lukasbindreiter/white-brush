import numpy as np
from scipy import stats as stats

from white_brush.colors.utils import rgb_to_hsv


def hsv_distance_threshold(img: np.ndarray, bg_color,
                           v_thresh=70, s_thresh=80) -> np.ndarray:
    """
    Decide which pixels are background pixels based on HSV distance.

    Calculate the difference between each color and the bg_color in the
    HSV color space and depending on the distances in the V and S
    channel mark each pixel as background or foreground.



    Args:
        img: The image for which to calculate a background mask
        bg_color: The background color to compare to
        v_thresh: Threshold for the V channel. If the difference between
            a color and the background color in the V channel is less
            than this, and also the same applies to s_thresh and the S
            channel, than the pixel is marked as belonging to the
            background.
        s_thresh: Threshold for the S channel.

    Returns:
        The calculated background mask. If an element in the mask is
        True, this means that the corresponding pixel is part of the
        background. If it is false, the pixel is part of the foreground.
    """
    # convert the hsv images to integers in order to avoid
    # uint8 overflows when calculating the difference later
    hsv_img = rgb_to_hsv(img).astype(np.int)
    hsv_bg = rgb_to_hsv(bg_color).astype(np.int)

    # the background is everything that has a difference less than
    # v_thresh in the v channel and less than s_thresh in the s channel
    background_mask = np.abs(hsv_img[:, :, 2] - hsv_bg[2]) <= v_thresh
    background_mask &= np.abs(hsv_img[:, :, 1] - hsv_bg[1]) <= s_thresh

    return background_mask


def extract_background_colors(img: np.ndarray, thresh=0.2) -> np.ndarray:
    """
    Extract the most frequently occurring colors in an image

    Args:
        img: The image of shape (X, Y, 3) for which to extract the
            background color
        thresh: The threshold in percent that will be used to decide
            if a certain color is part of the background or not.
            If a color occurs at least thresh % as often as the most
            frequent color, it is considered part of the background.
            The default value is 20%.

    Returns:
        R, G, B color values of the background as numpy array of
        shape (N, 3). It is not guaranteed that the background colors
        actually occurs in the image, since the bit depth of the colors
        is reduced before extracting the most frequent ones.

    """
    assert 0 <= thresh <= 1
    # only use a subset of the colors of the image
    sample = _color_sample(img)
    # reduce bit depth
    mask = _generate_bitmask(2, 8)
    reduced_colors = sample & mask
    # combine r, g and b into one single value
    rgb = _pack_rgb_values(*[reduced_colors[:, i] for i in range(3)])
    # find the most frequent colors
    colors, counts = np.unique(rgb, return_counts=True)
    # find all the colors that occur at least thresh % as often as
    # the most frequent color. Those colors are the background colors
    # of the image
    most_frequent = counts.max()
    frequent_mask = (counts / most_frequent) >= thresh
    bg_colors = colors[frequent_mask]
    # convert back to separate r, g and b
    bg_colors = np.stack(_unpack_rgb_values(bg_colors), axis=1)
    return bg_colors


def _color_sample(img: np.ndarray, p: float = 0.05) -> np.ndarray:
    """
    Get a representative color sample of the given image.

    Returns a subset of the color values of the given image which has
    a size of roughly the given percentage.

    Args:
        img: The image of shape (X, Y, 3) for which to extract a
            color_sample
        p: The percentage of pixels to sample, given as float
            e.g. 0.05 for 5%

    Returns:
        Color sample of shape (N, 3)
    """
    # combine the X and Y dimension into one, only keep the channels dimension
    ravelled = img.reshape(-1, 3)
    # for 5%, take every 20th value, for 10% every 10th, etc...
    every_nth = int(1 / p)
    return ravelled[::every_nth, :]


def _generate_bitmask(n: int = 2, n_bits: int = 8) -> int:
    """
    Generate a binary number with zeros at the end

    Calculate a value which, if applied as logical and, sets the lowest
    `n` bits to 0.

    Example:
    >>> _generate_bitmask(2, 8) == 0b11111100
    >>> True

    Args:
        n: The number of bits which should be set to zero
        n_bits: Bit size of the number on which the mask will be applied

    Returns:
        The generated bitmask as integer

    """
    all_ones = 2 ** n_bits - 1
    cancel_bits = 2 ** n - 1
    return all_ones - cancel_bits


def _pack_rgb_values(r, g, b):
    """Combine r, g and b into a single 24 bit value"""
    if isinstance(r, np.ndarray):
        r = r.astype(np.int)
    rgb = r << 8
    rgb |= g
    rgb = rgb << 8
    rgb |= b
    return rgb


def _unpack_rgb_values(rgb):
    """Extract r, g and b from a single 24 bit value"""
    mask = _generate_bitmask(0, 8)  # 8 bit int with all bits set to 1
    b = rgb & mask
    rgb = rgb >> 8
    g = rgb & mask
    r = rgb >> 8
    return r, g, b
