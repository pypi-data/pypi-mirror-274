from .pywincolor import text                        #  ------   Directly prints text with color codes, without replacing the built-in print function.
from .pywincolor import enable_print                # (enable)  Temporarily replaces python's built-in print function.
from .pywincolor import disable_print               # (disable) Temporarily replaces python's built-in print function.
from .pywincolor import enable_rn                   # (enable)  Places crlf at end of string.
from .pywincolor import disable_rn                  # (disable) Does not place a crlf at end of string.
from .pywincolor import enable_print_formatting     # (enable)  Custom handling of specific characters.
from .pywincolor import disable_print_formatting    # (disable) Custom handling of specific characters.
from .pywincolor import enable_sticky_colors        # (enable)  Sticks to the last color used within a string.
from .pywincolor import disable_sticky_colors       # (disable) Sticks to the last color used within a string.