# import packages to run
import const
from sim import batteryEstimate
from testing import motor_test

print(const.projectName)

# run methods from packages and files
batteryEstimate.run('4986 Weathervane Drive, Johns Creek, GA', '11435 Frazier Fir Ln, Alpharetta, GA')
# motor_test.run()
