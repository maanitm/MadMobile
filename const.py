#create module to retrieve constants and bindings
class _const:

    class ConstError(TypeError): pass

    def __setattr__(self, name, value):
        if self.__dict__.has_key(name):
            raise self.ConstError, "Can't rebind const(%s)"%name
        self.__dict__[name] = value

    def __delattr__(self, name):
        if self.__dict__.has_key(name):
            raise self.ConstError, "Can't unbind const(%s)"%name
        raise NameError, name

#set the class as a system module
import sys
sys.modules[__name__] = _const()

#set global constants
import const
const.projectName = "MadMobile"

const.rightMotorFrontPin = 1
const.rightMotorBackPin = 2
const.leftMotorFrontPin = 3
const.leftMotorBackPin = 4

const.mapQuestApiKey = "vtJYRcXbeLw2mQ66f6LWDRMaFn4E1D67"
const.googleMapsApiKey = "AIzaSyAuPFEQGq-5JohYzHZxJpQ6buf24tU_dmU"
const.mapboxApiKey = "sk.eyJ1IjoibWFhbml0bSIsImEiOiJjajY1YTFjdDEyMTlzMnFvM3FwcjRxZXY5In0.RF3RkIbvcfDiIK4xB2eBxQ"
