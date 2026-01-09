import sys

from mumu.mumu import Mumu


# Mumu(r"C:\Program Files\Netease\MuMu\nx_main\MuMuManager.exe").select(1)
Mumu().select(0).androidEvent.screenshot()


# def handle(frame, mumu):
#     # do something
#     print('接收到模拟器：', mumu.core.utils.get_vm_id(), '的帧',frame.shape)
#     # print(frame)
#     # mumu.auto.save(frame, r'd:\test.png')
#     # sys.exit()
#     pos=Mumu().auto.locateCenterOnScreen(frame,r'd:\fight.png')
#     if pos:
#         print('找到图片中心点：', pos)
#     else:
#         print('未找到图片')
#
#
# Mumu().select(0).auto.create_handle(handle)





# print(Mumu().select(0).screen.resolution_mobile())