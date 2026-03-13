import random
import time

from mumu.mumu import Mumu

# 获取vm_index: MuMuManager.exe info -v 6
vm_indexes = [1, 2, 3, 4]  # 6是大号

pos_x = 446
pos_y = 1510

while True:
    for idx in vm_indexes:
        x = pos_x + random.randint(-10, 10)
        y = pos_y + random.randint(-10, 10)

        Mumu().select(idx).adb.click(x, y)

    time.sleep(random.uniform(0.02, 0.03))
