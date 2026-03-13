import os.path
import queue
import threading
import time
from collections import defaultdict

from datetime import datetime
from mumu.mumu import Mumu


class Task:
    def __init__(self):
        self.done = threading.Event()
        self.abandon = False

    def run(self, frame, mumu) -> bool:
        pass


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

    def run(self, frame, mumu: Mumu) -> bool:
        self.loc = mumu.auto.locateCenterOnScreen(frame, self.icon_path)
        print(f'locate {self.icon_path} result:{self.loc}')
        return self.loc


class ClickIconTask(Task):
    def __init__(self, icon_path, infinite: bool = False, pause=2.0):
        super().__init__()
        self.icon_path = icon_path
        self.infinite = infinite
        self.pause = pause
        self.ignore_until_map: dict[int, float] = defaultdict(float)

    def run(self, frame, mumu: Mumu) -> bool:
        vm_id = mumu.core.utils.get_vm_id()
        now = time.monotonic()

        # 点击icon后，后续帧仍可能相同，导致重复点击。通过pause设置忽略帧时间
        # 如果该设备仍在忽略期
        if now < self.ignore_until_map[vm_id]:
            # print('ignore frame')
            return not self.infinite

        loc = mumu.auto.locateCenterOnScreen(frame, self.icon_path)
        # print(f'locate {self.icon_path} result:{loc}')
        if loc:
            x, y = loc
            mumu.adb.click(x, y)
            print(f'click {vm_id} ({x},{y})')
            if self.pause:
                self.ignore_until_map[vm_id] = now + self.pause

        return loc and not self.infinite


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

    def handle(self, frame, mumu: Mumu):
        # print(f'frame')
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

    def execute_task(self, task: Task, timeout=None):
        self.task_queue.put(task)
        task.abandon = not task.done.wait(timeout=timeout)
