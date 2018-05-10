from white_brush.command_parser import CommandParser
from white_brush.commands.enhance_command import EnhanceCommand
from white_brush.commands.template_command import TemplateCommand
from white_brush.services.enhance_service import EnhanceService


def main():
    """
    Entry point of the application which parses the given arguments.
    """
    command_parser = CommandParser(EnhanceCommand(EnhanceService()), TemplateCommand())
    command_parser.parse_args()


if __name__ == "__main__":
    main()
