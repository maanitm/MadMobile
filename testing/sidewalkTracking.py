# import the necessary packages
import numpy as np
import cv2
import imutils

def autoCanny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)

    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    # return the edged image
    return edged

def run(capturePort):
    print("Sidewalk Tracking Test")

    camera = cv2.VideoCapture(capturePort)

    while True:
        (grabbed, cam) = camera.read()

        cam = imutils.resize(cam, width=1000)
        # load the image, convert it to grayscale, and blur it slightly
        gray = cv2.cvtColor(cam, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)

        # apply Canny edge detection using a wide threshold, tight
        # threshold, and automatically determined threshold
        wide = cv2.Canny(blurred, 10, 200)
        tight = cv2.Canny(blurred, 225, 250)
        auto = autoCanny(blurred)

        cam = imutils.resize(cam, width=1000)
        frame = np.hstack([auto])
        frame = imutils.resize(frame, width=1000)
        # show the images
        cv2.imshow("Original", cam)
        cv2.imshow("Edges", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()
