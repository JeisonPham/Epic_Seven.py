import cv2
from PIL import ImageGrab
import numpy as np
import win32gui

method = cv2.TM_CCOEFF_NORMED
"""
Finds the window called char/dom and gets the dimensions
Does some calculations to get the center/kind of irrevant since it only works on fullscreen 1920x1080
"""

hwnd = win32gui.FindWindow(None, "char/dom")
left, top, right, bottom = win32gui.GetWindowRect(hwnd)
w = int((right - left)/2)
h = int((bottom - top)/4)
bbox = (left + w, top + h, right, bottom - h)


# Read the images from the file
small_image = cv2.imread('three.png')
w, h = small_image.shape[:-1]

while True:
    img = ImageGrab.grab(bbox)
    img = np.array(img)
    large_image = img[:, :, ::-1].copy()
    result = cv2.matchTemplate(small_image, large_image, method)

    threshold = 0.68
    loc = np.where(result >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(large_image, pt,
                      (pt[0] + w, pt[1] + h), (0, 255, 255), 2)
    cv2.imshow('output', large_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
