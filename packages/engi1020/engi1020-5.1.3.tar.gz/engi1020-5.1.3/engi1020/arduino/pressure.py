from . import command


def getTemperature():
    """Get temperature from Grove Beginner Air Pressure (BMP280)."""

    return (command("Getting temperature (BMP280)", "pt", int)/100)

def getPressure():
    """Get air pressure (BMP280)."""

    return (command("Getting air pressure", "pp", int)/100)

def getAltitude():
    """Get altitude (BMP280)."""

    return (command("Getting altitude", "pa", int)/100)
