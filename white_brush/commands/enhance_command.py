import os
import pathlib

from white_brush.entities.color_configuration import ColorConfiguration
from white_brush.entities.enhancement_configuration import EnhancementConfiguration


class EnhanceCommand:
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
            self.__enhance_file_or_directory__(file, 0, enhance_configuration)

    def __enhance_file_or_directory__(self, file, counter, enhance_configuration):
        """
        Iterates the files and folders to match correct files which should be enhanced. Also increments file names and matches optional masks.
        :param file: file or directory
        :param counter: subdirectory counter
        :param enhance_configuration: configuration
        """
        if os.path.isdir(file):
            if enhance_configuration.recursive or counter == 0:
                for sub_file in os.listdir(file):
                    self.__enhance_file_or_directory__(file + "/" + sub_file, counter + 1, enhance_configuration)
            return

        if enhance_configuration.replace_files:
            self.__enhance_file__(file, file, enhance_configuration)
        else:
            filename = pathlib.Path(file).stem
            extension = pathlib.Path(file).suffix

            target_file = os.path.dirname(file) + "/" + enhance_configuration.target_file_mask.replace("{name}",
                                                                                                       filename).replace(
                "{extension}",
                extension)
            counter = 1

            while os.path.exists(target_file):
                target_file = os.path.dirname(file) + "/" + enhance_configuration.target_file_mask.replace("{name}",
                                                                                                           filename).replace(
                    "{extension}", " (" + counter + ")" + extension)

            self.__enhance_file__(file, target_file, enhance_configuration)

    def __enhance_file__(self, source_file, target_file, enhance_configuration):
        """
        Enhances the given source file to the target_file if it exists.
        :param source_file: source file
        :param target_file:  target file
        :param enhance_configuration:  configuration
        """
        if not os.path.exists(source_file):
            print("Input '" + source_file + "' does not exist. whitebrush --help")
            return

        print("Enhancing '" + os.path.basename(source_file) + "' to '" + os.path.basename(target_file) + "'.")
        self.file_enhance_service.enhance_file(source_file, target_file,
                                               ColorConfiguration(enhance_configuration.foreground_color,
                                                                  enhance_configuration.background_color))
