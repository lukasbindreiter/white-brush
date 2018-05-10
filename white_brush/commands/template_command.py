import os

from white_brush.entities.enhancement_configuration import EnhancementConfiguration


class TemplateCommand:
    def __init__(self):
        self.default_templates = [("blackboard", "#FFFFFF", "#438D49"), ("whiteboard", "#000000", "#FFFFFF"),
                                  ("note", "#000000", "#E7EA1B")]

    def execute(self, template, enhance_configuration=EnhancementConfiguration()):
        templates = self.default_templates
