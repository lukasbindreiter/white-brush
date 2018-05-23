import webcolors
import numpy as np


def parse_color(color):
    """
    Parses the given color text to rgb values in format (255,255,255).

    Args:
        color: color text to be parsed in format 'red', '#728599', and 255,255,255

    Returns:
        Returns the parsed color as rgb value or None if not parseable.
    """
    try:
        color = webcolors.name_to_rgb(color)
        return color.red, color.green, color.blue
    except ValueError:
        pass

    try:
        color = webcolors.hex_to_rgb(color)
        return color.red, color.green, color.blue
    except ValueError:
        pass

    try:
        data = color.split(",")
        return int(data[0]), int(data[1]), int(data[2])
    except Exception:
        pass

    return None


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
