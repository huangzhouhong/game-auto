import os.path
import queue
import threading

from datetime import datetime
from mumu.mumu import Mumu

vm_index = 0


def set_vm_index(idx):
    global vm_index
    vm_index = idx


def m():
    return Mumu().select(vm_index)


class Task:
    def __init__(self):
        self.done = threading.Event()
        self.abandon = False

    def run(self, frame, mumu) -> bool:
        pass

    def wait(self, timeout=None):
        task_queue.put(self)
        self.abandon = not self.done.wait(timeout=timeout)


class SaveTask(Task):
    def __init__(self):
        super().__init__()
        self.path = ''

    def run(self, frame, mumu) -> bool:
        filename = datetime.now().strftime("%Y%m%d_%H%M%S.png")
        fullname = os.path.join(r'd:\mumu-auto\tmp', filename)
        mumu.auto.save(frame, fullname)
        self.path = fullname
        return True


class LocateIconTask(Task):
    def __init__(self, icon_path):
        super().__init__()
        self.loc = None
        self.icon_path = icon_path

    def run(self, frame, mumu) -> bool:
        self.loc = m().auto.locateCenterOnScreen(frame, self.icon_path)
        print(f'locate {self.icon_path} result:{self.loc}')
        return self.loc


task_queue = queue.Queue()
current_task: Task = None


def handle(frame, mumu):
    print(mumu)
    global current_task
    if current_task:
        task = current_task
    else:
        try:
            task = task_queue.get_nowait()
        except queue.Empty:
            # 队列为空
            return

    if task.abandon:
        print('abandon task')
        current_task = None
    elif task.run(frame, mumu):
        task.done.set()
        current_task = None
    else:
        current_task = task


def start_handle_frame():
    m().auto.create_handle(handle)
    print('mumu handler ready')
