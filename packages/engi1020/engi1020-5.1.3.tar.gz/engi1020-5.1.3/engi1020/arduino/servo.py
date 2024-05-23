from . import command


def setAngle(pin, angle):
    """Set angle of servo motor."""

    command(f"Setting angle {angle}", "sw", "SW-OK", bytes([pin, angle]))


def getAngle(pin):
    """Get angle of servo motor."""

    return (command("Getting angle", "sr", int, bytes([pin])))
