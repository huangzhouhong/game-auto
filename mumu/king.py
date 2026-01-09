import os.path
import threading
import time

import keyboard

from mumu.mumu import Mumu
from task import m, LocateIconTask

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


cancel = True


def cure():
    if not locate_icon('showing_cure', timeout=1):
        # 右下角打开治疗界面
        if not click_icon('need_cure', timeout=3):
            click_icon('need_help')
            click_icon('need_cure')

    while not cancel:
        click_icon('cure', timeout=2)
        click_icon('help_me', timeout=2)
d

def fight(queue_x, queue_y):
    global cancel
    cancel = True

    time.sleep(5)
    click_icon('quit_cure', timeout=1)
    time.sleep(1)
    click_screen_center()
    click_icon("red-fight")
    click_pos(queue_x, queue_y)
    click_icon("blue-fight")


def on_f1():
    global cancel
    if not cancel:
        print('repeat run, ignore')
        return
    cancel = False
    print("start cure")

    # cure()
    t = threading.Thread(target=cure)
    t.start()

    print("stop cure")


def on_f2():
    print("F2(cancel) pressed")
    global cancel
    cancel = True


# test screen center
def on_f3():
    click_screen_center()

def on_f4():
    fight(85, 160)

def on_1():
    fight(85, 160)


def on_2():
    fight(174, 151)


keyboard.add_hotkey('f1', on_f1)
keyboard.add_hotkey('f2', on_f2)
keyboard.add_hotkey('f3', on_f3)
keyboard.add_hotkey('f4', on_f4)
# keyboard.add_hotkey('1', on_1)  # 数字为'1',numpad数字为'num 0'
# keyboard.add_hotkey('2', on_2)

print("Listening hotkeys... (press ESC to exit)")
keyboard.wait('esc')
