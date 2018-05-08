import os

from white_brush.entities.enhancement_configuration import EnhancementConfiguration


class FileEnhanceCommand:
    def __init__(self, file_enhance_service):
        """
        Creates a new FileEnhanceCommand with the file_enhance_service as dependency.
        :param file_enhance_service: dependency
        """
        self.file_enhance_service = file_enhance_service

    def execute(self, list_of_files, enhance_configuration=EnhancementConfiguration()):
        """
        Executes the default command for the given file and directory parameters and additional configuration details.
        :param list_of_files: list of files and directories
        :param enhance_configuration: configuration values
        """
        for file in list_of_files:
            if os.path.isdir(file):
                for sub_file in os.listdir(file):
                    if not os.path.isdir(file):
                        self.file_enhance_service.enhance_file(sub_file)
            else:
                self.file_enhance_service.enhance_file(file)

        # TODO: Add tests
