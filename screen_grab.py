import cv2
from PIL import ImageGrab
import win32gui
import numpy as np
import pandas as pd
import math

method = cv2.TM_CCOEFF_NORMED
"""
Finds the window called char/dom and gets the dimensions
Does some calculations to get the center/kind of irrevant since it only works on fullscreen 1920x1080
"""


def filter(self, large_image, name, small_image, range=(0, 0)):
    x = []
    y = []
    type_img = []
    threshold = 0.67
    result = cv2.matchTemplate(small_image, large_image, method)
    loc = np.where(result >= threshold)
    index = 0
    for pt in zip(*loc[::-1]):
        # cv2.circle(large_image, (pt[0], pt[1]), 10, (0, 0, 255), -1)

        if index >= 1:
            if abs(x[index-1] - pt[0]) <= 10:
                continue
            if abs(y[index-1] - pt[1]) <= 10:
                continue

        x.append(pt[0] + 10)
        y.append(pt[1] + 10)
        type_img.append(name)
        index += 1

    points = pd.DataFrame({"X": x, "Y": y, str("Type"): type_img})
    points.drop_duplicates(subset=['X'], keep="first", inplace=True)
    points.drop_duplicates(subset=['Y'], keep="first", inplace=True)
    return points


class screen_grab():
    def __init__(self, name):
        self.hwnd = win32gui.FindWindow(None, name)
        self.left, self.top, self.right, self.bottom = win32gui.GetWindowRect(
            self.hwnd)
        # self.w = int((self.right - self.left)/2)
        # self.h = int((self.bottom - self.top)/4)
        # self.bbox = (self.left + self.w, self.top + self.h,
        #              self.right, self.bottom - self.h)
        self.image_names = ['go', 'zeaon', 'tutorial', 'skip', 'monster', 'confirm',
                            'adventure', 'ready', 'select_team', 'start_quest']
        self.images = {}
        for name in self.image_names:
            self.images[name] = cv2.imread('images/{}.png'.format(name))

    def monster_detect(self):

        # img = ImageGrab.grab(self.bbox)
        img = ImageGrab.grab()
        img = np.array(img)
        large_image = img[:, :, ::-1].copy()
        points = pd.DataFrame({'X': [], 'Y': [], 'Type': []})

        for name in self.image_names:
            points = pd.concat(
                [points, filter(self, large_image, name, self.images[name])])

        if not points.empty:
            return points
        return None
