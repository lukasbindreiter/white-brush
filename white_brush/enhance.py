import numpy as np

from white_brush.colors.color_balance import balance_color
from white_brush.colors.color_extraction import hsv_distance_threshold
from white_brush.colors.morphology import dilate


def enhance(img: np.ndarray) -> np.ndarray:
    # First, balance the color of the image
    balanced = balance_color(img)
    # Perform hsv thresholding
    hsv_thresh = hsv_distance_threshold(balanced)
    # Dilate the result, making the font 'bolder'
    hsv_thresh_dilated = dilate(hsv_thresh, 5)
