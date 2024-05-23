from . import command

def set_colour_rgb(pin, count, led, red, green, blue):
    """Set the RGB colour of an RGB LED

    Parameters:
      pin (int): digital pin
      count (int): number of chained LEDs
      led (int): index of led (starting at 0)
      red (int): 0-255
      green (int): 0-255
      blue (int): 0-255
    """

    command(f"Setting RGB LED {led} on {pin} to RGB ({red}, {green}, {blue})",
            "lr", "lC-OK", bytes([pin, count, led, red, green, blue]))

def set_colour_hsv(pin, count, led, hue, sat, val):
    """Set the HSV of the RGB LED.

    Parameters:
      pin (int): digital pin
      count (int): number of chained LEDs
      led (int): index of led (starting at 0)
      hue (float): 0-1
      sat (float): 0-1
      val (float): 0-1
    """

    command(f"Setting RGB LED to HSV ({hue}, {sat}, {val})",
            "lh", "lH-OK", bytes([pin, count, led, int(hue*255), int(sat*255), int(val*255)]))