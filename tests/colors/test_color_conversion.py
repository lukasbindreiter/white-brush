import numpy as np
from hypothesis import given
from hypothesis.extra.numpy import arrays
from numpy.testing import assert_allclose

from tests.resources import get_test_image
from white_brush.colors.conversion import *


class TestColorExtraction:

    def test_colorspace_conversion_rgb_hsv_single_color(self):
        """
        Assert that converting one color from HSV to RGB and back
        (or vice versa) results in the same color
        """
        rgb_color = np.array([10, 20, 30], np.uint8)
        hsv_color = np.array([105, 170, 30], np.uint8)

        assert_allclose(rgb_to_hsv(rgb_color), hsv_color)

        assert_allclose(hsv_to_rgb(hsv_color), rgb_color)

    def test_colorspace_conversion_rgb_hsv_input_shapes(self):
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

    @given(arrays(shape=(1), dtype=np.uint8))
    def test_colorspace_conversion_rgb_gray_single(self, gray_color):
        """
        Test that conversion from gray to rgb and back works when given
        a single color as input
        """
        rgb = gray_to_rgb(gray_color)
        assert rgb.shape == (3,)
        assert np.all(rgb == gray_color)
        gray = rgb_to_gray(rgb)
        assert_allclose(gray, gray_color)

    @given(arrays(shape=(20), dtype=np.uint8))
    def test_colorspace_conversion_rgb_gray_list(self, gray_list):
        """
        Test that conversion from gray to rgb and back works when given
        a list of color as input
        """
        rgb = gray_to_rgb(gray_list)
        assert rgb.shape == (20, 3)
        assert rgb.sum() == gray_list.sum() * 3
        gray = rgb_to_gray(rgb)
        assert_allclose(gray, gray_list)

    @given(arrays(shape=(20, 20), dtype=np.uint8))
    def test_colorspace_conversion_rgb_gray_image(self, gray_image):
        """
        Test that conversion from gray to rgb and back works when given
        an image as input
        """
        rgb = gray_to_rgb(gray_image)
        assert rgb.shape == (20, 20, 3)
        assert rgb.sum() == gray_image.sum() * 3
        gray = rgb_to_gray(rgb)
        assert_allclose(gray, gray_image)

    @given(arrays(shape=(20, 20), dtype=np.bool))
    def test_colorspace_conversion_mask_to_rgb(self, mask):
        """
        Test that converting a mask to rgb replaces the False values
        with the given background color and the True values with
        the given foreground color
        """
        fg_color = (255, 0, 0)  # red
        rgb = mask_to_rgb(mask, bg_color=[0, 0, 0], fg_color=fg_color)
        assert mask.sum() == rgb.sum() / sum(fg_color)

    def test_colorspace_conversion_mask_to_rgb_fg_colors(self):
        img_name, img = get_test_image()
        mask = np.empty(img.shape[:2], dtype=np.bool)
        mask[:] = False
        mask[50:100, 100:150] = True
        out_img = mask_to_rgb_with_fg_colors_from_image(mask, (255, 255, 255),
                                                        img)
        assert out_img.shape == img.shape
        assert np.all(out_img[~mask] == 255)

