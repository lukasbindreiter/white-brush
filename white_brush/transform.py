import numpy as np
import cv2


def resize_if(img: np.ndarray, target_size: int,
              thresh_size: int) -> np.ndarray:
    """
    Resize an image to the given target_size if it is larger than a
    given thresh_size.

    The size specified here is the larger dimension of width / height.

    >>> img.shape
    (800, 2000, 3)
    >>> resize_if(img, 1000, 1500).shape
    (400, 1000, 3)
    >>> resize_if(img, 1000, 2000).shape
    (800, 2000, 3)

    Args:
        img: The image to resize
        target_size: The new size for the image
        thresh_size: If the given image is larger in one dimension than
            this threshold, it will be resized, otherwise it will stay
            the same

    Returns:
        The resized image if it was larger than thresh_size, otherwise
        the same image as given as input
    """
    size = max(img.shape[:2])
    if size > thresh_size:
        f = 1 / (size / target_size)
        img = cv2.resize(img, None, fx=f, fy=f,
                         interpolation=cv2.INTER_CUBIC)
    return img
