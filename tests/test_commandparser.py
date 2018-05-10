import sys
import unittest

from white_brush.commands.command_parser import CommandParser
from white_brush.entities.enhancement_configuration import EnhancementConfiguration


class TestCommandParser(unittest.TestCase):

    # region Command parse_args

    def test_parse_args_given_files_should_call_FileEnhanceCommand(self):
        """
        Given
            valid file command parameters
        When
            CommandParser.parse_args() is called
        Then
            FileEnhanceCommand should be called.
        """
        # Arrange
        mocked_enhance_command = MockedFileEnhanceCommand()
        mocked_template_command = MockedTemplateCommand()
        class_under_test = CommandParser(mocked_enhance_command, mocked_template_command)
        args = "whitebrush cookie.png strange_image.png masterPiece.png".split(' ')

        # Act
        sys.argv = args
        class_under_test.parse_args()

        # Assert
        self.assertTrue(mocked_enhance_command.called)
        self.assertFalse(mocked_enhance_command.used_configuration.recursive)
        self.assertEqual(mocked_enhance_command.amount_of_processed_files, 3)

    def test_parse_args_given_no_files_should_not_call_FileEnhanceCommand(self):
        """
             Given
                 no file command parameters
             When
                 CommandParser.parse_args() is called
             Then
                 FileEnhanceCommand should not be called.
             """
        # Arrange
        mocked_enhance_command = MockedFileEnhanceCommand()
        mocked_template_command = MockedTemplateCommand()
        class_under_test = CommandParser(mocked_enhance_command, mocked_template_command)
        args = "whitebrush".split(' ')

        # Act
        sys.argv = args
        class_under_test.parse_args()

        # Assert
        self.assertFalse(mocked_enhance_command.called)

    def test_parse_args_given_files_with_recursive_tag_should_call_FileEnhanceCommand(self):
        """
             Given
                 valid file command parameters and --recursive
             When
                 CommandParser.parse_args() is called
             Then
                 FileEnhanceCommand with recursive enabled should be called.
             """
        # Arrange
        mocked_enhance_command = MockedFileEnhanceCommand()
        mocked_template_command = MockedTemplateCommand()
        class_under_test = CommandParser(mocked_enhance_command, mocked_template_command)
        args = "whitebrush --recursive cookie.png strange_image.png".split(' ')

        # Act
        sys.argv = args
        class_under_test.parse_args()

        # Assert
        self.assertTrue(mocked_enhance_command.called)
        self.assertTrue(mocked_enhance_command.used_configuration.recursive)
        self.assertEqual(mocked_enhance_command.amount_of_processed_files, 2)

    def test_parse_args_given_files_with_convert_tag_should_call_FileEnhanceCommand(self):
        """
             Given
                 valid file command parameters and --convert
             When
                 CommandParser.parse_args() is called
             Then
                 FileEnhanceCommand with replace enabled should be called.
             """
        # Arrange
        mocked_enhance_command = MockedFileEnhanceCommand()
        mocked_template_command = MockedTemplateCommand()
        class_under_test = CommandParser(mocked_enhance_command, mocked_template_command)
        args = "whitebrush --convert cookie.png strange_image.png".split(' ')

        # Act
        sys.argv = args
        class_under_test.parse_args()

        # Assert
        self.assertTrue(mocked_enhance_command.called)
        self.assertTrue(mocked_enhance_command.used_configuration.replace_files)
        self.assertEqual(mocked_enhance_command.amount_of_processed_files, 2)

    def test_parse_args_given_files_with_mask_tag_should_call_FileEnhanceCommand(self):
        """
             Given
                 valid file command parameters and --mask
             When
                 CommandParser.parse_args() is called
             Then
                 FileEnhanceCommand with correct mask should be called.
             """
        # Arrange
        mocked_enhance_command = MockedFileEnhanceCommand()
        mocked_template_command = MockedTemplateCommand()
        class_under_test = CommandParser(mocked_enhance_command, mocked_template_command)
        args = "whitebrush --mask {name}superfancyimage{extension} cookie.png".split(' ')
        expected = "{name}superfancyimage{extension}"

        # Act
        sys.argv = args
        class_under_test.parse_args()

        # Assert
        self.assertTrue(mocked_enhance_command.called)
        self.assertEqual(mocked_enhance_command.used_configuration.target_file_mask, expected)
        self.assertEqual(mocked_enhance_command.amount_of_processed_files, 1)

    def test_parse_args_given_files_with_background_tag_should_call_FileEnhanceCommand(self):
        """
             Given
                 valid file command parameters and --background
             When
                 CommandParser.parse_args() is called
             Then
                 FileEnhanceCommand with correct background should be called.
             """
        # Arrange
        mocked_enhance_command = MockedFileEnhanceCommand()
        mocked_template_command = MockedTemplateCommand()
        class_under_test = CommandParser(mocked_enhance_command, mocked_template_command)
        args = "whitebrush --background #813A3A cookie.png".split(' ')
        expected = "#813A3A"

        # Act
        sys.argv = args
        class_under_test.parse_args()

        # Assert
        self.assertTrue(mocked_enhance_command.called)
        self.assertEqual(mocked_enhance_command.used_configuration.background_color, expected)
        self.assertEqual(mocked_enhance_command.amount_of_processed_files, 1)

    def test_parse_args_given_files_with_foreground_tag_should_call_FileEnhanceCommand(self):
        """
             Given
                 valid file command parameters and --foreground
             When
                 CommandParser.parse_args() is called
             Then
                 FileEnhanceCommand with correct foreground should be called.
             """
        # Arrange
        mocked_enhance_command = MockedFileEnhanceCommand()
        mocked_template_command = MockedTemplateCommand()
        class_under_test = CommandParser(mocked_enhance_command, mocked_template_command)
        args = "whitebrush --foreground #728599 cookie.png".split(' ')
        expected = "#728599"

        # Act
        sys.argv = args
        class_under_test.parse_args()

        # Assert
        self.assertTrue(mocked_enhance_command.called)
        self.assertEqual(mocked_enhance_command.used_configuration.foreground_color, expected)
        self.assertEqual(mocked_enhance_command.amount_of_processed_files, 1)

    def test_parse_args_given_files_with_template_tag_should_call_TemplateCommand(self):
        """
             Given
                 valid file command parameters and --template
             When
                 CommandParser.parse_args() is called
             Then
                 TemplateCommand should be called.
             """
        # Arrange
        mocked_enhance_command = MockedFileEnhanceCommand()
        mocked_template_command = MockedTemplateCommand()
        class_under_test = CommandParser(mocked_enhance_command, mocked_template_command)
        args = "whitebrush --template blackboard cookie.png strange_image.png".split(' ')

        # Act
        sys.argv = args
        class_under_test.parse_args()

        # Assert
        self.assertTrue(mocked_template_command.called)
        self.assertEqual(mocked_enhance_command.amount_of_processed_files, 2)

    # endregion


# region Helper

class MockedFileEnhanceCommand:
    def __init__(self):
        self.called = False
        self.amount_of_processed_files = 0
        self.used_configuration = EnhancementConfiguration()

    def execute(self, list_of_files, enhance_configuration=EnhancementConfiguration()):
        self.called = True
        self.amount_of_processed_files = len(list_of_files)
        self.used_configuration = enhance_configuration


class MockedTemplateCommand:
    def __init__(self):
        self.called = False

    def execute(self, template, enhance_configuration=EnhancementConfiguration()):
        self.called = True


if __name__ == '__main__':
    unittest.main()

# endregion
