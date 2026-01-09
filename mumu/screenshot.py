import sys

from mumu.mumu import Mumu


def handle(frame, mumu):
    mumu.auto.save(frame, r'd:\test.png')
    sys.exit(0)

Mumu().select(0).auto.create_handle(handle)