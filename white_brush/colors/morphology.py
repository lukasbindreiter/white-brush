import numpy as np
import cv2


def erode(foreground_mask: np.ndarray, kernel_size, iterations=1):
    """
    Erode the given foreground mask, resulting in a lighter font

    Erosion means removing the boundaries of a given outline in an image
    Performed on text, this has the effect that the resulting text will
    be lighter

    Args:
        foreground_mask: The mask of shape (X, Y) to perform erosion
            on. Must be of type np.bool, True means the pixel is part of
            the foreground, False means its part of the background.
        kernel_size: The kernel_size specifies by how much the erosion
            will erode the image. To e.g. reduce the font by one pixel
            on the left and one pixel on the right, use a kernel_size
            of 3.
        iterations: How often the erosion algorithm will be applied
            on the image

    Returns:
        The eroded foreground mask
    """
    return __morphological_transformation__(cv2.erode, foreground_mask,
                                            kernel_size, iterations)


def dilate(foreground_mask: np.ndarray, kernel_size, iterations=1):
    """
    Dilate the given foreground mask, resulting in a bolder font

    Dilation means enlarging the boundaries of a given outline in an
    image. Performed on text, this has the effect that the resulting
    text will be bolder.

    Args:
        foreground_mask: The mask of shape (X, Y) to perform dilation
            on. Must be of type np.bool, True means the pixel is part of
            the foreground, False means its part of the background.
        kernel_size: The kernel_size specifies by how much the dilation
            will dilate the image. To e.g. enlarge the font by one pixel
            on the left and one pixel on the right, use a kernel_size
            of 3.
        iterations: How often the dilation algorithm will be applied
            on the image

    Returns:
        The dilated foreground mask
    """
    return __morphological_transformation__(cv2.dilate, foreground_mask,
                                            kernel_size, iterations)


def __morphological_transformation__(morph_func, mask: np.ndarray, kernel_size,
                                     iterations):
    assert mask.dtype == np.bool
    assert mask.ndim == 2
    # convert the boolean mask to a gray image
    # the background needs to be black, the foreground white
    gray_img = mask.astype(np.uint8) * 255

    # construct the kernel with the given size
    kernel = np.ones((kernel_size, kernel_size), np.uint8)

    # perform the morphological transformation
    result = morph_func(gray_img, kernel, iterations)
    # convert the resulting gray image back to a boolean mask
    result_mask = result == 255
    return result_mask
