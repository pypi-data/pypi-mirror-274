import ctypes
import sys, re

version               = "5.18.2024"
original_print        = print  # Save the original print function
rn_enabled            = False
sticky_colors_enabled = False
text_formatting       = False

def custom_print(*args, **kwargs):
    # Replaces python's built-in print function.
    text_str = ' '.join(str(arg) for arg in args)  # Convert all arguments to strings and concatenate
    if text_formatting:
        text_str = print_parse(text_str)
    text(text_str)  # Your existing text function

def enable_rn():
    # (enable) Places crlf at end of string.
    global rn_enabled
    rn_enabled = True
    
def disable_rn():
    # (disable) Does not place a crlf at end of string.
    global rn_enabled
    rn_enabled = False


def enable_sticky_colors():
    # (enable) Sticks to the last color used within a string.
    global sticky_colors_enabled
    sticky_colors_enabled = True
    
def disable_sticky_colors():
    # (disable) Sticks to the last color used within a string.
    global sticky_colors_enabled
    sticky_colors_enabled = False

def enable_print_formatting():
    # (enable) Custom handling of specific characters.
    global text_formatting
    text_formatting = True
    
def disable_print_formatting():
    # (disable) Custom handling of specific characters.
    global text_formatting
    text_formatting = False

def enable_print():
    enable_rn()
    __builtins__["print"] = custom_print

def disable_print():
    disable_rn()
    __builtins__["print"] = original_print

def print_parse(text_format):
    '''
        main parser for custom_print function.
    '''
    
    # Define the color codes replacement pattern.
    color_code_pattern = re.compile(r'(!@\d{2},\d{2})')
    
    # Function to escape color codes by replacing commas with a placeholder.
    def escape_color_codes(match):
        # Use the null character as a placeholder for commas within color codes.
        return match.group(0).replace(',', '\x00')

    # Escape the color codes in the text to prevent altering color codes with commas.
    text_format = color_code_pattern.sub(escape_color_codes, text_format)

    # Replacement dictionary for characters, excluding commas.
    replacements = {
        "=": "!@11,00=!@07,00",
        ">": "!@04,00>!!",
        "<": "!@04,00<!!",
        "(": "!@04,00(!@12,00",
        ")": "!@04,00)!!",
        "[": "!@03,00[!@01,00",
        "]": "!@03,00]!!",
        ":": "!@06,00:!!",
        "%": "!@02,00%!!",
        "#": "!@02,00#!!",
        "/": "!@15,00/!!",
        "\\": "!@15,00\\!!",
        "|": "!@14,00|!!",
        "&": "!@05,00&!!",
        "*": "!@11,00*!!",
        "^": "!@12,00^!!",
        ";": "!@09,00;!!",
        ".": "!@09,00.!!",
        "-": "!@06,00-!!",
        "=": "!@11,00=!@07,00",
        "?": "!@14,00?!!"
    }    
    
    # Apply replacements.
    for char, replacement in replacements.items():
        text_format = text_format.replace(char, replacement)

    # Replace the placeholder with a comma within color codes.
    text_format = text_format.replace('\x00', ',')

    # First, split the text by color code boundaries.
    parts = re.split('(!@\d{2},\d{2})', text_format)
    
    # Process parts that are not color codes.
    parts = [part if color_code_pattern.match(part) else part.replace(',', '!@10,00,!@07,00') for part in parts]
    
    # Reassemble the text.
    text_format = ''.join(parts)
    
    # Handle special cases for 'Error' and 'Success' messages.
    if 'Error' in text_format:
        text_format = f"!@04,00{text_format}!@07,00"  # Red text for errors.
    elif 'Success' in text_format or 'Successfully' in text_format:
        text_format = f"!@02,00{text_format}!@07,00"  # Green text for success messages.
        
    def handle_multiple_quotes(quote_char, text_format, quoted_color_code="!@10,00"):
        new_text = ""
        in_quotes = False
        quote_color_reset = quoted_color_code

        # Iterate over the characters in the text format.
        for char in text_format:
            if char == quote_char:
                # Toggle the in_quotes flag.
                in_quotes = not in_quotes
                
                if in_quotes:
                    # Opening quote
                    new_text += quoted_color_code + quote_char
                else:
                    # Closing quote
                    new_text += quote_char + "!!"
                
            elif in_quotes:
                # If we are inside quotes, apply color codes to the special characters.
                if char == '-':
                    new_text += "!@06,00-"
                elif char == '.':
                    new_text += "!@09,00.!!"
                elif char == '/':
                    new_text += "!@15,00/"
                elif char == '\\':
                    new_text += "!@15,00\\"
                else:
                    new_text += char
            else:
                # If we are outside quotes, just add the character.
                new_text += char

            # After processing a special character inside quotes, revert to the quoted color.
            if in_quotes and char in "-/\\.":
                new_text += quote_color_reset

        # Ensure the color is reset at the end if the last segment was inside quotes.
        if not in_quotes:
            new_text += "!@07,00"

        return new_text

    
    def remove_reset_inside_quotes(text_format, quote_char="'"):
        # Pattern to find quoted text
        quoted_text_pattern = re.compile(rf"{quote_char}[^{quote_char}]*{quote_char}")

        def replacement(match):
            # Remove all instances of '!!' inside quotes
            return match.group(0).replace('!!', '')

        # Replace all quoted segments with the modified ones without '!!'
        return quoted_text_pattern.sub(replacement, text_format)

    # Now you can call this function to clean up '!!' inside quotes
    text_format = remove_reset_inside_quotes(text_format)
    text_format = remove_reset_inside_quotes(text_format, quote_char='"')
    
    # Apply color to hyphens within quotes
    text_format = handle_multiple_quotes("'", text_format)
    text_format = handle_multiple_quotes('"', text_format)
    
    if sticky_colors_enabled:
        text_format = text_format.replace('!!', '') 
    else:
        text_format = text_format.replace('!!', '!@07,00') 
    
    return text_format

