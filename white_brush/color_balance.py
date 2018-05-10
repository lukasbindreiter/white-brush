import cv2
import numpy as np


def balance_color(img: np.ndarray, percentile: float = 0.5) -> np.ndarray:
    """
    Balance the color in an image by setting the lowest value of each
    channel to zero and the highest to 255.

    The value mapped to 0 is not really to lowest value in each channel,
    but the value at the given percentile. E.g. a percentile of `0.5`
    means it is the 0.5% smallest value. The same percentile is used for
    the largest value.

    Args:
        img: The image of shape (X, Y, 3) for which to perform the
            color balancing
        percentile: At which percentile in each channel the
            lowest / highest value will be picked from.

    Returns:
        The color balanced image of shape (X, Y, 3)

    """
    return cv2.merge(
        [normalize(channel, percentile) for channel in cv2.split(img)])


def normalize(img_channel: np.ndarray, percentile: float = 1) -> np.ndarray:
    """
    Normalize the values in an image by mapping one of the lowest values
    to 0 and one of the highest to 255. All values in between will be
    redistributed accordingly.

    Args:
        img_channel: One channel of an image with shape (X, Y)
        percentile: At which percentile the lowest / highest value
            will be picked from.

    Returns:
        The color balanced channel of shape (X, Y)
    """
    img_channel = img_channel.astype(np.float)

    low = np.percentile(img_channel, percentile)
    high = np.percentile(img_channel, 100 - percentile)

    # map channel values to range 0 - 1
    img_channel = img_channel - low
    img_channel /= (high - low)

    # values outside the specified percentile will be < 0 or > 1,
    # therefore set them to 0 or 1 here
    clipped = np.clip(img_channel, 0, 1)
    # transform to range 0 - 255
    clipped *= 255

    return np.round(clipped).astype(np.uint8)
