import unittest

from white_brush.commands.template_command import TemplateCommand
from white_brush.entities.enhancement_configuration import \
    EnhancementConfiguration


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
        test_cases = [
            (("whiteboard", "wHitEboaRd", "bw", "blackwhite"),
             ("#000000", "#FFFFFF")),
            (("note", "postit"),
             ("#040b33", "#F7EA5E"))
        ]
        for test_case in test_cases:
            enhance_configuration = EnhancementConfiguration()

            expected_foreground, expected_background = test_case[1]

            for template in test_case[0]:
                # Act
                class_under_test.execute(template, enhance_configuration)

                # Assert
                self.assertEqual(expected_foreground,
                                 enhance_configuration.foreground_color)
                self.assertEqual(expected_background,
                                 enhance_configuration.background_color)

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

        expected_foreground = None
        expected_background = None

        # Act
        class_under_test.execute(template, enhance_configuration)

        # Assert
        self.assertEqual(expected_foreground,
                         enhance_configuration.foreground_color)
        self.assertEqual(expected_background,
                         enhance_configuration.background_color)

    # endregion


# region Helper

if __name__ == '__main__':
    unittest.main()

# endregion
