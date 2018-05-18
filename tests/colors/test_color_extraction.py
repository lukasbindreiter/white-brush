import numpy as np
from hypothesis import given, assume
from hypothesis.extra.numpy import arrays
from hypothesis.strategies import integers
from numpy.testing import assert_allclose

from tests.resources import *
from white_brush.colors.color_balance import balance_color
import white_brush.colors.color_extraction as ce


class TestColorExtraction:

    def test_hsv_thresholding_with_example_images(self):
        """Test thresholding using the hsv distance method"""
        # these values were precalculated once, this test is to make
        # sure that the calculation works the same on all platforms
        # (which e.g. is not the case if the images were in a lossy
        # format like jpg)
        expected_masked_pixels = {
            "01.png": 16352,
            "02.png": 18696,
            "03.png": 28549
        }

        for name, img in get_test_images():
            if name in expected_masked_pixels:
                img = balance_color(img)
                bg_colors = ce.extract_background_colors(img, thresh=0.4)
                mask = ce.hsv_distance_threshold(img, bg_colors)
                assert mask.sum() == expected_masked_pixels[name]

        # if no bg_colors are specified, they should be calculated from
        # the image automatically, using the default thresh value
        name, img = get_test_image()
        mask_auto = ce.hsv_distance_threshold(img)
        assert mask_auto.shape == (img.shape[0], img.shape[1])

    def test_adaptive_thresholding_with_example_images(self):
        expected_masked_pixels = {
            "01.png": 138641,
            "02.png": 96992,
            "03.png": 150182
        }

        for name, img in get_test_images():
            if name in expected_masked_pixels:
                img = balance_color(img)
                mask = ce.adaptive_threshold(img, 9, 3)
                assert mask.sum() == expected_masked_pixels[name]

    def test_extract_background_colors(self):
        """Test the extraction of the background color in an image"""
        expected_colors = {
            # these four colors are different shades of grey
            "01.jpg": [164, 160, 156],
            "02.jpg": [156, 156, 156],
            "03.jpg": [156, 156, 152],
            "04_crop_and_rotate.jpg": [160, 160, 152],
            # green
            "05_blackboard.jpg": [72, 112, 60]
        }

        for img_name, img in get_test_images():
            # extract a single background color (by setting thresh to 1)
            background = ce.extract_background_colors(img,
                                                      thresh=1)

            if img_name in expected_colors:
                bg_color = expected_colors[img_name]
                assert_allclose(background.ravel(), bg_color)

            # make sure multiple background color extraction works as well
            backgrounds = ce.extract_background_colors(img)
            assert len(backgrounds) > 1

    def test_color_sample(self):
        """Test extracting a representative sample of pixels from an image"""
        for img_name, img in get_test_images():
            sample05 = ce._color_sample(img, p=0.05)
            assert sample05.size < (img.size // 20) + 5
            sample50 = ce._color_sample(img, p=0.5)
            assert sample50.size < (img.size // 2) + 5
            sample20 = ce._color_sample(img, p=0.2)
            assert sample20.size < (img.size // 5) + 5

    def test_bitmask(self):
        """Test creating a value that can be used to mask specific bits"""

        def int_to_binary_str(x: int) -> str:
            return "{:b}".format(x)

        mask = ce._generate_bitmask(2, 8)
        assert int_to_binary_str(mask) == "11111100"

        mask = ce._generate_bitmask(0, 8)
        assert int_to_binary_str(mask) == "11111111"

        mask = ce._generate_bitmask(4, 8)
        assert int_to_binary_str(mask) == "11110000"

        mask = ce._generate_bitmask(4, 16)
        assert int_to_binary_str(mask) == "1111111111110000"

    @given(integers(0, 255), integers(0, 255), integers(0, 255))
    def test_pack_rgb_values(self, r, g, b):
        """
        Test converting between a color in r, g, b format
        (three separate integers) to a single 24bit representation and back
        """
        rgb = ce._pack_rgb_values(r, g, b)
        assert ce._unpack_rgb_values(rgb) == (r, g, b)

    @given(arrays(np.uint8, (2, 3)))
    def test_pack_rgb_uniqueness(self, colors):
        """
        Assert that converting two different colors from r, g, b format
        (three separate integers) to a single 24bit representation
        results in two different values."""
        assume(np.any(colors[0] != colors[1]))
        c1 = ce._pack_rgb_values(*colors[0])
        c2 = ce._pack_rgb_values(*colors[1])
        assert c1 != c2

    @given(arrays(np.uint8, (100, 3)))
    def test_pack_rgb_values_array(self, rgb_arr):
        """
        Test converting between many colors in r, g, b format
        (three separate arrays) to a single 24bit representation and back
        """
        rgb = ce._pack_rgb_values(rgb_arr[:, 0],
                                  rgb_arr[:, 1],
                                  rgb_arr[:, 2])
        r, g, b = ce._unpack_rgb_values(rgb)
        rgb_back = np.stack([r, g, b], axis=1)
        assert_allclose(rgb_arr, rgb_back)
