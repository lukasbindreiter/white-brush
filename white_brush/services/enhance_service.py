from white_brush import io
from white_brush.enhance import enhance


class EnhanceService:
    def enhance_file(self, input_file_name, output_file_name,
                     color_configuration):
        """
        Enhances the given input_file_name with the given color configuration to the output_file_name.

        Args:
            input_file_name: path to the input file
            output_file_name: path to the output file
            color_configuration:  color_configuration
        """
        # TODO: Use the configuration
        img = io.read_image(input_file_name)
        out = enhance(img)
        io.write_image(output_file_name, out)
