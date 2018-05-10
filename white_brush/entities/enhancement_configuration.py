class EnhancementConfiguration:

    def __init__(self, recursive=False, replace_files=False, masked="{name}_brushed{extension}",
                 foreground_color="#default", background_color="#default"):
        self.recursive = recursive
        self.replace_files = replace_files
        self.target_file_mask = masked
        self.foreground_color = foreground_color
        self.background_color = background_color
