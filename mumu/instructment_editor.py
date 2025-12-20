import subprocess

import keyboard

from task import SaveTask


def screenshot():
    task = SaveTask()
    task.wait(timeout=3)
    if not task.path:
        print('wait screenshot timeout')
    else:
        print([r"C:\Program Files (x86)\Adobe\Adobe Photoshop CS5\Photoshop.exe",task.path])
        subprocess.run([r"C:\Program Files (x86)\Adobe\Adobe Photoshop CS5\Photoshop.exe",task.path])
    return task.path


def on_f1():
    print("F1 pressed")
    print(screenshot())


def on_f2():
    print("F2 pressed")


keyboard.add_hotkey('f1', on_f1)  # 数字为'1',numpad数字为'num 0'
keyboard.add_hotkey('f2', on_f2)

print("Listening hotkeys... (press ESC to exit)")
keyboard.wait('esc')
