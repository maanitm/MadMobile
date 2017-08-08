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

import sys
sys.modules[__name__] = _const()

import const
const.projectName = "MadMobile"
const.rightMotorFrontPin = 1
const.rightMotorBackPin = 2
const.leftMotorFrontPin = 3
const.leftMotorBackPin = 4
