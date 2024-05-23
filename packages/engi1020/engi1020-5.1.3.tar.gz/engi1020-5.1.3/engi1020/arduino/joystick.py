from . import command
import math

#Min and max x, y, values when joystick connected to A3 on Grove Shield
#Determined experimentally
minX = 206
maxX = 798
minY = 797
maxY = 954


def getX():
    """Get value in x-axis from Grove Joystick."""
    result = command("Getting joystick value in x-axis on port A3", "ar", int, bytes([3]))
    x_norm = (2/(maxX-minX)*(result - minX) - 1)
    if -1 <= x_norm <= 1:
        return x_norm
    elif x_norm < -1:
        return -1.0
    else:
        return 1.0 

def getY():
    """Get value in x-axis from Grove Joystick."""
    result = command("Getting joystick value in y-axis on port A3", "ar", int, bytes([4]))
    
    y_norm = (2/(maxY-minY)*(result - minY) - 1)
    if -1 <= y_norm <= 1:
        return y_norm
    elif y_norm < -1:
        return -1.0
    else:
        return 1.0

def getR_Theta():
    """Get acceleration in x-axis from Grove Beginner Accelerometer."""

    x = getX()
    y = getY()

    r = (x**2 + y**2)**0.5
    theta = math.atan2(y, x)

    return (r, theta)