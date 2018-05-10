import unittest

from white_brush.commands.template_command import TemplateCommand
from white_brush.entities.enhancement_configuration import EnhancementConfiguration


class TestTemplateCommand(unittest.TestCase):

    # region execute

    def test_execute_given_matching_template_should_change_color_codes(self):
        """
        Given
            a template matching with the default templates
        When
            TemplateCommand.execute() is called
        Then
            the configuration should be filled with the template color codes.
        """
        # Arrange
        class_under_test = TemplateCommand()
        template = "wHitEboaRd"
        enhance_configuration = EnhancementConfiguration()

        expected_foreground = "#000000"
        expected_background = "#FFFFFF"

        # Act
        class_under_test.execute(template, enhance_configuration)

        # Assert
        self.assertEqual(enhance_configuration.foreground_color, expected_foreground)
        self.assertEqual(enhance_configuration.background_color, expected_background)

    def test_execute_given_no_matching_template_should_keep_default(self):
        """
        Given
            a unknown template not matching with the default templates
        When
            TemplateCommand.execute() is called
        Then
            the configuration should keep the default template color codes.
        """
        # Arrange
        class_under_test = TemplateCommand()
        template = "MultiMedia"
        enhance_configuration = EnhancementConfiguration()

        expected_foreground = "#default"
        expected_background = "#default"

        # Act
        class_under_test.execute(template, enhance_configuration)

        # Assert
        self.assertEqual(enhance_configuration.foreground_color, expected_foreground)
        self.assertEqual(enhance_configuration.background_color, expected_background)

    # endregion


# region Helper

if __name__ == '__main__':
    unittest.main()

# endregion
