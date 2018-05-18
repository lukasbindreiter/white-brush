import numpy as np
import cv2


def erode(foreground_mask: np.ndarray, kernel_size: int,
          kernel_shape: str = "rect", iterations: int = 1) -> np.ndarray:
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
        kernel_shape: How the boundaries will be eroded. Must be one of
            'rect', 'ellipse' or 'cross'
        iterations: How often the erosion algorithm will be applied
            on the image

    Returns:
        The eroded foreground mask
    """
    return __morphological_transformation__(cv2.erode, foreground_mask,
                                            kernel_size, kernel_shape,
                                            iterations)


def dilate(foreground_mask: np.ndarray, kernel_size: int,
           kernel_shape: str = "rect", iterations: int = 1) -> np.ndarray:
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
        kernel_shape: How the boundaries will be dilated. Must be one of
            'rect', 'ellipse' or 'cross'
        iterations: How often the dilation algorithm will be applied
            on the image

    Returns:
        The dilated foreground mask
    """
    return __morphological_transformation__(cv2.dilate, foreground_mask,
                                            kernel_size, kernel_shape,
                                            iterations)


def smooth(foreground_mask: np.ndarray, kernel_size: int,
           kernel_shape: str = "rect") -> np.ndarray:
    """
    Smooth the edges of a text given as foreground mask

    Smoothing an image is used to straightens the lines in the image.
    Smoothing is defined as a series of erosions and dilations after
    one another. smooth = erode(dilate(dilate(erode(mask)))) to be
    exact.

    Args:
        foreground_mask: The mask of shape (X, Y) to smooth
        kernel_size: The kernel size used for the erosion and dilation
        kernel_shape: The kernel shape used for the erosion and dilation
            Must be one of 'rect', 'ellipse' or 'cross'
    Returns:
        The smoothed foreground mask of shape (X, Y)
    """

    def opening(img):
        # opening = erosion followed by dilation
        return dilate(erode(img, kernel_size, kernel_shape), kernel_size,
                      kernel_shape)

    def closing(img):
        # closing = dilation followed by erosion
        return erode(dilate(img, kernel_size, kernel_shape), kernel_size,
                     kernel_shape)

    # smoothing = opening followed by closing
    #           = erode(dilate(dilate(erode(mask))))
    return closing(opening(foreground_mask))


def __morphological_transformation__(morph_func, mask: np.ndarray,
                                     kernel_size: int,
                                     kernel_shape: str = "rect",
                                     iterations: int = 1):
    assert mask.dtype == np.bool
    assert mask.ndim == 2
    shape_dict = {
        "rect": cv2.MORPH_RECT,
        "cross": cv2.MORPH_CROSS,
        "ellipse": cv2.MORPH_ELLIPSE
    }
    assert kernel_shape in shape_dict
    # convert the boolean mask to a gray image
    # the background needs to be black, the foreground white
    gray_img = mask.astype(np.uint8) * 255

    # construct the kernel with the given size and shape
    kernel = cv2.getStructuringElement(shape_dict[kernel_shape],
                                       (kernel_size, kernel_size))

    # perform the morphological transformation
    result = morph_func(gray_img, kernel, iterations)
    # convert the resulting gray image back to a boolean mask
    result_mask = result == 255
    return result_mask
