import unittest
import numpy as np
from numpy.testing import assert_allclose
from hypothesis import given, assume
from hypothesis.extra.numpy import arrays
from hypothesis.strategies import integers

from tests.resources import get_test_images
from white_brush.colors import utils


class TestColorExtraction(unittest.TestCase):

    def test_parse_color_valid_html_colorcode_should_return_rgb_value(self):
        """
           Given
                  valid html color code
            When
                  utils.py_parse_color is called
            Then
                  the valid rgb values should be returned.
        """
        # Arrange
        module_under_test = utils
        color_code = "#729976"
        expected_value = 114, 153, 118

        # Act
        result = module_under_test.parse_color(color_code)

        # Assert
        self.assertEqual(expected_value, result)

    def test_parse_color_valid_color_name_should_return_rgb_value(self):
        """
           Given
                  valid color name
            When
                  utils.py_parse_color is called
            Then
                  the valid rgb values should be returned.
        """
        # Arrange
        module_under_test = utils
        color_code = "rEd"
        expected_value = 255, 0, 0

        # Act
        result = module_under_test.parse_color(color_code)

        # Assert
        self.assertEqual(expected_value, result)

    def test_parse_color_valid_rgb_values_should_return_rgb_value(self):
        """
           Given
                  valid rgb color codes
            When
                  utils.py_parse_color is called
            Then
                  the valid rgb values should be returned.
        """
        # Arrange
        module_under_test = utils
        color_code = "231,115,70"
        expected_value = 231, 115, 70

        # Act
        result = module_under_test.parse_color(color_code)

        # Assert
        self.assertEqual(expected_value, result)

    def test_parse_color_invalid_test_should_return_none(self):
        """
           Given
                  invalid text input
            When
                  utils.py_parse_color is called
            Then
                  none should be returned.
        """
        # Arrange
        module_under_test = utils
        color_code = "somecolor"
        expected_value = None

        # Act
        result = module_under_test.parse_color(color_code)

        # Assert
        self.assertEqual(expected_value, result)

    def test_color_sample(self):
        """Test extracting a representative sample of pixels from an image"""
        for img_name, img in get_test_images():
            sample05 = utils._color_sample(img, p=0.05)
            assert sample05.size < (img.size // 20) + 5
            sample50 = utils._color_sample(img, p=0.5)
            assert sample50.size < (img.size // 2) + 5
            sample20 = utils._color_sample(img, p=0.2)
            assert sample20.size < (img.size // 5) + 5

    def test_bitmask(self):
        """Test creating a value that can be used to mask specific bits"""

        def int_to_binary_str(x: int) -> str:
            return "{:b}".format(x)

        mask = utils._generate_bitmask(2, 8)
        assert int_to_binary_str(mask) == "11111100"

        mask = utils._generate_bitmask(0, 8)
        assert int_to_binary_str(mask) == "11111111"

        mask = utils._generate_bitmask(4, 8)
        assert int_to_binary_str(mask) == "11110000"

        mask = utils._generate_bitmask(4, 16)
        assert int_to_binary_str(mask) == "1111111111110000"

    @given(integers(0, 255), integers(0, 255), integers(0, 255))
    def test_pack_rgb_values(self, r, g, b):
        """
        Test converting between a color in r, g, b format
        (three separate integers) to a single 24bit representation and back
        """
        rgb = utils._pack_rgb_values(r, g, b)
        assert utils._unpack_rgb_values(rgb) == (r, g, b)

    @given(arrays(np.uint8, (2, 3)))
    def test_pack_rgb_uniqueness(self, colors):
        """
        Assert that converting two different colors from r, g, b format
        (three separate integers) to a single 24bit representation
        results in two different values."""
        assume(np.any(colors[0] != colors[1]))
        c1 = utils._pack_rgb_values(*colors[0])
        c2 = utils._pack_rgb_values(*colors[1])
        assert c1 != c2

    @given(arrays(np.uint8, (100, 3)))
    def test_pack_rgb_values_array(self, rgb_arr):
        """
        Test converting between many colors in r, g, b format
        (three separate arrays) to a single 24bit representation and back
        """
        rgb = utils._pack_rgb_values(rgb_arr[:, 0],
                                  rgb_arr[:, 1],
                                  rgb_arr[:, 2])
        r, g, b = utils._unpack_rgb_values(rgb)
        rgb_back = np.stack([r, g, b], axis=1)
        assert_allclose(rgb_arr, rgb_back)
