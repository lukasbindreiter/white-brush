import unittest

from white_brush.commands.rotation_command import RotationCommand
from white_brush.entities.enhancement_configuration import \
    EnhancementConfiguration


class TestRotationCommand(unittest.TestCase):

    # region execute

    def test_execute_rotation_divisible_by_90_should_set_rotation(self):
        """
        Given
            a rotation divisible by 90
        When
            RotationCommand.execute() is called
        Then
            the configuration should be filled with the rotation.
        """
        # Arrange
        class_under_test = RotationCommand()
        rotation = "90"
        enhance_configuration = EnhancementConfiguration()
        expected_rotation = 90

        # Act
        class_under_test.execute(rotation, False, enhance_configuration)

        # Assert
        self.assertEqual(expected_rotation, enhance_configuration.rotation)

    def test_execute_rotation_not_divisible_by_90_should_not_set_rotation(self):
        """
        Given
            a rotation not divisible by 90
        When
            RotationCommand.execute() is called
        Then
            the configuration should not be filled with the rotation.
        """
        # Arrange
        class_under_test = RotationCommand()
        rotation = 66
        enhance_configuration = EnhancementConfiguration()
        expected_rotation = 0

        # Act
        class_under_test.execute(rotation, False, enhance_configuration)

        # Assert
        self.assertEqual(expected_rotation, enhance_configuration.rotation)

    def test_execute_rotation_bigger_than_360_should_not_set_rotation(self):
        """
        Given
            a rotation bigger than 360
        When
            RotationCommand.execute() is called
        Then
            the configuration should not be filled with the rotation.
        """
        # Arrange
        class_under_test = RotationCommand()
        rotation = 360 + 90
        enhance_configuration = EnhancementConfiguration()
        expected_rotation = 0

        # Act
        class_under_test.execute(rotation, False, enhance_configuration)

        # Assert
        self.assertEqual(expected_rotation, enhance_configuration.rotation)

    def test_execute_rotation_smaller_than_minus_360_should_not_set_rotation(self):
        """
        Given
            a rotation smaller than -360
        When
           RotationCommand.execute() is called
        Then
            the configuration should not be filled with the rotation.
        """
        # Arrange
        class_under_test = RotationCommand()
        rotation = -360 - 90
        enhance_configuration = EnhancementConfiguration()
        expected_rotation = 0

        # Act
        class_under_test.execute(rotation, False, enhance_configuration)

        # Assert
        self.assertEqual(expected_rotation, enhance_configuration.rotation)

    def test_execute_minus_rotation_divisible_by_90_should_set_rotation(self):
        """
        Given
            a rotation smaller than 0 divisble by 90
        When
           RotationCommand.execute() is called
        Then
            the configuration should not be filled with the rotation.
        """
        # Arrange
        class_under_test = RotationCommand()
        rotation = -270
        enhance_configuration = EnhancementConfiguration()
        expected_rotation = -270

        # Act
        class_under_test.execute(rotation, False, enhance_configuration)

        # Assert
        self.assertEqual(expected_rotation, enhance_configuration.rotation)

    def test_execute_rotation_counter_clockwise_divisible_by_90_should_set_rotation(self):
        """
        Given
            a rotation smaller than -360
        When
            RotationCommand.execute() is called
        Then
            the configuration should not be filled with the rotation.
        """
        # Arrange
        class_under_test = RotationCommand()
        rotation = 270
        enhance_configuration = EnhancementConfiguration()
        expected_rotation = -270

        # Act
        class_under_test.execute(rotation, True, enhance_configuration)

        # Assert
        self.assertEqual(expected_rotation, enhance_configuration.rotation)

    # endregion


# region Helper

if __name__ == '__main__':
    unittest.main()

# endregion
