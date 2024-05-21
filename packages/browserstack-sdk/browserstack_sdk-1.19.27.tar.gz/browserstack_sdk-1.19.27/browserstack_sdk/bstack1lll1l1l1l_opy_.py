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
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1l1ll11l11_opy_ = {}
        bstack1l11l11ll1_opy_ = os.environ.get(bstack11ll_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭ഞ"), bstack11ll_opy_ (u"࠭ࠧട"))
        if not bstack1l11l11ll1_opy_:
            return bstack1l1ll11l11_opy_
        try:
            bstack1l11l11l1l_opy_ = json.loads(bstack1l11l11ll1_opy_)
            if bstack11ll_opy_ (u"ࠢࡰࡵࠥഠ") in bstack1l11l11l1l_opy_:
                bstack1l1ll11l11_opy_[bstack11ll_opy_ (u"ࠣࡱࡶࠦഡ")] = bstack1l11l11l1l_opy_[bstack11ll_opy_ (u"ࠤࡲࡷࠧഢ")]
            if bstack11ll_opy_ (u"ࠥࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠢണ") in bstack1l11l11l1l_opy_ or bstack11ll_opy_ (u"ࠦࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠢത") in bstack1l11l11l1l_opy_:
                bstack1l1ll11l11_opy_[bstack11ll_opy_ (u"ࠧࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠣഥ")] = bstack1l11l11l1l_opy_.get(bstack11ll_opy_ (u"ࠨ࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠥദ"), bstack1l11l11l1l_opy_.get(bstack11ll_opy_ (u"ࠢࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠥധ")))
            if bstack11ll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࠤന") in bstack1l11l11l1l_opy_ or bstack11ll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢഩ") in bstack1l11l11l1l_opy_:
                bstack1l1ll11l11_opy_[bstack11ll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠣപ")] = bstack1l11l11l1l_opy_.get(bstack11ll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࠧഫ"), bstack1l11l11l1l_opy_.get(bstack11ll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠥബ")))
            if bstack11ll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣഭ") in bstack1l11l11l1l_opy_ or bstack11ll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠣമ") in bstack1l11l11l1l_opy_:
                bstack1l1ll11l11_opy_[bstack11ll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠤയ")] = bstack1l11l11l1l_opy_.get(bstack11ll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠦര"), bstack1l11l11l1l_opy_.get(bstack11ll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠦറ")))
            if bstack11ll_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࠦല") in bstack1l11l11l1l_opy_ or bstack11ll_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠤള") in bstack1l11l11l1l_opy_:
                bstack1l1ll11l11_opy_[bstack11ll_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠥഴ")] = bstack1l11l11l1l_opy_.get(bstack11ll_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࠢവ"), bstack1l11l11l1l_opy_.get(bstack11ll_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠧശ")))
            if bstack11ll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦഷ") in bstack1l11l11l1l_opy_ or bstack11ll_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤസ") in bstack1l11l11l1l_opy_:
                bstack1l1ll11l11_opy_[bstack11ll_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥഹ")] = bstack1l11l11l1l_opy_.get(bstack11ll_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࠢഺ"), bstack1l11l11l1l_opy_.get(bstack11ll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩ഻ࠧ")))
            if bstack11ll_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡹࡩࡷࡹࡩࡰࡰ഼ࠥ") in bstack1l11l11l1l_opy_ or bstack11ll_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥഽ") in bstack1l11l11l1l_opy_:
                bstack1l1ll11l11_opy_[bstack11ll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦാ")] = bstack1l11l11l1l_opy_.get(bstack11ll_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡤࡼࡥࡳࡵ࡬ࡳࡳࠨി"), bstack1l11l11l1l_opy_.get(bstack11ll_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨീ")))
            if bstack11ll_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠢു") in bstack1l11l11l1l_opy_:
                bstack1l1ll11l11_opy_[bstack11ll_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠣൂ")] = bstack1l11l11l1l_opy_[bstack11ll_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳࡖࡢࡴ࡬ࡥࡧࡲࡥࡴࠤൃ")]
        except Exception as error:
            logger.error(bstack11ll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡨࡻࡲࡳࡧࡱࡸࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡥࡣࡷࡥ࠿ࠦࠢൄ") +  str(error))
        return bstack1l1ll11l11_opy_