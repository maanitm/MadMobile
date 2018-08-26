# import packages to run
import const
from os import sys

print(const.projectName)

platform = sys.argv[1]

# platforms:
#   mac-test - MacBook Air Test
#   ras-pi - Raspberry Pi Master

if platform == "mac-test":
    # from testing import navSimulation
    from testing import sidewalkTracking

    # navSimulation.run('4986 Weathervane Drive, Johns Creek, GA', '11585 Jones Bridge Rd Ste 500, Johns Creek, GA')
    sidewalkTracking.run('testing/test.mp4')

if platform == "win-test":
    # from testing import navSimulation
    from testing import sidewalkTracking

    # navSimulation.run('4986 Weathervane Drive, Johns Creek, GA', '11585 Jones Bridge Rd Ste 500, Johns Creek, GA')
    sidewalkTracking.run('testing/test1.mp4')

elif platform == "ras-pi":
    from run.raspberrypi import raspberryMaster
    raspberryMaster.startDrive()

else:
    print("platforms: \n    mac-test - MacBook Air Test\n    ras-pi - Raspberry Pi Master\n    win-test - Windows PC Test")
