import numpy as np
from hypothesis import given
from hypothesis.extra.numpy import arrays
from hypothesis.strategies import integers
from numpy.testing import assert_allclose

from tests.resources import get_test_images
from white_brush import color_extraction


class TestColorExtraction:

    def test_extract_background_color(self):
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
            background = color_extraction.extract_background_color(img)
            if img_name in expected_colors:
                assert_allclose(background, expected_colors[img_name])

    def test_color_sample(self):
        """Test extracting a representative sample of pixels from an image"""
        for img_name, img in get_test_images():
            sample05 = color_extraction._color_sample(img, p=0.05)
            assert sample05.size < (img.size // 20) + 5
            sample50 = color_extraction._color_sample(img, p=0.5)
            assert sample50.size < (img.size // 2) + 5
            sample20 = color_extraction._color_sample(img, p=0.2)
            assert sample20.size < (img.size // 5) + 5

    def test_bitmask(self):
        """Test creating a value that can be used to mask specific bits"""

        def int_to_binary_str(x: int) -> str:
            return "{:b}".format(x)

        mask = color_extraction._generate_bitmask(2, 8)
        assert int_to_binary_str(mask) == "11111100"

        mask = color_extraction._generate_bitmask(0, 8)
        assert int_to_binary_str(mask) == "11111111"

        mask = color_extraction._generate_bitmask(4, 8)
        assert int_to_binary_str(mask) == "11110000"

        mask = color_extraction._generate_bitmask(4, 16)
        assert int_to_binary_str(mask) == "1111111111110000"

    @given(integers(0, 255), integers(0, 255), integers(0, 255))
    def test_combine_extract_rgb_values(self, r, g, b):
        """
        Test converting between a color in r, g, b format
        (three separate integers) to a single 24bit representation and back
        """
        rgb = color_extraction._combine_rgb_values(r, g, b)
        assert color_extraction._separate_rgb_values(rgb) == (r, g, b)

    @given(arrays(np.uint8, (100, 3)))
    def test_combine_extract_rgb_values_array(self, rgb_arr):
        """
        Test converting between many colors in r, g, b format
        (three separate arrays) to a single 24bit representation and back
        """
        rgb = color_extraction._combine_rgb_values(rgb_arr[:, 0],
                                                   rgb_arr[:, 1],
                                                   rgb_arr[:, 2])
        r, g, b = color_extraction._separate_rgb_values(rgb)
        rgb_back = np.stack([r, g, b], axis=1)
        assert_allclose(rgb_arr, rgb_back)
