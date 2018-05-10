import pathlib
import unittest

from white_brush.commands.enhance_command import EnhanceCommand
from white_brush.entities.color_configuration import ColorConfiguration
from white_brush.entities.enhancement_configuration import EnhancementConfiguration


class TestEnhanceCommand(unittest.TestCase):

    # region execute

    def test_execute_given_file_enhancement_configuration_should_call_service(self):
        """
             Given
                   valid file
             When
                   CommandParser.parse_args() is called
             Then
                   Enhance service should be called.
        """
        # Arrange
        files = ['../.pytest_cache/testfile1.png']
        mocked_enhance_service = MockedEnhanceService()
        class_under_test = EnhanceCommand(mocked_enhance_service)
        enhance_configuration = EnhancementConfiguration()

        # Act
        pathlib.Path("../.pytest_cache").mkdir(parents=True, exist_ok=True)
        f = open(files[0], "w+")
        f.write("Hello World")
        f.close()

        class_under_test.execute(files, enhance_configuration)

        # Assert
        self.assertTrue(mocked_enhance_service.called)

    def test_execute_given_multiple_files_enhancement_configuration_should_call_service(self):
        """
             Given
                   valid files
             When
                   CommandParser.parse_args() is called
             Then
                   Enhance service should be called for each file.
        """
        # Arrange
        files = ['../.pytest_cache/testfile1.png', '../.pytest_cache/testfile2.png', '../.pytest_cache/testfile3.png']
        mocked_enhance_service = MockedEnhanceService()
        class_under_test = EnhanceCommand(mocked_enhance_service)
        enhance_configuration = EnhancementConfiguration()

        # Act
        pathlib.Path("../.pytest_cache").mkdir(parents=True, exist_ok=True)
        for i in range(1, 3):
            f = open(files[i], "w+")
            f.write("Hello World")
            f.close()

        class_under_test.execute(files, enhance_configuration)

        # Assert
        self.assertTrue(mocked_enhance_service.called)
        self.assertEqual(3, mocked_enhance_service.called_counter)

    def test_execute_given_files_and_directories_enhancement_configuration_should_call_service(self):
        """
           Given
                 valid files and subdirectories without recursive tag.
           When
                 CommandParser.parse_args() is called
           Then
                 Enhance service with all files and only files in the first sub diretory should be called.
        """
        # Arrange
        files = ['../.pytest_cache/testfile1.png', '../.pytest_cache/testdirectory']
        mocked_enhance_service = MockedEnhanceService()
        class_under_test = EnhanceCommand(mocked_enhance_service)
        enhance_configuration = EnhancementConfiguration()

        # Act
        pathlib.Path("../.pytest_cache").mkdir(parents=True, exist_ok=True)
        pathlib.Path(files[1]).mkdir(parents=True, exist_ok=True)
        f = open(files[1] + "/sample.jpg", "w+")
        f.write("Hello World")
        f.close()

        class_under_test.execute(files, enhance_configuration)

        # Assert
        self.assertTrue(mocked_enhance_service.called)
        self.assertEqual(2, mocked_enhance_service.called_counter)

    def test_execute_given_files_and_subdirectories_configuration_should_call_service(self):
        """
            Given
                  valid files and subdirectories with recursive tag.
            When
                  CommandParser.parse_args() is called
            Then
                  Enhance service with all files and not directories should be called.
        """
        # Arrange
        files = ['../.pytest_cache/testfile1.png', '../.pytest_cache/testdirectory']
        mocked_enhance_service = MockedEnhanceService()
        class_under_test = EnhanceCommand(mocked_enhance_service)
        enhance_configuration = EnhancementConfiguration()
        enhance_configuration.recursive = True
        enhance_configuration.foreground_color = "#fore"
        enhance_configuration.background_color = "#back"

        expected_foreground = "#fore"
        expected_background = "#back"

        # Act
        pathlib.Path("../.pytest_cache").mkdir(parents=True, exist_ok=True)
        pathlib.Path(files[1]).mkdir(parents=True, exist_ok=True)
        f = open(files[1] + "/sample.jpg", "w+")
        f.write("Hello World")
        f.close()
        pathlib.Path(files[1] + "/subtestdirectory").mkdir(parents=True, exist_ok=True)
        f = open(files[1] + "/subtestdirectory/subsample.jpg", "w+")
        f.write("Hello World")
        f.close()

        class_under_test.execute(files, enhance_configuration)

        # Assert
        self.assertTrue(mocked_enhance_service.called)
        self.assertEqual(3, mocked_enhance_service.called_counter)
        self.assertEqual(expected_foreground, mocked_enhance_service.called_color_configuration.foreground_color)
        self.assertEqual(expected_background, mocked_enhance_service.called_color_configuration.background_color)

    def test_execute_given_files_and_convert_should_call_service(self):
        """
             Given
                   valid files and replace file tag
             When
                   CommandParser.parse_args() is called
             Then
                   Enhance service with the same file names should be called.
        """
        # Arrange
        files = ['../.pytest_cache/testfile1.png', '../.pytest_cache/testfile2.png', '../.pytest_cache/testfile3.png']
        mocked_enhance_service = MockedEnhanceService()
        class_under_test = EnhanceCommand(mocked_enhance_service)
        enhance_configuration = EnhancementConfiguration()
        enhance_configuration.replace_files = True

        # Act
        class_under_test.execute(files, enhance_configuration)

        # Assert
        self.assertTrue(mocked_enhance_service.called)
        self.assertEqual(3, mocked_enhance_service.called_counter)
        self.assertEqual(3, mocked_enhance_service.same_file_name_amount)

    def test_execute_given_files_and_existing_target_should_call_service(self):
        """
            Given
                 valid file and existing target file
            When
                 CommandParser.parse_args() is called
            Then
                 Enhance service should be called.
        """
        # Arrange
        files = ['../.pytest_cache/testfile5.png']
        mocked_enhance_service = MockedEnhanceService()
        class_under_test = EnhanceCommand(mocked_enhance_service)
        enhance_configuration = EnhancementConfiguration()

        # Act
        pathlib.Path("../.pytest_cache").mkdir(parents=True, exist_ok=True)
        f = open("../.pytest_cache/testfile5_brushed.png", "w+")
        f.write("Hello World")
        f.close()
        f = open("../.pytest_cache/testfile5.png", "w+")
        f.write("Hello World")
        f.close()
        class_under_test.execute(files, enhance_configuration)

        # Assert
        self.assertTrue(mocked_enhance_service.called)
        self.assertEqual(1, mocked_enhance_service.called_counter)

    # endregion


# region Helper

class MockedEnhanceService:
    def __init__(self):
        self.called = False
        self.called_counter = 0
        self.called_color_configuration = ColorConfiguration()
        self.same_file_name_amount = 0

    def enhance_file(self, input_file_name, output_file_name, color_configuration):
        self.called = True
        self.called_counter += 1
        self.called_color_configuration = color_configuration
        if input_file_name == output_file_name:
            self.same_file_name_amount += 1


if __name__ == '__main__':
    unittest.main()

# endregion
