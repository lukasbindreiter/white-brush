import argparse

from white_brush.entities.enhancement_configuration import EnhancementConfiguration


class CommandParser:
    def __init__(self, enhance_command, template_command, rotation_command):
        """
        Creates a new CommandParser with the enhance_command and template_command as dependency.

        Args:
            enhance_command: command executing the enhancement process.
            template_command: command matching the template to the color codes
            rotation_command: command matching the rotation degrees
        """
        self.enhance_command = enhance_command
        self.template_command = template_command
        self.rotation_command = rotation_command

    def parse_args(self):
        """
        Takes the sys.argv arguments and parses it by the given ArgumentParser specifications. Calls the
        command implementations.

        Returns:
            True when command got executed. False when command could not be parsed.
        """
        parser = argparse.ArgumentParser()
        enhancement_configuration = EnhancementConfiguration()

        parser.add_argument("-r", "--recursive",
                            help="Selects all sub files in sub directories of the given files and directories.",
                            action="store_true")
        parser.add_argument("-c", "--convert",
                            help="Replaces the input files with their output files.", action="store_true")
        parser.add_argument("-m", "--mask",
                            help="Changes the mask of the target files. Default format: {name}_brushed{extension}"
                                 " where name is " "the placeholder for filename and extension the placeholder "
                                 "for the file extension. --convert ignores this tag.")
        parser.add_argument("-f", "--foreground",
                            help="Uses the given HTML Color code as foreground color.")
        parser.add_argument("-b", "--background",
                            help="Uses the given HTML Color code as background color.")
        parser.add_argument("-cw", "--clockwise",
                            help="Uses the given degree to rotate the target file clockwise. Degrees have to be divisible by 90.")
        parser.add_argument("-ccw", "--counterclockwise",
                            help="Uses the given degree to rotate the target file counterclockwise. Degrees have to be divisible by 90.")
        parser.add_argument("-t", "--template",
                            help="Uses the chosen template color codes for conversion. Templates: whiteboard, blackboard, note.")

        args, unknown_args = parser.parse_known_args()

        if args.recursive:
            enhancement_configuration.recursive = True
        if args.convert:
            enhancement_configuration.replace_files = True
        if args.mask:
            enhancement_configuration.target_file_mask = args.mask
        if args.background:
            enhancement_configuration.background_color = args.background
        if args.foreground:
            enhancement_configuration.foreground_color = args.foreground
        if args.clockwise:
            self.rotation_command.execute(args.clockwise, False, enhancement_configuration)
        if args.counterclockwise:
            self.rotation_command.execute(args.counterclockwise, True, enhancement_configuration)
        if args.template:
            self.template_command.execute(args.template, enhancement_configuration)

        if len(unknown_args) == 0:
            print("Please specify atleast one file. whitebrush --help")
            return False

        self.enhance_command.execute(unknown_args, enhancement_configuration)
