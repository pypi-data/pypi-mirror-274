import os
import argparse
import sys

# ANSI color dictionary
colors = {
    "almond": 101, "aqua": 36, "aquamarine": 96, "banana": 102, "beige": 103, 
    "bisque": 104, "black": 30, "blue": 34, "bone": 105, "brass": 106, 
    "bronze": 107, "brown": 108, "bubblegum": 109, "buff": 110, "burgundy": 111, 
    "burnt_sienna": 112, "burnt_umber": 113, "cadet_blue": 114, "camel": 115, 
    "candy": 116, "caramel": 117, "celadon": 118, "cerulean": 119, "champagne": 120, 
    "charcoal": 90, "chartreuse": 121, "cherry": 122, "chestnut": 123, "chocolate": 124, 
    "cinnamon": 125, "claret": 126, "copper": 127, "coral": 128, "cornflower": 129, 
    "cranberry": 130, "cream": 131, "cyan": 36, "dark_gray": 90, "denim": 132, 
    "ecru": 133, "eggplant": 134, "emerald": 135, "emerald_green": 136, "forest_green": 32, 
    "frost": 137, "gold": 138, "goldenrod": 139, "gray": 140, "grape": 141, 
    "grass_green": 32, "green": 32, "hot_pink": 142, "hunter_green": 32, "ice_blue": 143, "indigo": 144, 
    "iris": 145, "jade": 146, "jungle_green": 147, "khaki": 148, "lavender": 149, 
    "lemon": 150, "lemonade": 151, "lilac": 152, "lime": 32, "lime_green": 153, 
    "linen": 154, "magenta": 35, "mahogany": 155, "malachite": 156, "maroon": 157, 
    "melon": 158, "midnight_blue": 34, "mint_green": 159, "mocha": 160, "moonstone": 161, 
    "moss_green": 32, "mulberry": 162, "mustard": 163, "navy": 34, "nude": 164, 
    "ocean_blue": 34, "olive": 33, "onyx": 30, "opal": 165, "orange": 38, 
    "orchid": 166, "pale_blue": 167, "pale_pink": 168, "paprika": 169, "peach": 170, 
    "pearl": 171, "periwinkle": 172, "petal_pink": 173, "pine_green": 32, "plum": 174, 
    "powder_blue": 175, "pumpkin": 176, "raspberry": 177, "red": 31, "rose": 178, 
    "rust": 179, "sage": 180, "sapphire": 34, "sea_blue": 34, "seafoam": 181, 
    "seashell": 182, "sepia": 183, "sienna": 184, "sky_blue": 185, "slate_blue": 186, 
    "slate_gray": 90, "snow": 187, "spearmint": 188, "steel_blue": 189, "stone": 190, 
    "strawberry": 191, "sunflower": 192, "tan": 193, "taupe": 194, "teal": 36, 
    "terracotta": 195, "thistle": 196, "tomato": 197, "topaz": 198, "tulip": 199, 
    "turquoise": 200, "vanilla": 201, "violet": 202, "white": 203, "yellow": 33
}

# Mapping of style formats
formats_mapping = {
    "bright": 1,
    "bold": 1,
    "dim": 2,
    "italic": 3,
    "underlined": 4,
    "blink": 5,
    "reverse": 7,
}

# List of all colors
__all__ = list(colors.keys())

# Function to get ANSI color code
def get_ansi_color_code(color):
    """
    Retrieve the ANSI color code for a given color name.

    Parameters:
        color (str): The name of the color.

    Returns:
        int or None: The ANSI color code corresponding to the input color name, or None if the color is not found.

    Example:
        >>> get_ansi_color_code("blue")
        34
    """
    return colors.get(color.lower())

# Function to parse format
def parse_format_to_ansi_code(format_str):
    """
    Parse the format string into its corresponding ANSI code.

    Parameters:
        format_str (str): The format string.

    Returns:
        int: The ANSI code corresponding to the input format.

    Raises:
        Exception: If the input format is not valid.

    Example:
        >>> parse_format_to_ansi_code("bold")
        1
    """
    if isinstance(format_str, str):
        code = formats_mapping.get(format_str)
        if code and code not in range(1, 100):
            raise Exception("Format must be in range(1,100)")
        return code


# Function to get ANSI color function
def create_ansi_color_function(color):
    """
    Create an ANSI color function for the specified color.

    Parameters:
        color (str): The color for which the ANSI function is created.

    Returns:
        function: The created ANSI color function.

    Example:
        >>> green_printer = create_ansi_color_function("green")
        >>> green_printer("Hello, world!", formats=["bold"])
        '\x1b[1;32mHello, world!\x1b[0m'
    """
    def ansi_color_printer(text, formats=None):
        # ensure list
        if not isinstance(formats, (tuple, list)):
            formats = [formats]

        # ensure int
        formats = [parse_format_to_ansi_code(format_str) for format_str in formats if parse_format_to_ansi_code(format_str)]

        code = get_ansi_color_code(color)
        if not code:
            raise Exception("color {} not supported".format(color))
        if formats:
            return "\033[{};{}m{}\033[0m".format(
                ";".join(str(x) for x in formats), code, text
            )
        else:
            return "\033[{}m{}\033[0m".format(code, text)

    return ansi_color_printer

# Function to get text from a file
def read_text_from_file_or_return_text(text_or_filepath):
    """
    Read text from a file or return the provided text if it's not a file path.

    Parameters:
        text_or_filepath (str): The path to the file or the text itself.

    Returns:
        str: The text content.

    Example:
        >>> read_text_from_file_or_return_text("example.txt")
        'This is an example text.'
    """
    if os.path.exists(text_or_filepath):
        with open(text_or_filepath) as file:
            return file.read().strip()
    return text_or_filepath

# Assign ANSI color functions to attributes of the module for each color in __all__
def assign_ansi_color_functions():
    """
    Assign ANSI color functions to attributes of the module for each color in __all__.

    This function dynamically creates ANSI color functions for each color defined
    in the __all__ list and assigns them to attributes of the module.

    Returns:
        None
    """
    for color_name in __all__:
        setattr(sys.modules[__name__], color_name, create_ansi_color_function(color_name.lower()))

# Main function
def main():
    """
    Main function of the program.

    This function parses command-line arguments, assigns ANSI color functions, 
    retrieves text from a file or directly from the input, and prints the formatted text.

    Command-line arguments:
        color (str): The color to apply to the text. Should be one of the colors 
                     defined in the list __all__.
        text (str): The text to be formatted. This can be a path to a file containing 
                    the text or the text itself.
        -s, --style (str, optional): Additional formatting styles to apply to the text. 
                                      These should be one or more of the formatting 
                                      options defined in formats_mapping.

    Example:
        To print the text "Hello, World!" in red and bold:
        >>> python script.py red "Hello, World!" -s bold
    """
    parser = argparse.ArgumentParser(description="Apply ANSI color formatting to text.")
    parser.add_argument("color", choices=__all__, help="The color to apply to the text.")
    parser.add_argument("text", help="The text to be formatted.")
    parser.add_argument("-s", "--style", nargs="*", choices=formats_mapping.keys(), 
                        help="Additional formatting styles to apply to the text.")
    args = parser.parse_args()

    # Get the ANSI color function based on the specified color
    color_function = get_ansi_color_function(args.color)

    # Retrieve text from file or use the provided text
    text = read_text_from_file_or_return_text(args.text)

    # Print the formatted text
    print(color_function(text, args.style))
        
# Load ANSI color functions into module attributes
assign_ansi_color_functions()

# Entry point of the program
if __name__ == "__main__":
    main()