def parse_color_code(code):
    """
    Parses the color code string and returns the foreground and background color values.
    Supports hexadecimal format.
    """
    fg, bg = code[:2], code[3:]  # Split the 5-byte code into foreground and background
    fg_color = int(fg, 16) if any(c in 'ABCDEFabcdef' for c in fg) else int(fg)
    bg_color = int(bg, 16) if any(c in 'ABCDEFabcdef' for c in bg) else int(bg)

    if 0 <= fg_color <= 15 and 0 <= bg_color <= 15:
        return fg_color, bg_color
    else:
        raise ValueError("Invalid color code. Must be between 0-15 or 0-F.")

def text(text):
    """ Function to colorize text based on color codes. """
    std_handle = ctypes.windll.kernel32.GetStdHandle(-11)

    ctypes.windll.kernel32.SetConsoleTextAttribute(std_handle, 7)  # Reset to default color at the start.
    last_index = 0

    while True:
        start_index = text.find('!@', last_index)
        if start_index == -1:
            break

        # Print text before color code
        sys.stdout.write(text[last_index:start_index])
        sys.stdout.flush()

        # Extract color code
        color_code_str = text[start_index + 2:start_index + 7]
        end_index = start_index + 7

        try:
            fg_color, bg_color = parse_color_code(color_code_str)
            color_code = fg_color | (bg_color << 4)
            ctypes.windll.kernel32.SetConsoleTextAttribute(std_handle, color_code)
        except ValueError:
            # If invalid color code, print as is.
            sys.stdout.write(text[start_index:end_index])
            sys.stdout.flush()

        last_index = end_index

    # Print remaining text
    sys.stdout.write(text[last_index:])
    sys.stdout.flush()
    
    if rn_enabled:
        sys.stdout.write('\r\n')
        sys.stdout.flush()

    ctypes.windll.kernel32.SetConsoleTextAttribute(std_handle, 7)  # Reset to default color at the end.

original_print = print

"""

 Example usage:
  
  import pywincolor
  pywincolor.text("!@04,11  Red Text black bg  !@07,2  Blue text, bright white bg !! \r\n")
  pywincolor.text("!@13,12 magenta on magenta !@02,15 Blue text, bright white bg !! abc \r\n")
  pywincolor.text("!@12  red text black bg by default  !@00,09 Blue text, black bg by default !! ")

    -or-
  
  import pywincolor
  pywincolor.enable_print()                          # by default, this triggers pywincolor.enable_rn which appends \r\n
  print("!@05,00This is purple text!!.")     # Text used with Print will be colored.
  pywincolor.disable_rn()                            # Now text used with print() function will not include \r\n
  print("This text does not have CRLF appended.") # (ie. no \r\n newline instruction.)
  pywincolor.enable_rn()                             # \r\n is added to print() string. 
  pywincolor.disable_print()                         # print() function is now returned to it's original state. 
  pywincolor.text("!@03,00Blue text here.")          # pywincolor.text still operates.

    -or-
   
  pywincolor.enable_print()            
  pywincolor.enable_sticky_colors()    
  pywincolor.enable_print_formatting() 
  print("> All red text Here. ")

"""
  
  
  