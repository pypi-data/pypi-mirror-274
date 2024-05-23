from . import command

def start_monitor(pin):
    """Get value in x-axis from Grove Joystick."""
    command(f"Starting HR monitor on{pin}", "hs", "HS-OK", bytes([pin]))

def get_rate(pin):
    """Get value in x-axis from Grove Joystick."""
    result = command(f"Starting HR monitor on{pin}", "hr", int, bytes([pin]))
    return result