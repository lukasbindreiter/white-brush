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

        assert_allclose(rgb_to_hsv(rgb_color), hsv_color)

        assert_allclose(hsv_to_rgb(hsv_color), rgb_color)

    def test_colorspace_conversion_input_shapes(self):
        """
        Test that colorspace conversion works with input arrays of
        different shapes
        """
        rgb_color = np.array([10, 20, 30], np.uint8)
        rgb_2D = np.tile(rgb_color, 5).reshape(5, 3)
        rgb_3D = np.tile(rgb_color, 5 * 5).reshape(5, 5, 3)

        def there_and_back_again(color_arr):
            return hsv_to_rgb(rgb_to_hsv(color_arr))

        assert_allclose(there_and_back_again(rgb_2D), rgb_2D)
        assert_allclose(there_and_back_again(rgb_3D), rgb_3D)
