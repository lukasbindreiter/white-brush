import numpy as np

from white_brush.colors.color_balance import balance_color
from white_brush.colors.color_extraction import hsv_distance_threshold, \
    adaptive_threshold, eroded_background_difference_threshold, \
    background_difference_image, otsu_threshold
from white_brush.colors.conversion import mask_to_rgb, \
    mask_to_rgb_with_fg_colors_from_image
from white_brush.colors.crop_and_rotate import rotate
from white_brush.colors.morphology import dilate, erode, smooth
from white_brush.colors.utils import parse_color
from white_brush.entities.color_configuration import ColorConfiguration
from white_brush.transform import resize_if


class ImageEnhancer:
    def __init__(self, color_config: ColorConfiguration, rotation: int):
        self.color_config = color_config
        self.rotation = rotation

    def enhance(self, img: np.ndarray) -> np.ndarray:
        img = self._transform(img)
        preprocessed_img = self._preprocess(img)
        foreground_mask = self._extract_foreground(preprocessed_img)
        out_img = self._apply_colors(foreground_mask, img, preprocessed_img)
        return out_img

    def _transform(self, img: np.ndarray) -> np.ndarray:
        """
        Steps which transform the given image to its target shape

        - Resize the image if it is too large (>1500 pixels in width or
        height)
        """
        img = rotate(img, self.rotation)
        return resize_if(img, 1000, 1500)

    def _preprocess(self, img: np.ndarray) -> np.ndarray:
        """
        Steps done before starting the actual extraction of background
        and foreground colors, but after the image is transformed to
        its target shape

        - Perform an automatic color balancing
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
        adaptive_thresh = adaptive_threshold(img, 31, 10)
        bg_diff = background_difference_image(img)
        bg_diff2 = (255 - np.clip((255 - bg_diff.astype(np.int)) * 2, 0,
                                  255)).astype(np.uint8)
        otsu = otsu_threshold(bg_diff2)
        result = dilate(otsu, 3) & adaptive_thresh
        return result

    def _apply_colors(self, foreground_mask: np.ndarray,
                      orig_img: np.ndarray,
                      preprocessed_img: np.ndarray) -> np.ndarray:
        """
        Steps done to apply colors to the extracted foreground mask

        Args:
            foreground_mask: Foreground mask returned from
                _extract_foreground
            orig_img: The original (but already transformed) image
                where the mask was calculated from
            preprocessed_img: The preprocessed image
        Returns:
            An RGB image with colors inserted into the given foreground
            mask based on the color config
        """
        if self.color_config.background_color is None:
            bg_color = (255, 255, 255)
        else:
            bg_color = parse_color(self.color_config.background_color)
        if self.color_config.foreground_color is None:
            return mask_to_rgb_with_fg_colors_from_image(foreground_mask,
                                                         bg_color,
                                                         preprocessed_img)
        else:
            fg_color = parse_color(self.color_config.foreground_color)
            return mask_to_rgb(foreground_mask, bg_color=bg_color,
                               fg_color=fg_color)


def enhance(img: np.ndarray, config: ColorConfiguration, rotation: int = 0) -> np.ndarray:
    return ImageEnhancer(config, rotation).enhance(img)
