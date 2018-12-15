# import the necessary packages
import numpy as np
import imutils
import cv2
import tkinter as tk

def grayscale(img):
    """Applies the Grayscale transform
    This will return an image with only one color channel
    but NOTE: to see the returned image as grayscale
    (assuming your grayscaled image is called 'gray')
    you should call plt.imshow(gray, cmap='gray')"""
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Or use BGR2GRAY if you read an image with cv2.imread()
    # return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def canny(img, low_threshold, high_threshold):
    """Applies the Canny transform"""
    return cv2.Canny(img, low_threshold, high_threshold)

def gaussian_blur(img, kernel_size):
    """Applies a Gaussian Noise kernel"""
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def region_of_interest(img, vertices):
    """
    Applies an image mask.
    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    """
    #defining a blank mask to start with
    mask = np.zeros_like(img)

    #defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255

    #filling pixels inside the polygon defined by "vertices" with the fill color
    cv2.fillPoly(mask, vertices, ignore_mask_color)

    #returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

def draw_lines(img, lines, color=[255, 0, 0], thickness=2):
    """
    NOTE: this is the function you might want to use as a starting point once you want to
    average/extrapolate the line segments you detect to map out the full
    extent of the lane (going from the result shown in raw-lines-example.mp4
    to that shown in P1_example.mp4).
    Think about things like separating line segments by their
    slope ((y2-y1)/(x2-x1)) to decide which segments are part of the left
    line vs. the right line.  Then, you can average the position of each of
    the lines and extrapolate to the top and bottom of the lane.
    This function draws `lines` with `color` and `thickness`.
    Lines are drawn on the image inplace (mutates the image).
    If you want to make the lines semi-transparent, think about combining
    this function with the weighted_img() function below
    """
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)

def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    """
    `img` should be the output of a Canny transform.
    Returns an image with hough lines drawn.
    """
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_lines(line_img, lines)
    return line_img

# Python 3 has support for cool math symbols.

def weighted_img(img, initial_img, α=0.8, β=1., λ=0.):
    """
    `img` is the output of the hough_lines(), An image with lines drawn on it.
    Should be a blank image (all black) with lines drawn on it.
    `initial_img` should be the image before any processing.
    The result image is computed as follows:
    initial_img * α + img * β + λ
    NOTE: initial_img and img must be the same shape!
    """
    return cv2.addWeighted(initial_img, α, img, β, λ)

def callback(x):
    pass

def run(capture_port):
    camera = cv2.VideoCapture(capture_port)
    cv2.namedWindow('image')

    ilowH = 0
    ihighH = 189

    ilowS = 0
    ihighS = 118

    ilowV = 27
    ihighV = 255

    # create trackbars for color change
    cv2.createTrackbar('lowH','image',ilowH,255,callback)
    cv2.createTrackbar('highH','image',ihighH,255,callback)

    cv2.createTrackbar('lowS','image',ilowS,255,callback)
    cv2.createTrackbar('highS','image',ihighS,255,callback)

    cv2.createTrackbar('lowV','image',ilowV,255,callback)
    cv2.createTrackbar('highV','image',ihighV,255,callback)

    frame_counter = 0

    while True:
        (grabbed, cam) = camera.read()

        frame_counter += 1
        #If the last frame is reached, reset the capture and the frame_counter
        # print(cv2.CV_CAP_)
        if frame_counter == camera.get(cv2.CAP_PROP_FRAME_COUNT):
            frame_counter = 0 #Or whatever as long as it is the same as next line
            camera.set(cv2.CAP_PROP_POS_FRAMES, 0)

        try:
            cam = imutils.resize(cam, width=1080)

            hsv = cv2.cvtColor(cam,cv2.COLOR_BGR2HSV)

            ilowH = cv2.getTrackbarPos('lowH', 'image')
            ihighH = cv2.getTrackbarPos('highH', 'image')
            ilowS = cv2.getTrackbarPos('lowS', 'image')
            ihighS = cv2.getTrackbarPos('highS', 'image')
            ilowV = cv2.getTrackbarPos('lowV', 'image')
            ihighV = cv2.getTrackbarPos('highV', 'image')

            lower_gray = np.array([ilowH, ilowS, ilowV])
            upper_gray = np.array([ihighH, ihighS, ihighV])

            mask = cv2.inRange(hsv, lower_gray, upper_gray)
            res = cv2.bitwise_and(cam, cam, mask=mask)

            # gray_image = cv2.cvtColor(mask, cv2.COLOR_HSV2GRAY)

            kernel_size = 7
            gauss_gray = gaussian_blur(mask, kernel_size)

            low_threshold = 0
            high_threshold = 5
            canny_edges = canny(gauss_gray, low_threshold, high_threshold)
            
            rho = 2
            theta = np.pi/180
            #threshold is minimum number of intersections in a grid for candidate line to go to output
            threshold = 20
            min_line_len = 50
            max_line_gap = 200

            line_image = hough_lines(canny_edges, rho, theta, threshold, min_line_len, max_line_gap)

            result = weighted_img(line_image, cam, α=0.8, β=1., λ=0.)

            print(ilowH)
            print(ilowS)
            print(ilowV)
            print(ihighH)
            print(ihighS)
            print(ihighV)

            cv2.imshow("Original", cam)
            cv2.imshow("Mask", mask)
            cv2.imshow("Results", result)
            cv2.imshow("Canny", canny_edges)
        except:
            continue
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    camera.release()
    cv2.destroyAllWindows()

    
            # imshape = cam.shape
            # lower_left = [0, imshape[0]]
            # lower_right = [imshape[1], imshape[0]]
            # top_left = [imshape[1]/2-imshape[1]/8, imshape[0]/2+imshape[0]/10]
            # top_right = [imshape[1]/2+imshape[1]/8, imshape[0]/2+imshape[0]/10]
            # vertices = [np.array([lower_left, top_left, top_right, lower_right], dtype=np.int32)]
            # roi_image = region_of_interest(canny_edges, vertices)

            #rho and theta are the distance and angular resolution of the grid in Hough space
            #same values as quiz