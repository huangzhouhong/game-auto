import os.path
import threading
import time

import keyboard

from mumu.mumu import Mumu
from task import LocateIconTask, Device, ClickIconTask

screen_width = 896
screen_height = 1600


def click_pos(device: Device, x, y):
    device.mumu().adb.click(x, y)


def click_screen_center():
    click_pos(screen_width / 2, screen_height / 2)


def locate_icon(device: Device, name: str, timeout=None):
    fullpath = os.path.join(r'D:\mumu-auto\crop', f'{name}.png')
    task = LocateIconTask(fullpath)
    task.to(device)
    task.wait(timeout=timeout)
    return task.loc


def click_icon(device: Device, name: str, timeout=None):
    loc = locate_icon(device, name, timeout)
    if loc:
        x, y = loc
        click_pos(device, x, y)
    return loc


def worker(vm_index):
    print(f'worker for {vm_index}')
    device = Device(i)
    while True:
        click_icon(device, 'help')
        time.sleep(3)

def get_icon_path(name:str):
    return os.path.join(r'D:\mumu-auto\crop', f'{name}.png')


if __name__ == '__main__':
    # 1-4
    # for i in range(1, 5):
    #     t = threading.Thread(target=worker, args=(i,))
    #     t.start()
    #     time.sleep(3)
    device = Device(None) # None表示所有设置，参考select逻辑
    task = ClickIconTask(get_icon_path('help'), True)
    device.execute_task(task)
