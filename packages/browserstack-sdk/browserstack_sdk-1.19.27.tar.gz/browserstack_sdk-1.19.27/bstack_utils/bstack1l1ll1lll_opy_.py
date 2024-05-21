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
from browserstack_sdk.bstack1llll1111l_opy_ import bstack11l1l1ll_opy_
from browserstack_sdk.bstack11llll111l_opy_ import RobotHandler
def bstack1llll11l1l_opy_(framework):
    if framework.lower() == bstack11ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᆃ"):
        return bstack11l1l1ll_opy_.version()
    elif framework.lower() == bstack11ll_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪᆄ"):
        return RobotHandler.version()
    elif framework.lower() == bstack11ll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬᆅ"):
        import behave
        return behave.__version__
    else:
        return bstack11ll_opy_ (u"࠭ࡵ࡯࡭ࡱࡳࡼࡴࠧᆆ")