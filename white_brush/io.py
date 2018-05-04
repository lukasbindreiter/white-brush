import cv2


def read_image(filename: str):
    """
    Read an image from disk and return it as matrix of size (width, height, 3) in the RGB Format.
    First dimension is the

    Args:
        filename: The image file to read

    Returns: Three dimensional numpy array.

    """
    img = cv2.imread(filename)
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

