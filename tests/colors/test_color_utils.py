import numpy as np
from numpy.testing import assert_allclose

from white_brush.colors.utils import rgb_to_hsv, hsv_to_rgb


class TestColorExtraction:

    def test_colorspace_conversion_single_color(self):
        """
        Assert that converting one color from HSV to RGB and back
        (or vice versa) results in the same color
        """
        rgb_color = np.array([10, 20, 30], np.uint8)
        hsv_color = np.array([105, 170, 30], np.uint8)
        rgb_color_image = np.tile(rgb_color, 5 * 5).reshape(5, 5, 3)
        hsv_color_image = np.tile(hsv_color, 5 * 5).reshape(5, 5, 3)

        assert_allclose(rgb_to_hsv(rgb_color), hsv_color)
        assert_allclose(rgb_to_hsv(rgb_color_image), hsv_color_image)

        assert_allclose(hsv_to_rgb(hsv_color), rgb_color)
        assert_allclose(hsv_to_rgb(hsv_color_image), rgb_color_image)
