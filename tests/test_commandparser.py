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
        mocked_command = MockedFileEnhanceCommand()
        class_under_test = CommandParser(mocked_command)
        args = "whitebrush cookie.png strange_image.png masterPiece.png".split(' ')

        # Act
        sys.argv = args
        class_under_test.parse_args()

        # Assert
        self.assertTrue(mocked_command.called)
        self.assertFalse(mocked_command.used_configuration.recursive)
        self.assertEqual(mocked_command.amount_of_processed_files, 3)

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
        mocked_command = MockedFileEnhanceCommand()
        class_under_test = CommandParser(mocked_command)
        args = "whitebrush".split(' ')

        # Act
        sys.argv = args
        class_under_test.parse_args()

        # Assert
        self.assertFalse(mocked_command.called)

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
        mocked_command = MockedFileEnhanceCommand()
        class_under_test = CommandParser(mocked_command)
        args = "whitebrush --recursive cookie.png strange_image.png".split(' ')

        # Act
        sys.argv = args
        class_under_test.parse_args()

        # Assert
        self.assertTrue(mocked_command.called)
        self.assertTrue(mocked_command.used_configuration.recursive)
        self.assertEqual(mocked_command.amount_of_processed_files, 1)

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


if __name__ == '__main__':
    unittest.main()

# endregion
