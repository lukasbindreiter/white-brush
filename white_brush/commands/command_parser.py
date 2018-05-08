import argparse

from white_brush.entities.enhancement_configuration import EnhancementConfiguration


class CommandParser:
    def __init__(self, enhance_command):
        """
        Creates a new CommandParser with the enhance_command as dependency.
        :param enhance_command: command executing the enhancement process.
        """
        self.enhance_command = enhance_command

    def parse_args(self):
        """
        Takes the sys.argv arguments and parses it by the given ArgumentParser specifications. Calls the
        command implementations
        :return: True when command got executed. False when command could not be parsed.
        """
        parser = argparse.ArgumentParser()
        enhancement_configuration = EnhancementConfiguration()

        parser.add_argument("-r", "--recursive",
                            help="Selects all sub files in sub directories of the given files and directories.")
        # TODO: Add all other commands displayed in issue

        args, unknown_args = parser.parse_known_args()

        if args.recursive:
            enhancement_configuration.recursive = True

        if len(unknown_args) == 0:
            print("Please specify atleast one file.")
            return False

        print(unknown_args)
        self.enhance_command.execute(unknown_args, enhancement_configuration)
