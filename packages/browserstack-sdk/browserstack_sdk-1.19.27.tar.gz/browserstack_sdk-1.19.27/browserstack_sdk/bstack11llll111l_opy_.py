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
import os
class RobotHandler():
    def __init__(self, args, logger, bstack11lll11111_opy_, bstack11ll1lllll_opy_):
        self.args = args
        self.logger = logger
        self.bstack11lll11111_opy_ = bstack11lll11111_opy_
        self.bstack11ll1lllll_opy_ = bstack11ll1lllll_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack11lll1l111_opy_(bstack11ll1l11l1_opy_):
        bstack11ll1l11ll_opy_ = []
        if bstack11ll1l11l1_opy_:
            tokens = str(os.path.basename(bstack11ll1l11l1_opy_)).split(bstack11ll_opy_ (u"ࠨ࡟ࠣะ"))
            camelcase_name = bstack11ll_opy_ (u"ࠢࠡࠤั").join(t.title() for t in tokens)
            suite_name, bstack11ll1l111l_opy_ = os.path.splitext(camelcase_name)
            bstack11ll1l11ll_opy_.append(suite_name)
        return bstack11ll1l11ll_opy_
    @staticmethod
    def bstack11ll1l1l11_opy_(typename):
        if bstack11ll_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦา") in typename:
            return bstack11ll_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥำ")
        return bstack11ll_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦิ")