# coding: UTF-8
import sys
bstack111l11_opy_ = sys.version_info [0] == 2
bstack111_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack11ll_opy_ (bstack11ll1_opy_):
    global bstack1ll1111_opy_
    bstack1111111_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack111l1l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack111l1l_opy_ = bstack1111111_opy_ % len (bstack111l1l1_opy_)
    bstack111111_opy_ = bstack111l1l1_opy_ [:bstack111l1l_opy_] + bstack111l1l1_opy_ [bstack111l1l_opy_:]
    if bstack111l11_opy_:
        bstack1lll1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111_opy_ - (bstack1l1l_opy_ + bstack1111111_opy_) % bstack1111lll_opy_) for bstack1l1l_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll1ll_opy_ = str () .join ([chr (ord (char) - bstack111_opy_ - (bstack1l1l_opy_ + bstack1111111_opy_) % bstack1111lll_opy_) for bstack1l1l_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll1ll_opy_)
import threading
bstack1lllll11l11_opy_ = 1000
bstack1llll1lll1l_opy_ = 5
bstack1lllll11lll_opy_ = 30
bstack1lllll11111_opy_ = 2
class bstack1lllll111ll_opy_:
    def __init__(self, handler, bstack1lllll111l1_opy_=bstack1lllll11l11_opy_, bstack1llll1llll1_opy_=bstack1llll1lll1l_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1lllll111l1_opy_ = bstack1lllll111l1_opy_
        self.bstack1llll1llll1_opy_ = bstack1llll1llll1_opy_
        self.lock = threading.Lock()
        self.timer = None
    def start(self):
        if not self.timer:
            self.bstack1lllll11l1l_opy_()
    def bstack1lllll11l1l_opy_(self):
        self.timer = threading.Timer(self.bstack1llll1llll1_opy_, self.bstack1lllll11ll1_opy_)
        self.timer.start()
    def bstack1llll1lllll_opy_(self):
        self.timer.cancel()
    def bstack1lllll1111l_opy_(self):
        self.bstack1llll1lllll_opy_()
        self.bstack1lllll11l1l_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1lllll111l1_opy_:
                t = threading.Thread(target=self.bstack1lllll11ll1_opy_)
                t.start()
                self.bstack1lllll1111l_opy_()
    def bstack1lllll11ll1_opy_(self):
        if len(self.queue) <= 0:
            return
        data = self.queue[:self.bstack1lllll111l1_opy_]
        del self.queue[:self.bstack1lllll111l1_opy_]
        self.handler(data)
    def shutdown(self):
        self.bstack1llll1lllll_opy_()
        while len(self.queue) > 0:
            self.bstack1lllll11ll1_opy_()