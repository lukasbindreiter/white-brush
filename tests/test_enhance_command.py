import pathlib
import unittest

from white_brush.commands.enhance_command import EnhanceCommand
from white_brush.entities.color_configuration import ColorConfiguration
from white_brush.entities.enhancement_configuration import EnhancementConfiguration


class TestEnhanceCommand(unittest.TestCase):

    # region execute

    def test_execute_given_file_enhancement_configuration_should_call_service(self):
        # Arrange
        files = ['../.pytest_cache/testfile1.png']
        mocked_enhance_service = MockedEnhanceService()
        class_under_test = EnhanceCommand(mocked_enhance_service)
        enhance_configuration = EnhancementConfiguration()

        # Act
        f = open(files[0], "w+")
        f.write("Hello World")
        f.close()

        class_under_test.execute(files, enhance_configuration)

        # Assert
        self.assertTrue(mocked_enhance_service.called, True)

    def test_execute_given_multiple_files_enhancement_configuration_should_call_service(self):
        # Arrange
        files = ['../.pytest_cache/testfile1.png','../.pytest_cache/testfile2.png','../.pytest_cache/testfile3.png']
        mocked_enhance_service = MockedEnhanceService()
        class_under_test = EnhanceCommand(mocked_enhance_service)
        enhance_configuration = EnhancementConfiguration()

        # Act
        for i in range(1,3):
            f = open(files[i], "w+")
            f.write("Hello World")
            f.close()

        class_under_test.execute(files, enhance_configuration)

        # Assert
        self.assertTrue(mocked_enhance_service.called, True)
        self.assertEqual(mocked_enhance_service.called_counter, 3)

    def test_execute_given_files_and_directories_enhancement_configuration_should_call_service(self):
        # Arrange
        files = ['../.pytest_cache/testfile1.png', '../.pytest_cache/testdirectory']
        mocked_enhance_service = MockedEnhanceService()
        class_under_test = EnhanceCommand(mocked_enhance_service)
        enhance_configuration = EnhancementConfiguration()

        # Act
        pathlib.Path(files[1]).mkdir(parents=True, exist_ok=True)
        f = open(files[1] + "/sample.jpg", "w+")
        f.write("Hello World")
        f.close()

        class_under_test.execute(files, enhance_configuration)

        # Assert
        self.assertTrue(mocked_enhance_service.called, True)
        self.assertEqual(mocked_enhance_service.called_counter, 2)

    def test_execute_given_files_and_subdirectories_configuration_should_call_service(self):
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
        self.assertTrue(mocked_enhance_service.called, True)
        self.assertEqual(mocked_enhance_service.called_counter, 3)
        self.assertEqual(mocked_enhance_service.called_color_configuration.foreground_color, expected_foreground)
        self.assertEqual(mocked_enhance_service.called_color_configuration.background_color, expected_background)

    # endregion


# region Helper

class MockedEnhanceService:
    def __init__(self):
        self.called = False
        self.called_counter = 0
        self.called_color_configuration = ColorConfiguration()

    def enhance_file(self, input_file_name, output_file_name, color_configuration):
        self.called = True
        self.called_counter += 1
        self.called_color_configuration = color_configuration


if __name__ == '__main__':
    unittest.main()

# endregion
