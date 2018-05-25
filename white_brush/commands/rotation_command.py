from white_brush.entities.enhancement_configuration import \
    EnhancementConfiguration


class RotationCommand:
    def execute(self, rotation, counter_clock_wise: bool, enhance_configuration=EnhancementConfiguration()):
        """
        Executes the rotation command for the given rotation degree and configuration.

        Args:
            counter_clock_wise: counter clockwise.
            rotation: rotation degree
            enhance_configuration: configuration
        """

        result = self.__try_parse_int(rotation)
        if not result[1]:
            return

        rotation = result[0]

        if rotation % 90 != 0:
            return

        if rotation > 360 or rotation < -360:
            return

        if counter_clock_wise:
            rotation = rotation * -1

        enhance_configuration.rotation = rotation

    def __try_parse_int(self, value):
        try:
            return int(value), True
        except ValueError:
            return value, False
