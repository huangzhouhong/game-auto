import os.path
import queue
import threading

from datetime import datetime
from mumu.mumu import Mumu


class Task:
    def __init__(self):
        self.done = threading.Event()
        self.abandon = False
        self.device: Device = None

    def to(self, device):
        self.device = device

    def run(self, frame, mumu) -> bool:
        pass

    def wait(self, timeout=None):
        self.device.task_queue.put(self)
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
        self.loc = self.device.mumu().auto.locateCenterOnScreen(frame, self.icon_path)
        print(f'locate {self.icon_path} result:{self.loc}')
        return self.loc


class Device:
    def __init__(self, vm_index):
        self.vm_index = vm_index
        self.task_queue = queue.Queue()
        self.current_task = None
        # 开始处理帧
        self.mumu().auto.create_handle(self.handle)
        print(f'mumu {self.vm_index} handler ready')

    def mumu(self):
        return Mumu().select(self.vm_index)

    def handle(self, frame, mumu):
        # print('frame')
        if self.current_task:
            task = self.current_task
        else:
            try:
                task = self.task_queue.get_nowait()
            except queue.Empty:
                # 队列为空
                return

        if task.abandon:
            print('abandon task')
            self.current_task = None
        elif task.run(frame, mumu):
            task.done.set()
            self.current_task = None
        else:
            self.current_task = task
