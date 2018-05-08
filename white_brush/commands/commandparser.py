import argparse

class CommandParser:

    def __init__(self, enhanceService):



    def parse_args(self):
        ###
        print("ok")

        parser = argparse.ArgumentParser()
        parser.add_argument("-r", "--recursive", help="increase output verbosity", action="store_true")
        args, unknownargs = parser.parse_known_args()

        if args.recursive:
            print("recursive turned on")

        if len(unknownargs) == 0:
            print ("Please specify atleast one file.")

        print(unknownargs)

        FileEnhanceCommand()


    def foo_command__(selfs, args):
        print("Found the foo command")

    def foo(args):
        print("Hello WOrld")


class FileEnhanceCommand:

    def __init__(self, file_enhance_service):
        self.file_enhance_service = file_enhance_service

    def execute(self, list_of_files):
        for file in list_of_files:
            self.file_enhance_service.enhance_file(file)


