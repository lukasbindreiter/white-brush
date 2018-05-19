import numpy as np
import unittest
from numpy.testing import assert_allclose

from white_brush.colors import utils
from white_brush.colors.utils import rgb_to_hsv, hsv_to_rgb


class TestColorExtraction(unittest.TestCase):

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
