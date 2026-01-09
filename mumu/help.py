import os.path
import threading
import time

import keyboard

from mumu.mumu import Mumu
from task import m, LocateIconTask, set_vm_index, start_handle_frame

screen_width = 896
screen_height = 1600


def click_pos(x, y):
    m().adb.click(x, y)


def click_screen_center():
    click_pos(screen_width / 2, screen_height / 2)


def locate_icon(name: str, timeout=None):
    fullpath = os.path.join(r'D:\mumu-auto\crop', f'{name}.png')
    task = LocateIconTask(fullpath)
    task.wait(timeout=timeout)
    return task.loc


def click_icon(name: str, timeout=None):
    loc = locate_icon(name, timeout)
    if loc:
        x, y = loc
        click_pos(x, y)
    return loc


set_vm_index(2)
start_handle_frame()


while True:
    click_icon('help')
    time.sleep(3)

