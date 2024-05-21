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
import sys
class bstack1l1111l11l_opy_:
    def __init__(self, handler):
        self._11l1l1ll11_opy_ = sys.stdout.write
        self._11l1l1ll1l_opy_ = sys.stderr.write
        self.handler = handler
        self._started = False
    def start(self):
        if self._started:
            return
        self._started = True
        sys.stdout.write = self.bstack11l1l1l1ll_opy_
        sys.stdout.error = self.bstack11l1l1lll1_opy_
    def bstack11l1l1l1ll_opy_(self, _str):
        self._11l1l1ll11_opy_(_str)
        if self.handler:
            self.handler({bstack11ll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ໩"): bstack11ll_opy_ (u"ࠪࡍࡓࡌࡏࠨ໪"), bstack11ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ໫"): _str})
    def bstack11l1l1lll1_opy_(self, _str):
        self._11l1l1ll1l_opy_(_str)
        if self.handler:
            self.handler({bstack11ll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ໬"): bstack11ll_opy_ (u"࠭ࡅࡓࡔࡒࡖࠬ໭"), bstack11ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ໮"): _str})
    def reset(self):
        if not self._started:
            return
        self._started = False
        sys.stdout.write = self._11l1l1ll11_opy_
        sys.stderr.write = self._11l1l1ll1l_opy_