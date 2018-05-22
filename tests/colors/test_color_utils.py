import unittest

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
