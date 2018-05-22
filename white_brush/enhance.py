import numpy as np

from white_brush.colors.calc_colors import choose_representative_colors
from white_brush.colors.color_balance import balance_color
from white_brush.colors.color_extraction import hsv_distance_threshold, \
    adaptive_threshold, _generate_bitmask
from white_brush.colors.conversion import mask_to_rgb
from white_brush.colors.morphology import dilate, erode, smooth
from white_brush.colors.utils import parse_color
from white_brush.entities.color_configuration import ColorConfiguration


class ImageEnhancer:
    def __init__(self, color_config: ColorConfiguration):
        self.color_config = color_config

    def enhance(self, img: np.ndarray) -> np.ndarray:
        preprocessed_img = self._preprocess(img)
        foreground_mask = self._extract_foreground(preprocessed_img)
        out_img = self._apply_colors(foreground_mask, img, preprocessed_img)
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

    def _apply_colors(self, foreground_mask: np.ndarray,
                      orig_img: np.ndarray,
                      preprocessed_img: np.ndarray) -> np.ndarray:
        if self.color_config.background_color is None:
            bg_color = (255, 255, 255)
        else:
            bg_color = parse_color(self.color_config.background_color)
        if self.color_config.foreground_color is None:
            colors = preprocessed_img[foreground_mask]
            colors &= _generate_bitmask(2, 8)
            rep_colors, color_mapping = choose_representative_colors(colors)
            out_img = np.empty(orig_img.shape, np.uint8)
            out_img[~foreground_mask, :] = bg_color
            out_img[foreground_mask] = rep_colors[color_mapping]
            return out_img
        else:
            fg_color = parse_color(self.color_config.foreground_color)
            return mask_to_rgb(foreground_mask, bg_color=bg_color,
                               fg_color=fg_color)


def enhance(img: np.ndarray, config: ColorConfiguration) -> np.ndarray:
    return ImageEnhancer(config).enhance(img)
