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
class bstack1ll111l1l_opy_:
    def __init__(self, handler):
        self._1llll1ll1ll_opy_ = None
        self.handler = handler
        self._1llll1lll11_opy_ = self.bstack1llll1ll1l1_opy_()
        self.patch()
    def patch(self):
        self._1llll1ll1ll_opy_ = self._1llll1lll11_opy_.execute
        self._1llll1lll11_opy_.execute = self.bstack1llll1ll11l_opy_()
    def bstack1llll1ll11l_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack11ll_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࠧᒀ"), driver_command, None, this, args)
            response = self._1llll1ll1ll_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack11ll_opy_ (u"ࠨࡡࡧࡶࡨࡶࠧᒁ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1llll1lll11_opy_.execute = self._1llll1ll1ll_opy_
    @staticmethod
    def bstack1llll1ll1l1_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver