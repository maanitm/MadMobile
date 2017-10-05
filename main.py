# import packages to run
import const
# from testing import navSimulation
# from testing import sidewalkTracking
from run.raspberrypi import raspberryMaster

print(const.projectName)

# run methods from packages and files
# navSimulation.run('4986 Weathervane Drive, Johns Creek, GA', '11585 Jones Bridge Rd Ste 500, Johns Creek, GA')
# sidewalkTracking.run(0)
raspberryMaster.startDrive()
