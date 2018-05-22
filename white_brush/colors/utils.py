import webcolors


def parse_color(color):
    """
    Parses the given color text to rgb values in format (255,255,255).

    Args:
        color: color text to be parsed in format 'red', '#728599', and 255,255,255

    Returns:
        Returns the parsed color as rgb value or None if not parseable.
    """
    try:
        color = webcolors.name_to_rgb(color)
        return color.red, color.green, color.blue
    except ValueError:
        pass

    try:
        color = webcolors.hex_to_rgb(color)
        return color.red, color.green, color.blue
    except ValueError:
        pass

    try:
        data = color.split(",")
        return int(data[0]), int(data[1]), int(data[2])
    except Exception:
        pass

    return None
