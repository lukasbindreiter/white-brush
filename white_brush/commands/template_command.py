from white_brush.entities.enhancement_configuration import EnhancementConfiguration


class TemplateCommand:
    def __init__(self):
        """
            Creates a new TemplateCommand.
        """
        self.default_templates = [("blackboard", "#FFFFFF", "#438D49"), ("whiteboard", "#000000", "#FFFFFF"),
                                  ("note", "#000000", "#E7EA1B")]

    def execute(self, template, enhance_configuration=EnhancementConfiguration()):
        """
        Executes the template command for the given template name and configuration. Replaces the color codes
        if the templates match.
        :param template: template.
        :param enhance_configuration: configuration containing color codes.
        """
        template_data = next((x for x in self.default_templates if x[0].lower() == template.lower()), None)

        if template_data is not None:
            enhance_configuration.foreground_color = template_data[1]
            enhance_configuration.background_color = template_data[2]
