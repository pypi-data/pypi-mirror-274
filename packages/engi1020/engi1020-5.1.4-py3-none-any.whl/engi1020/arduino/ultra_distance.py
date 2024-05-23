from . import command


def getCentimeters(pin):
    """Get distance from ultrasonic in cm."""

    return (command("Getting distance in cm", "uc", int, bytes([pin])))/100


def getInches(pin):
    """Get distance from ultrasonic in inches."""

    return (command("Getting distance in inches", "ui", int, bytes([pin])))/100
