from . import command


def getTemp(pin):
    """Get temperature reading from DHT11."""

    return (command("Getting temperature", "Dt", int, bytes([pin])))/100


def getHumidity(pin):
    """Get humidity reading from DHT11."""

    return (command("Getting humidity", "Dh", int, bytes([pin])))/100
