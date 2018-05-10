import unittest

from white_brush.commands.enhance_command import EnhanceCommand
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

    # endregion


# region Helper

class MockedEnhanceService:
    def __init__(self):
        self.called = False
        self.called_counter = 0

    def enhance_file(self, input_file_name, output_file_name, color_configuration):
        self.called = True
        self.called_counter += 1


if __name__ == '__main__':
    unittest.main()

# endregion
