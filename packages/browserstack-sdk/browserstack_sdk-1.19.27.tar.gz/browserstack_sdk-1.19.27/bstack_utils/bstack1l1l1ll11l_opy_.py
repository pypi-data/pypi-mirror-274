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
from collections import deque
from bstack_utils.constants import *
class bstack11l1ll11_opy_:
    def __init__(self):
        self._1111111111_opy_ = deque()
        self._1llllllllll_opy_ = {}
        self._111111l11l_opy_ = False
    def bstack111111ll11_opy_(self, test_name, bstack111111111l_opy_):
        bstack11111111ll_opy_ = self._1llllllllll_opy_.get(test_name, {})
        return bstack11111111ll_opy_.get(bstack111111111l_opy_, 0)
    def bstack111111l111_opy_(self, test_name, bstack111111111l_opy_):
        bstack1lllllllll1_opy_ = self.bstack111111ll11_opy_(test_name, bstack111111111l_opy_)
        self.bstack1111111lll_opy_(test_name, bstack111111111l_opy_)
        return bstack1lllllllll1_opy_
    def bstack1111111lll_opy_(self, test_name, bstack111111111l_opy_):
        if test_name not in self._1llllllllll_opy_:
            self._1llllllllll_opy_[test_name] = {}
        bstack11111111ll_opy_ = self._1llllllllll_opy_[test_name]
        bstack1lllllllll1_opy_ = bstack11111111ll_opy_.get(bstack111111111l_opy_, 0)
        bstack11111111ll_opy_[bstack111111111l_opy_] = bstack1lllllllll1_opy_ + 1
    def bstack1ll11111l1_opy_(self, bstack1111111l1l_opy_, bstack111111l1ll_opy_):
        bstack111111l1l1_opy_ = self.bstack111111l111_opy_(bstack1111111l1l_opy_, bstack111111l1ll_opy_)
        bstack1111111ll1_opy_ = bstack11l11llll1_opy_[bstack111111l1ll_opy_]
        bstack11111111l1_opy_ = bstack11ll_opy_ (u"ࠢࡼࡿ࠰ࡿࢂ࠳ࡻࡾࠤᐧ").format(bstack1111111l1l_opy_, bstack1111111ll1_opy_, bstack111111l1l1_opy_)
        self._1111111111_opy_.append(bstack11111111l1_opy_)
    def bstack1llll11l1_opy_(self):
        return len(self._1111111111_opy_) == 0
    def bstack1l1l111ll1_opy_(self):
        bstack1111111l11_opy_ = self._1111111111_opy_.popleft()
        return bstack1111111l11_opy_
    def capturing(self):
        return self._111111l11l_opy_
    def bstack1ll11ll11l_opy_(self):
        self._111111l11l_opy_ = True
    def bstack1ll11lll11_opy_(self):
        self._111111l11l_opy_ = False