import const

# this class is used to set motor values via raspberry pi GPIO
class Motor(object):
    """Manages the currect Angular rotation
    Implements the IO interface using the RPIO lib
    __init_(self, name, pin, kv=1000, RPMMin=1, RPMMax=100, debug=True, simulation=True):
    More info on RPIO in http://pythonhosted.org/RPIO/index.html"""

    # initializes the class with variables default values
    def __init__(self, name, pin, kv=1000, WMin=0, WMax=100, debug=True, simulation=True):
        self.name = name
        self.powered = False
        self.simulation = simulation
        self.__pin = pin
        self.__kv = kv
        self.setWLimits(WMin, WMax)
        self.setDebug(debug)

        self.__W = self.__WMin
        self.__Wh = 10

        try:
            from RPIO import PWM
            self.__IO = PWM.Servo()
        except ImportError:
            self.simulation = True

    # set debugging mode
    def setDebug(self, debug):
        self.__debug = debug
        #if self.__debug:
            #self.__logger.setLevel(logging.DEBUG)
        #else:
            #self.__logger.setLevel(logging.WARNING)

    def getDebug(self):
        return self.__debug

    # set the pin for the motor as GPIO pin numbers
    def setPin(self, pin):
        "set the pin for each motor"
        self.__pin = pin

    def setKv(self, kv):
        "set the kv for each motor"
        self.__kv = kv

    # set the min and max wattage for the motor
    def setWLimits(self, WMin, WMax):
        "set the watts limits for the motor"
        if WMin < 0:
            WMin = 0
        self.__WMin = WMin
        if WMax > 100:
            WMax = 100
        self.__WMax = WMax

    # save the current W as the Wh
    def saveWh(self):
        "Save Wh = current W%"
        self.__Wh = self.__W

    # set the wattage to Wh
    def setWh(self):
        "Sets current W% =Wh"
        self.__W = self.__Wh
        self.setW(self.__W)

    # get current Wh
    def getWh(self):
        "returns current W% =Wh"
        return self.__Wh

    # initialize PWM if not simulating
    def start(self):
        "Run the procedure to init the PWM"
        if not self.simulation:
            try:
                from RPIO import PWM
                self.__IO = PWM.Servo()
                self.powered = True
                #TODO Decide How to manage the WMax < 100
                #to keep anyhow the throttle range 0-100
            except ImportError:
                self.simulation = True
                self.powered = False

    # stop the PWM cleanly
    def stop(self):
        "Stop PWM signal"

        self.setW(0)
        if self.powered:
            self.__IO.stop_servo(self.__pin)
            self.powered = False

    # increase W by steps (default is 1)
    def increaseW(self, step=1):
        "increases W% for the motor"

        self.__W = self.__W + step
        self.setW(self.__W)

    # decrease W by steps (default is 1)
    def decreaseW(self, step=1):
        "decreases W% for the motor"

        self.__W = self.__W - step
        self.setW(self.__W)

    # get current W
    def getW(self):
        "retuns current W%"
        return self.__W

    # set current W
    def setW(self, W):
        "Checks W% is between limits than sets it"

        PW = 0
        self.__W = W
        if self.__W < self.__WMin:
            self.__W = self.__WMin
        if self.__W > self.__WMax:
            self.__W = self.__WMax
        PW = (1000 + (self.__W) * 10)
        # Set servo to xxx us
        if self.powered:
            self.__IO.set_servo(self.__pin, PW)
