from . import command


## Need to cast to signed int
def getAccelX():
    """Get acceleration in x-axis from Grove Beginner Accelerometer."""
    result = command("Getting acceleration in x-axis", "3x", int)
    if result >= 2**15:
        result -= 2**16
    return (result/100)

def getAccelY():
    """Get acceleration in x-axis from Grove Beginner Accelerometer."""

    result = command("Getting acceleration in y-axis", "3y", int)
    if result >= 2**15:
        result -= 2**16
    return (result/100)


def getAccelZ():
    """Get acceleration in z-axis from Grove Beginner Accelerometer."""

    result = command("Getting acceleration in z-axis", "3z", int)
    if result >= 2**15:
        result -= 2**16
    return (result/100)

