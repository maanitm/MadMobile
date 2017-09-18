import const

# this class is used to set motor values via raspberry pi GPIO
class Motor(object):
    """Manages the currect Angular rotation
    Implements the IO interface using the RPIO lib
    __init_(self, name, pin, kv=1000, RPMMin=1, RPMMax=100, debug=True, simulation=True):
    More info on RPIO in http://pythonhosted.org/RPIO/index.html"""

    # initializes the class with variables default values
    def __init__(self):
        print("motor")
