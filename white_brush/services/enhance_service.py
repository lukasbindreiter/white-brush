from white_brush import io
from white_brush.enhance import enhance
from white_brush.entities.color_configuration import ColorConfiguration


class EnhanceService:
    def enhance_file(self, input: str, output: str,
                     config: ColorConfiguration):
        """
        Enhances the given input_file_name with the given color configuration to the output_file_name.

        Args:
            input: path to the input file
            output: path to the output file
            color_configuration:  color_configuration
        """
        img = io.read_image(input)
        out = enhance(img, config)
        io.write_image(output, out)
