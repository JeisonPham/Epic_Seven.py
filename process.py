import pandas as pd
import screen_grab
import win32api
import win32con
import time

test = screen_grab.screen_grab('char/dom')


def leftDown():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)


def leftUp():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def mousePos(x, y):
    win32api.SetCursorPos((x, y))


def get_coords():
    x, y = win32api.GetCursorPos()
    return x, y


def hold(x, y):
    x = int(x)
    y = int(y)
    mousePos(x, y)
    leftDown()
    time.sleep(1)
    leftUp()


def click(x, y):
    hold(x, y)
    leftUp()


def filter_fn(row):
    if (row['Type'] == 'skip' or row['Type'] == 'tutorial') and (row['Y'] > 100 or row["X"] < 1000):
        return False
    if row['Type'] == 'monster' and row['X'] < 1000:
        return False
    if row['Type'] == 'zeaon' and row['Y'] < 700:
        return False
    return True


while True:
    try:
        points = test.monster_detect()
        m = points.apply(filter_fn, axis=1)
        points = points[m]
        if points.empty:
            hold(1571, 708)
            continue

        print(points)
        value = points.iloc[0]
        value = value.values
        if value[2] == 'go':
            hold(value[0], value[1])

        else:
            click(value[0], value[1])
            print(get_coords())
            time.sleep(.1)
    except:
        hold(1571, 708)
        print('error')
