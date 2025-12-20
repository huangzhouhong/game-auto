import os.path
import queue
import threading

from datetime import datetime
from mumu.mumu import Mumu


class Task:
    def __init__(self):
        self.done = threading.Event()

    def run(self, frame, mumu) -> bool:
        pass

    def wait(self, timeout=None):
        task_queue.put(self)
        self.done.wait(timeout=timeout)


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


task_queue = queue.Queue()
current_task: Task = None


def handle(frame, mumu):
    global current_task
    if current_task:
        task = current_task
    else:
        try:
            task = task_queue.get_nowait()
        except queue.Empty:
            # 队列为空
            return

    if task.run(frame, mumu):
        task.done.set()
        current_task = None
    else:
        current_task = task


Mumu().select(0).auto.create_handle(handle)
