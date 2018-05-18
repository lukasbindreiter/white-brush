import numpy as np

from white_brush.colors.color_balance import balance_color
from white_brush.colors.color_extraction import hsv_distance_threshold, \
    adaptive_threshold
from white_brush.colors.conversion import mask_to_rgb
from white_brush.colors.morphology import dilate, erode, smooth


class ImageEnhancer:
    def enhance(self, img: np.ndarray) -> np.ndarray:
        img = self._preprocess(img)
        foreground_mask = self._extract_foreground(img)
        out_img = self._apply_colors(foreground_mask)
        return out_img

    def _preprocess(self, img: np.ndarray) -> np.ndarray:
        """
        Steps done before starting the actual extraction of background
        and foreground colors
        """
        return balance_color(img)

    def _extract_foreground(self, img: np.ndarray) -> np.ndarray:
        """
        Steps done to extract the foreground and background of an image

        Args:
            img: Input image in RGB, shape (X, Y, 3)

        Returns:
            The calculated foreground mask. If an element in the mask
            is False, this means that the corresponding pixel is part
            of the background. If it is True, the pixel is part of the
            foreground.
        """
        # Perform hsv thresholding
        hsv_thresh = hsv_distance_threshold(img)

        # Also perform adaptive thresholding
        adaptive_thresh = adaptive_threshold(img, 17, 3)

        # Now combine the two threshold results
        hsv_thresh_dilated = dilate(hsv_thresh, 5)
        adaptive_thresh_dilated = dilate(adaptive_thresh, 3)
        combined_thresh = hsv_thresh_dilated & adaptive_thresh_dilated
        combined_thresh = erode(combined_thresh, 3, kernel_shape="ellipse")
        combined_thresh = smooth(combined_thresh, 3)
        return combined_thresh

    def _apply_colors(self, foreground_mask: np.ndarray) -> np.ndarray:
        return mask_to_rgb(foreground_mask, bg_color=[255, 255, 255],
                           fg_color=[0, 0, 0])


def enhance(img: np.ndarray) -> np.ndarray:
    return ImageEnhancer().enhance(img)
