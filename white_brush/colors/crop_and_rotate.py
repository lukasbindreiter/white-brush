import numpy as np
import cv2


def rotate(img: np.ndarray, degree: int):
    """
    Rotate an Image by a multiple of 90 degrees

    Args:
        img: The image to rotate
        degree: Multiple of 90, degrees to rotate.
            Examples: 90 for clockwise rotation, 180, or -90 for
            counter clockwise.

    Returns:
        The rotated image
    """
    if degree == 0:
        return img

    degree = (degree + 360) % 360
    return np.rot90(img, k=(4 - degree) // 90)


def four_point_transform(image: np.ndarray, rectangle_coords):
    """
    Calculate a warped image based on 4 given points

    First computes the max height and width, which will be the
    height and width of the new image.

    Then computes a perspective transformation matrix and
    applies it to the image.

    Args:
        image: The image in which the portion to be warped is in
        rectangle_coords: the coordinates of the part to be warped.
            Order: Top left, Top Right, Bottom Right, Bottom Left

    Returns:
        The Warped Image
    """
    (tl, tr, br, bl) = rectangle_coords

    width_1 = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    width_2 = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    max_width = max(int(width_1), int(width_2))

    height_1 = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    height_2 = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    max_height = max(int(height_1), int(height_2))

    destination_image = np.array([
        [0, 0],
        [max_width - 1, 0],
        [max_width - 1, max_height - 1],
        [0, max_height - 1]], dtype="float32")
    """
    Alternative (preserves size):
    destination_image = np.array([
        [0, 0],
        [image.shape[1] - 1, 0],
        [image.shape[1] - 1, image.shape[0] - 1],
        [0, image.shape[0] - 1]], dtype="float32")
    """

    perspective_transformation_matrix = cv2.getPerspectiveTransform(
        rectangle_coords, destination_image)
    warped_image = cv2.warpPerspective(image,
                                       perspective_transformation_matrix,
                                       (max_width, max_height))

    return warped_image
