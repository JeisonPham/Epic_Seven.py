import win32api
import time

features = ['Skip', 'Heal', 'Tap to start', 'Go']
skip = (1827, 57)
go = (1571, 708)
confirm_1 = (1645, 974)
confirm_2 = (1329, 966)

prologue = []

x = 0
while True:
    x += 1
    print(x)
    time.sleep(1)
