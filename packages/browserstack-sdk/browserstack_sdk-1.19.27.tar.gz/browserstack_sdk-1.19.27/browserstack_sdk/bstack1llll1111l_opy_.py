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
import multiprocessing
import os
import json
from time import sleep
import bstack_utils.bstack11l1111l_opy_ as bstack1l1l11111l_opy_
from browserstack_sdk.bstack1ll1l1l11l_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1l11lll1l_opy_
class bstack11l1l1ll_opy_:
    def __init__(self, args, logger, bstack11lll11111_opy_, bstack11ll1lllll_opy_):
        self.args = args
        self.logger = logger
        self.bstack11lll11111_opy_ = bstack11lll11111_opy_
        self.bstack11ll1lllll_opy_ = bstack11ll1lllll_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1l1l1l111l_opy_ = []
        self.bstack11ll1l1l1l_opy_ = None
        self.bstack11l11l111_opy_ = []
        self.bstack11ll1lll11_opy_ = self.bstack11lll1l1_opy_()
        self.bstack1llll1ll1_opy_ = -1
    def bstack11llll1l1_opy_(self, bstack11lll111ll_opy_):
        self.parse_args()
        self.bstack11ll1llll1_opy_()
        self.bstack11ll1ll111_opy_(bstack11lll111ll_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack11ll1ll1l1_opy_():
        import importlib
        if getattr(importlib, bstack11ll_opy_ (u"ࠪࡪ࡮ࡴࡤࡠ࡮ࡲࡥࡩ࡫ࡲࠨฑ"), False):
            bstack11ll1ll1ll_opy_ = importlib.find_loader(bstack11ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭ฒ"))
        else:
            bstack11ll1ll1ll_opy_ = importlib.util.find_spec(bstack11ll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧณ"))
    def bstack11ll1l1lll_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1llll1ll1_opy_ = -1
        if bstack11ll_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ด") in self.bstack11lll11111_opy_:
            self.bstack1llll1ll1_opy_ = int(self.bstack11lll11111_opy_[bstack11ll_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧต")])
        try:
            bstack11ll1lll1l_opy_ = [bstack11ll_opy_ (u"ࠨ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠪถ"), bstack11ll_opy_ (u"ࠩ࠰࠱ࡵࡲࡵࡨ࡫ࡱࡷࠬท"), bstack11ll_opy_ (u"ࠪ࠱ࡵ࠭ธ")]
            if self.bstack1llll1ll1_opy_ >= 0:
                bstack11ll1lll1l_opy_.extend([bstack11ll_opy_ (u"ࠫ࠲࠳࡮ࡶ࡯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬน"), bstack11ll_opy_ (u"ࠬ࠳࡮ࠨบ")])
            for arg in bstack11ll1lll1l_opy_:
                self.bstack11ll1l1lll_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack11ll1llll1_opy_(self):
        bstack11ll1l1l1l_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack11ll1l1l1l_opy_ = bstack11ll1l1l1l_opy_
        return bstack11ll1l1l1l_opy_
    def bstack1llllll1ll_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack11ll1ll1l1_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1l11lll1l_opy_)
    def bstack11ll1ll111_opy_(self, bstack11lll111ll_opy_):
        bstack11llll1l_opy_ = Config.bstack11l1l11l1_opy_()
        if bstack11lll111ll_opy_:
            self.bstack11ll1l1l1l_opy_.append(bstack11ll_opy_ (u"࠭࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪป"))
            self.bstack11ll1l1l1l_opy_.append(bstack11ll_opy_ (u"ࠧࡕࡴࡸࡩࠬผ"))
        if bstack11llll1l_opy_.bstack11lll1111l_opy_():
            self.bstack11ll1l1l1l_opy_.append(bstack11ll_opy_ (u"ࠨ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧฝ"))
            self.bstack11ll1l1l1l_opy_.append(bstack11ll_opy_ (u"ࠩࡗࡶࡺ࡫ࠧพ"))
        self.bstack11ll1l1l1l_opy_.append(bstack11ll_opy_ (u"ࠪ࠱ࡵ࠭ฟ"))
        self.bstack11ll1l1l1l_opy_.append(bstack11ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡳࡰࡺ࡭ࡩ࡯ࠩภ"))
        self.bstack11ll1l1l1l_opy_.append(bstack11ll_opy_ (u"ࠬ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠧม"))
        self.bstack11ll1l1l1l_opy_.append(bstack11ll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ย"))
        if self.bstack1llll1ll1_opy_ > 1:
            self.bstack11ll1l1l1l_opy_.append(bstack11ll_opy_ (u"ࠧ࠮ࡰࠪร"))
            self.bstack11ll1l1l1l_opy_.append(str(self.bstack1llll1ll1_opy_))
    def bstack11ll1ll11l_opy_(self):
        bstack11l11l111_opy_ = []
        for spec in self.bstack1l1l1l111l_opy_:
            bstack1l1lllll11_opy_ = [spec]
            bstack1l1lllll11_opy_ += self.bstack11ll1l1l1l_opy_
            bstack11l11l111_opy_.append(bstack1l1lllll11_opy_)
        self.bstack11l11l111_opy_ = bstack11l11l111_opy_
        return bstack11l11l111_opy_
    def bstack11lll1l1_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack11ll1lll11_opy_ = True
            return True
        except Exception as e:
            self.bstack11ll1lll11_opy_ = False
        return self.bstack11ll1lll11_opy_
    def bstack1ll1ll11ll_opy_(self, bstack11ll1l1ll1_opy_, bstack11llll1l1_opy_):
        bstack11llll1l1_opy_[bstack11ll_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨฤ")] = self.bstack11lll11111_opy_
        multiprocessing.set_start_method(bstack11ll_opy_ (u"ࠩࡶࡴࡦࡽ࡮ࠨล"))
        if bstack11ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ฦ") in self.bstack11lll11111_opy_:
            bstack11l11ll11_opy_ = []
            manager = multiprocessing.Manager()
            bstack1l1l1111_opy_ = manager.list()
            for index, platform in enumerate(self.bstack11lll11111_opy_[bstack11ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧว")]):
                bstack11l11ll11_opy_.append(multiprocessing.Process(name=str(index),
                                                           target=bstack11ll1l1ll1_opy_,
                                                           args=(self.bstack11ll1l1l1l_opy_, bstack11llll1l1_opy_, bstack1l1l1111_opy_)))
            i = 0
            bstack11lll11l11_opy_ = len(self.bstack11lll11111_opy_[bstack11ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨศ")])
            for t in bstack11l11ll11_opy_:
                os.environ[bstack11ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ษ")] = str(i)
                os.environ[bstack11ll_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨส")] = json.dumps(self.bstack11lll11111_opy_[bstack11ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫห")][i % bstack11lll11l11_opy_])
                i += 1
                t.start()
            for t in bstack11l11ll11_opy_:
                t.join()
            return list(bstack1l1l1111_opy_)
    @staticmethod
    def bstack1l111llll_opy_(driver, bstack1ll1l1ll_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack11ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭ฬ"), None)
        if item and getattr(item, bstack11ll_opy_ (u"ࠪࡣࡦ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡤࡣࡶࡩࠬอ"), None) and not getattr(item, bstack11ll_opy_ (u"ࠫࡤࡧ࠱࠲ࡻࡢࡷࡹࡵࡰࡠࡦࡲࡲࡪ࠭ฮ"), False):
            logger.info(
                bstack11ll_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠣࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡯ࡳࠡࡷࡱࡨࡪࡸࡷࡢࡻ࠱ࠦฯ"))
            bstack11lll111l1_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1l1l11111l_opy_.bstack1lll1ll1_opy_(driver, bstack11lll111l1_opy_, item.name, item.module.__name__, item.path, bstack1ll1l1ll_opy_)
            item._a11y_stop_done = True
            if wait:
                sleep(2)