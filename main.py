import cv2 as cv
import numpy as np
import time

cap = cv.VideoCapture(0)

# Warming-up of camera
time.sleep(3)
background = 0

for i in range(30):
    ret, background = cap.read()

# Lateral inversion of image
background = np.flip(background, axis=1)

while (cap.isOpened()):
    # Capture live frame
    ret, img = cap.read()

    # Flipping the image
    img = np.flip(img, axis=1)

    # Convert the image to HSV color space
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    blurred = cv.GaussianBlur(hsv, (35, 35), 0)

    # Defining the lower range for red color detection
    lower = np.array([0, 120, 70])
    upper = np.array(([10, 255, 255]))
    mask1 = cv.inRange(hsv, lower, upper)

    # Defining the upper range for red color detection
    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])
    mask2 = cv.inRange(hsv, lower_red, upper_red)

    # Generating the final mask to detect red color
    mask = mask1 + mask2
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, np.ones((5, 5), np.uint8))

    # Replacing pixels corresponding to cloak with the background pixels.
    img[np.where(mask == 255)] = background[np.where(mask == 255)]
    cv.imshow('Display', img)
    k = cv.waitKey(10)
    if k == 27:
        break