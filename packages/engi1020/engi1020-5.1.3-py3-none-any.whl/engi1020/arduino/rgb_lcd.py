from . import command

cur_row = 0
cur_col = 0

def clear():
    """Clear the RGB-LCD display."""

    command("Clearing RGB LCD display", "Rc", "Rc-OK")


def print(message, row = 0, col = 0):
    """Print a message to the RGB LCD screen."

    Parameters:
      message (str): The message to print
      row (int): 0-1
      col (int): 0-15
    """

    global cur_row
    global cur_col
    
    encoded = message.encode('utf-8')

    command(f"Printing '{message}' to RGB LCD display @ ({row}, {col})",
            "Rp", "Rp-OK", bytes([row, col, len(encoded)]), encoded)

    cur_row = row
    cur_col = col + len(encoded)


def set_colour(red, green, blue):
    """Set the backlight colour of the RGB LCD screen.

    Parameters:
      red (int): 0-255
      green (int): 0-255
      blue (int): 0-255
    """

    command(f"Setting RGB LCD backlight colour to ({red}, {green}, {blue})",
            "RC", "RC-OK", bytes([red, green, blue]))
