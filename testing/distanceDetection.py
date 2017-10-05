# import the necessary packages
import numpy as np
import argparse
import glob
import cv2
import imutils
from matplotlib import pyplot as plt

cameraL = cv2.VideoCapture(1)
cameraR = cv2.VideoCapture(2)

print(cameraL.get(3))
print(cameraL.get(4))
print(cameraR.get(3))
print(cameraR.get(4))

while True:
    (grabbedL, camL) = cameraL.read()
    (grabbedR, camR) = cameraR.read()

    # camL = imutils.resize(camL, width=1280, height=960)
    # camR = imutils.resize(camR, width=1280, height=960)

    imgL = cv2.cvtColor(camL, cv2.COLOR_BGR2GRAY)
    # camR = camR[120:840, 0:1280]
    imgR = cv2.cvtColor(camR, cv2.COLOR_BGR2GRAY)
    #
    # height, width = imgL.shape[:2]
    # print(width)
    # print(height)
    # height, width = imgR.shape[:2]
    # print(width)
    # print(height)

    stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
    disparity = stereo.compute(imgL,imgR)
    plt.imshow(disparity,'gray')
    plt.show()

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
