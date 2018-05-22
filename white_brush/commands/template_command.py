from white_brush.entities.enhancement_configuration import \
    EnhancementConfiguration


class TemplateCommand:
    def __init__(self):
        """
        Creates a new TemplateCommand.
        """
        self.default_templates = {
            "blackboard": ("#FFFFFF", "#00471C"),
            "whiteboard": ("#000000", "#FFFFFF"),
            "note": ("#040b33", "#F7EA5E")
        }

        self.aliases = {
            "bw": "whiteboard",
            "blackwhite": "whiteboard",
            "postit": "note"
        }

    def execute(self, template: str,
                enhance_configuration=EnhancementConfiguration()):
        """
        Executes the template command for the given template name and configuration. Replaces the color codes
        if the templates match.

        Args:
            template: template.
            enhance_configuration: configuration containing color codes.
        """
        template = template.lower()
        if template in self.aliases:
            template = self.aliases[template]

        if template in self.default_templates:
            template_data = self.default_templates[template]
            enhance_configuration.foreground_color = template_data[0]
            enhance_configuration.background_color = template_data[1]
