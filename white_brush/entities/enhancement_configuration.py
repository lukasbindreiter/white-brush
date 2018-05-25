class EnhancementConfiguration:

    def __init__(self, recursive=False, replace_files=False, masked="{name}_brushed{extension}",
                 foreground_color=None, background_color=None, rotation=0):
        self.recursive = recursive
        self.replace_files = replace_files
        self.target_file_mask = masked
        self.rotation = rotation
        self.foreground_color = foreground_color
        self.background_color = background_color
