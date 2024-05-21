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
import datetime
import json
import logging
import os
import threading
from bstack_utils.helper import bstack11l1lll1l1_opy_, bstack1ll1111l11_opy_, get_host_info, bstack11l1ll1ll1_opy_, bstack11ll111111_opy_, bstack111lll1l1l_opy_, \
    bstack11l11ll1ll_opy_, bstack11l11l1ll1_opy_, bstack1l11llll1_opy_, bstack111lll1111_opy_, bstack111llll1_opy_, bstack1l111l1l1l_opy_, bstack11lll1l11_opy_
from bstack_utils.bstack1lllll1l111_opy_ import bstack1lllll111ll_opy_
from bstack_utils.bstack11lll1l1ll_opy_ import bstack1l11111ll1_opy_
import bstack_utils.bstack11l1111l_opy_ as bstack1l1l11111l_opy_
from bstack_utils.constants import bstack11l1l1111l_opy_
bstack1llll11111l_opy_ = [
    bstack11ll_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ᓴ"), bstack11ll_opy_ (u"ࠪࡇࡇ࡚ࡓࡦࡵࡶ࡭ࡴࡴࡃࡳࡧࡤࡸࡪࡪࠧᓵ"), bstack11ll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᓶ"), bstack11ll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭ᓷ"),
    bstack11ll_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᓸ"), bstack11ll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᓹ"), bstack11ll_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᓺ")
]
bstack1lll1llllll_opy_ = bstack11ll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡧࡴࡲ࡬ࡦࡥࡷࡳࡷ࠳࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩᓻ")
logger = logging.getLogger(__name__)
class bstack1l1ll111l1_opy_:
    bstack1lllll1l111_opy_ = None
    bs_config = None
    @classmethod
    @bstack1l111l1l1l_opy_(class_method=True)
    def launch(cls, bs_config, bstack1lll1ll1111_opy_):
        cls.bs_config = bs_config
        cls.bstack1lll1llll1l_opy_()
        bstack11ll11l11l_opy_ = bstack11l1ll1ll1_opy_(bs_config)
        bstack11ll1111l1_opy_ = bstack11ll111111_opy_(bs_config)
        bstack1l11llll_opy_ = False
        bstack1l11lll1_opy_ = False
        if bstack11ll_opy_ (u"ࠪࡥࡵࡶࠧᓼ") in bs_config:
            bstack1l11llll_opy_ = True
        else:
            bstack1l11lll1_opy_ = True
        bstack1lll1l11ll_opy_ = {
            bstack11ll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᓽ"): cls.bstack1l11lll111_opy_(bstack1lll1ll1111_opy_.get(bstack11ll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡷࡶࡩࡩ࠭ᓾ"), bstack11ll_opy_ (u"࠭ࠧᓿ"))),
            bstack11ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᔀ"): bstack1l1l11111l_opy_.bstack11111ll11_opy_(bs_config),
            bstack11ll_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧᔁ"): bs_config.get(bstack11ll_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨᔂ"), False),
            bstack11ll_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬᔃ"): bstack1l11lll1_opy_,
            bstack11ll_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪᔄ"): bstack1l11llll_opy_
        }
        data = {
            bstack11ll_opy_ (u"ࠬ࡬࡯ࡳ࡯ࡤࡸࠬᔅ"): bstack11ll_opy_ (u"࠭ࡪࡴࡱࡱࠫᔆ"),
            bstack11ll_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡠࡰࡤࡱࡪ࠭ᔇ"): bs_config.get(bstack11ll_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ᔈ"), bstack11ll_opy_ (u"ࠩࠪᔉ")),
            bstack11ll_opy_ (u"ࠪࡲࡦࡳࡥࠨᔊ"): bs_config.get(bstack11ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧᔋ"), os.path.basename(os.path.abspath(os.getcwd()))),
            bstack11ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᔌ"): bs_config.get(bstack11ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᔍ")),
            bstack11ll_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᔎ"): bs_config.get(bstack11ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫᔏ"), bstack11ll_opy_ (u"ࠩࠪᔐ")),
            bstack11ll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡡࡷ࡭ࡲ࡫ࠧᔑ"): datetime.datetime.now().isoformat(),
            bstack11ll_opy_ (u"ࠫࡹࡧࡧࡴࠩᔒ"): bstack111lll1l1l_opy_(bs_config),
            bstack11ll_opy_ (u"ࠬ࡮࡯ࡴࡶࡢ࡭ࡳ࡬࡯ࠨᔓ"): get_host_info(),
            bstack11ll_opy_ (u"࠭ࡣࡪࡡ࡬ࡲ࡫ࡵࠧᔔ"): bstack1ll1111l11_opy_(),
            bstack11ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡲࡶࡰࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᔕ"): os.environ.get(bstack11ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧᔖ")),
            bstack11ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࡠࡴࡨࡶࡺࡴࠧᔗ"): os.environ.get(bstack11ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠨᔘ"), False),
            bstack11ll_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࡤࡩ࡯࡯ࡶࡵࡳࡱ࠭ᔙ"): bstack11l1lll1l1_opy_(),
            bstack11ll_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹࡥ࡭ࡢࡲࠪᔚ"): bstack1lll1l11ll_opy_,
            bstack11ll_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᔛ"): {
                bstack11ll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡑࡥࡲ࡫ࠧᔜ"): bstack1lll1ll1111_opy_.get(bstack11ll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࠩᔝ"), bstack11ll_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩᔞ")),
                bstack11ll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᔟ"): bstack1lll1ll1111_opy_.get(bstack11ll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᔠ")),
                bstack11ll_opy_ (u"ࠬࡹࡤ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩᔡ"): bstack1lll1ll1111_opy_.get(bstack11ll_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫᔢ"))
            }
        }
        config = {
            bstack11ll_opy_ (u"ࠧࡢࡷࡷ࡬ࠬᔣ"): (bstack11ll11l11l_opy_, bstack11ll1111l1_opy_),
            bstack11ll_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩᔤ"): cls.default_headers()
        }
        response = bstack1l11llll1_opy_(bstack11ll_opy_ (u"ࠩࡓࡓࡘ࡚ࠧᔥ"), cls.request_url(bstack11ll_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡺ࡯࡬ࡥࡵࠪᔦ")), data, config)
        if response.status_code != 200:
            os.environ[bstack11ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᔧ")] = bstack11ll_opy_ (u"ࠬࡴࡵ࡭࡮ࠪᔨ")
            os.environ[bstack11ll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡆࡓࡒࡖࡌࡆࡖࡈࡈࠬᔩ")] = bstack11ll_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ᔪ")
            os.environ[bstack11ll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠩᔫ")] = bstack11ll_opy_ (u"ࠩࡱࡹࡱࡲࠧᔬ")
            os.environ[bstack11ll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩᔭ")] = bstack11ll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᔮ")
            os.environ[bstack11ll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭ᔯ")] = bstack11ll_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᔰ")
            bstack1lll1lll111_opy_ = response.json()
            if bstack1lll1lll111_opy_ and bstack1lll1lll111_opy_[bstack11ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᔱ")]:
                error_message = bstack1lll1lll111_opy_[bstack11ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᔲ")]
                if bstack1lll1lll111_opy_[bstack11ll_opy_ (u"ࠩࡨࡶࡷࡵࡲࡕࡻࡳࡩࠬᔳ")] == bstack11ll_opy_ (u"ࠪࡉࡗࡘࡏࡓࡡࡌࡒ࡛ࡇࡌࡊࡆࡢࡇࡗࡋࡄࡆࡐࡗࡍࡆࡒࡓࠨᔴ"):
                    logger.error(error_message)
                elif bstack1lll1lll111_opy_[bstack11ll_opy_ (u"ࠫࡪࡸࡲࡰࡴࡗࡽࡵ࡫ࠧᔵ")] == bstack11ll_opy_ (u"ࠬࡋࡒࡓࡑࡕࡣࡆࡉࡃࡆࡕࡖࡣࡉࡋࡎࡊࡇࡇࠫᔶ"):
                    logger.info(error_message)
                elif bstack1lll1lll111_opy_[bstack11ll_opy_ (u"࠭ࡥࡳࡴࡲࡶ࡙ࡿࡰࡦࠩᔷ")] == bstack11ll_opy_ (u"ࠧࡆࡔࡕࡓࡗࡥࡓࡅࡍࡢࡈࡊࡖࡒࡆࡅࡄࡘࡊࡊࠧᔸ"):
                    logger.error(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack11ll_opy_ (u"ࠣࡆࡤࡸࡦࠦࡵࡱ࡮ࡲࡥࡩࠦࡴࡰࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡖࡨࡷࡹࠦࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࠦࡦࡢ࡫࡯ࡩࡩࠦࡤࡶࡧࠣࡸࡴࠦࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠥᔹ"))
            return [None, None, None]
        bstack1lll1lll111_opy_ = response.json()
        os.environ[bstack11ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᔺ")] = bstack1lll1lll111_opy_[bstack11ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬᔻ")]
        if cls.bstack1l11lll111_opy_(bstack1lll1ll1111_opy_.get(bstack11ll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡶࡵࡨࡨࠬᔼ"), bstack11ll_opy_ (u"ࠬ࠭ᔽ"))) is True:
            logger.debug(bstack11ll_opy_ (u"࠭ࡔࡦࡵࡷࠤࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲ࡙ࠥࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠣࠪᔾ"))
            os.environ[bstack11ll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡇࡔࡓࡐࡍࡇࡗࡉࡉ࠭ᔿ")] = bstack11ll_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᕀ")
            if bstack1lll1lll111_opy_.get(bstack11ll_opy_ (u"ࠩ࡭ࡻࡹ࠭ᕁ")):
                os.environ[bstack11ll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫᕂ")] = bstack1lll1lll111_opy_[bstack11ll_opy_ (u"ࠫ࡯ࡽࡴࠨᕃ")]
                os.environ[bstack11ll_opy_ (u"ࠬࡉࡒࡆࡆࡈࡒ࡙ࡏࡁࡍࡕࡢࡊࡔࡘ࡟ࡄࡔࡄࡗࡍࡥࡒࡆࡒࡒࡖ࡙ࡏࡎࡈࠩᕄ")] = json.dumps({
                    bstack11ll_opy_ (u"࠭ࡵࡴࡧࡵࡲࡦࡳࡥࠨᕅ"): bstack11ll11l11l_opy_,
                    bstack11ll_opy_ (u"ࠧࡱࡣࡶࡷࡼࡵࡲࡥࠩᕆ"): bstack11ll1111l1_opy_
                })
            if bstack1lll1lll111_opy_.get(bstack11ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᕇ")):
                os.environ[bstack11ll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨᕈ")] = bstack1lll1lll111_opy_[bstack11ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬᕉ")]
            if bstack1lll1lll111_opy_.get(bstack11ll_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨᕊ")):
                os.environ[bstack11ll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭ᕋ")] = str(bstack1lll1lll111_opy_[bstack11ll_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪᕌ")])
        return [bstack1lll1lll111_opy_[bstack11ll_opy_ (u"ࠧ࡫ࡹࡷࠫᕍ")], bstack1lll1lll111_opy_[bstack11ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᕎ")], bstack1lll1lll111_opy_[bstack11ll_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ᕏ")]]
    @classmethod
    @bstack1l111l1l1l_opy_(class_method=True)
    def stop(cls):
        if not cls.on():
            return
        if os.environ[bstack11ll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫᕐ")] == bstack11ll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᕑ") or os.environ[bstack11ll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫᕒ")] == bstack11ll_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᕓ"):
            print(bstack11ll_opy_ (u"ࠧࡆ࡚ࡆࡉࡕ࡚ࡉࡐࡐࠣࡍࡓࠦࡳࡵࡱࡳࡆࡺ࡯࡬ࡥࡗࡳࡷࡹࡸࡥࡢ࡯ࠣࡖࡊࡗࡕࡆࡕࡗࠤ࡙ࡕࠠࡕࡇࡖࡘࠥࡕࡂࡔࡇࡕ࡚ࡆࡈࡉࡍࡋࡗ࡝ࠥࡀࠠࡎ࡫ࡶࡷ࡮ࡴࡧࠡࡣࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢࡷࡳࡰ࡫࡮ࠨᕔ"))
            return {
                bstack11ll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᕕ"): bstack11ll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᕖ"),
                bstack11ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᕗ"): bstack11ll_opy_ (u"࡙ࠫࡵ࡫ࡦࡰ࠲ࡦࡺ࡯࡬ࡥࡋࡇࠤ࡮ࡹࠠࡶࡰࡧࡩ࡫࡯࡮ࡦࡦ࠯ࠤࡧࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥࡳࡩࡨࡪࡷࠤ࡭ࡧࡶࡦࠢࡩࡥ࡮ࡲࡥࡥࠩᕘ")
            }
        else:
            cls.bstack1lllll1l111_opy_.shutdown()
            data = {
                bstack11ll_opy_ (u"ࠬࡹࡴࡰࡲࡢࡸ࡮ࡳࡥࠨᕙ"): datetime.datetime.now().isoformat()
            }
            config = {
                bstack11ll_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧᕚ"): cls.default_headers()
            }
            bstack11l111l1ll_opy_ = bstack11ll_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿ࠲ࡷࡹࡵࡰࠨᕛ").format(os.environ[bstack11ll_opy_ (u"ࠣࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠢᕜ")])
            bstack1lll1lll1ll_opy_ = cls.request_url(bstack11l111l1ll_opy_)
            response = bstack1l11llll1_opy_(bstack11ll_opy_ (u"ࠩࡓ࡙࡙࠭ᕝ"), bstack1lll1lll1ll_opy_, data, config)
            if not response.ok:
                raise Exception(bstack11ll_opy_ (u"ࠥࡗࡹࡵࡰࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡱࡳࡹࠦ࡯࡬ࠤᕞ"))
    @classmethod
    def bstack11lll1l11l_opy_(cls):
        if cls.bstack1lllll1l111_opy_ is None:
            return
        cls.bstack1lllll1l111_opy_.shutdown()
    @classmethod
    def bstack1l1l11l111_opy_(cls):
        if cls.on():
            print(
                bstack11ll_opy_ (u"࡛ࠫ࡯ࡳࡪࡶࠣ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿࠣࡸࡴࠦࡶࡪࡧࡺࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡶ࡯ࡳࡶ࠯ࠤ࡮ࡴࡳࡪࡩ࡫ࡸࡸ࠲ࠠࡢࡰࡧࠤࡲࡧ࡮ࡺࠢࡰࡳࡷ࡫ࠠࡥࡧࡥࡹ࡬࡭ࡩ࡯ࡩࠣ࡭ࡳ࡬࡯ࡳ࡯ࡤࡸ࡮ࡵ࡮ࠡࡣ࡯ࡰࠥࡧࡴࠡࡱࡱࡩࠥࡶ࡬ࡢࡥࡨࠥࡡࡴࠧᕟ").format(os.environ[bstack11ll_opy_ (u"ࠧࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠦᕠ")]))
    @classmethod
    def bstack1lll1llll1l_opy_(cls):
        if cls.bstack1lllll1l111_opy_ is not None:
            return
        cls.bstack1lllll1l111_opy_ = bstack1lllll111ll_opy_(cls.bstack1lll1lll1l1_opy_)
        cls.bstack1lllll1l111_opy_.start()
    @classmethod
    def bstack1l1111l1l1_opy_(cls, bstack1l111ll111_opy_, bstack1llll111111_opy_=bstack11ll_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬᕡ")):
        if not cls.on():
            return
        bstack1111lll1l_opy_ = bstack1l111ll111_opy_[bstack11ll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᕢ")]
        bstack1lll1ll1lll_opy_ = {
            bstack11ll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᕣ"): bstack11ll_opy_ (u"ࠩࡗࡩࡸࡺ࡟ࡔࡶࡤࡶࡹࡥࡕࡱ࡮ࡲࡥࡩ࠭ᕤ"),
            bstack11ll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᕥ"): bstack11ll_opy_ (u"࡙ࠫ࡫ࡳࡵࡡࡈࡲࡩࡥࡕࡱ࡮ࡲࡥࡩ࠭ᕦ"),
            bstack11ll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭ᕧ"): bstack11ll_opy_ (u"࠭ࡔࡦࡵࡷࡣࡘࡱࡩࡱࡲࡨࡨࡤ࡛ࡰ࡭ࡱࡤࡨࠬᕨ"),
            bstack11ll_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫᕩ"): bstack11ll_opy_ (u"ࠨࡎࡲ࡫ࡤ࡛ࡰ࡭ࡱࡤࡨࠬᕪ"),
            bstack11ll_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᕫ"): bstack11ll_opy_ (u"ࠪࡌࡴࡵ࡫ࡠࡕࡷࡥࡷࡺ࡟ࡖࡲ࡯ࡳࡦࡪࠧᕬ"),
            bstack11ll_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᕭ"): bstack11ll_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡢࡉࡳࡪ࡟ࡖࡲ࡯ࡳࡦࡪࠧᕮ"),
            bstack11ll_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪᕯ"): bstack11ll_opy_ (u"ࠧࡄࡄࡗࡣ࡚ࡶ࡬ࡰࡣࡧࠫᕰ")
        }.get(bstack1111lll1l_opy_)
        if bstack1llll111111_opy_ == bstack11ll_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧᕱ"):
            cls.bstack1lll1llll1l_opy_()
            cls.bstack1lllll1l111_opy_.add(bstack1l111ll111_opy_)
        elif bstack1llll111111_opy_ == bstack11ll_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧᕲ"):
            cls.bstack1lll1lll1l1_opy_([bstack1l111ll111_opy_], bstack1llll111111_opy_)
    @classmethod
    @bstack1l111l1l1l_opy_(class_method=True)
    def bstack1lll1lll1l1_opy_(cls, bstack1l111ll111_opy_, bstack1llll111111_opy_=bstack11ll_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩᕳ")):
        config = {
            bstack11ll_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬᕴ"): cls.default_headers()
        }
        response = bstack1l11llll1_opy_(bstack11ll_opy_ (u"ࠬࡖࡏࡔࡖࠪᕵ"), cls.request_url(bstack1llll111111_opy_), bstack1l111ll111_opy_, config)
        bstack11l1lll11l_opy_ = response.json()
    @classmethod
    @bstack1l111l1l1l_opy_(class_method=True)
    def bstack1l1ll11l_opy_(cls, bstack1l111l11ll_opy_):
        bstack1lll1lllll1_opy_ = []
        for log in bstack1l111l11ll_opy_:
            bstack1lll1l1llll_opy_ = {
                bstack11ll_opy_ (u"࠭࡫ࡪࡰࡧࠫᕶ"): bstack11ll_opy_ (u"ࠧࡕࡇࡖࡘࡤࡒࡏࡈࠩᕷ"),
                bstack11ll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᕸ"): log[bstack11ll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᕹ")],
                bstack11ll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᕺ"): log[bstack11ll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᕻ")],
                bstack11ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡢࡶࡪࡹࡰࡰࡰࡶࡩࠬᕼ"): {},
                bstack11ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᕽ"): log[bstack11ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᕾ")],
            }
            if bstack11ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᕿ") in log:
                bstack1lll1l1llll_opy_[bstack11ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᖀ")] = log[bstack11ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᖁ")]
            elif bstack11ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᖂ") in log:
                bstack1lll1l1llll_opy_[bstack11ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᖃ")] = log[bstack11ll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᖄ")]
            bstack1lll1lllll1_opy_.append(bstack1lll1l1llll_opy_)
        cls.bstack1l1111l1l1_opy_({
            bstack11ll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᖅ"): bstack11ll_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬᖆ"),
            bstack11ll_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧᖇ"): bstack1lll1lllll1_opy_
        })
    @classmethod
    @bstack1l111l1l1l_opy_(class_method=True)
    def bstack1lll1llll11_opy_(cls, steps):
        bstack1lll1l1lll1_opy_ = []
        for step in steps:
            bstack1lll1ll1l1l_opy_ = {
                bstack11ll_opy_ (u"ࠪ࡯࡮ࡴࡤࠨᖈ"): bstack11ll_opy_ (u"࡙ࠫࡋࡓࡕࡡࡖࡘࡊࡖࠧᖉ"),
                bstack11ll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᖊ"): step[bstack11ll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᖋ")],
                bstack11ll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᖌ"): step[bstack11ll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᖍ")],
                bstack11ll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᖎ"): step[bstack11ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᖏ")],
                bstack11ll_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭ᖐ"): step[bstack11ll_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧᖑ")]
            }
            if bstack11ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᖒ") in step:
                bstack1lll1ll1l1l_opy_[bstack11ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᖓ")] = step[bstack11ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᖔ")]
            elif bstack11ll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᖕ") in step:
                bstack1lll1ll1l1l_opy_[bstack11ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᖖ")] = step[bstack11ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᖗ")]
            bstack1lll1l1lll1_opy_.append(bstack1lll1ll1l1l_opy_)
        cls.bstack1l1111l1l1_opy_({
            bstack11ll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᖘ"): bstack11ll_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪᖙ"),
            bstack11ll_opy_ (u"ࠧ࡭ࡱࡪࡷࠬᖚ"): bstack1lll1l1lll1_opy_
        })
    @classmethod
    @bstack1l111l1l1l_opy_(class_method=True)
    def bstack1111l1l11_opy_(cls, screenshot):
        cls.bstack1l1111l1l1_opy_({
            bstack11ll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᖛ"): bstack11ll_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ᖜ"),
            bstack11ll_opy_ (u"ࠪࡰࡴ࡭ࡳࠨᖝ"): [{
                bstack11ll_opy_ (u"ࠫࡰ࡯࡮ࡥࠩᖞ"): bstack11ll_opy_ (u"࡚ࠬࡅࡔࡖࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࠧᖟ"),
                bstack11ll_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᖠ"): datetime.datetime.utcnow().isoformat() + bstack11ll_opy_ (u"࡛ࠧࠩᖡ"),
                bstack11ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᖢ"): screenshot[bstack11ll_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨᖣ")],
                bstack11ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᖤ"): screenshot[bstack11ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᖥ")]
            }]
        }, bstack1llll111111_opy_=bstack11ll_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪᖦ"))
    @classmethod
    @bstack1l111l1l1l_opy_(class_method=True)
    def bstack1ll1ll1ll_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1l1111l1l1_opy_({
            bstack11ll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᖧ"): bstack11ll_opy_ (u"ࠧࡄࡄࡗࡗࡪࡹࡳࡪࡱࡱࡇࡷ࡫ࡡࡵࡧࡧࠫᖨ"),
            bstack11ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪᖩ"): {
                bstack11ll_opy_ (u"ࠤࡸࡹ࡮ࡪࠢᖪ"): cls.current_test_uuid(),
                bstack11ll_opy_ (u"ࠥ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠤᖫ"): cls.bstack11lll11l1l_opy_(driver)
            }
        })
    @classmethod
    def on(cls):
        if os.environ.get(bstack11ll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬᖬ"), None) is None or os.environ[bstack11ll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭ᖭ")] == bstack11ll_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᖮ"):
            return False
        return True
    @classmethod
    def bstack1l11lll111_opy_(cls, framework=bstack11ll_opy_ (u"ࠢࠣᖯ")):
        if framework not in bstack11l1l1111l_opy_:
            return False
        bstack1lll1ll11ll_opy_ = not bstack11lll1l11_opy_()
        return bstack111llll1_opy_(cls.bs_config.get(bstack11ll_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᖰ"), bstack1lll1ll11ll_opy_))
    @staticmethod
    def request_url(url):
        return bstack11ll_opy_ (u"ࠩࡾࢁ࠴ࢁࡽࠨᖱ").format(bstack1lll1llllll_opy_, url)
    @staticmethod
    def default_headers():
        headers = {
            bstack11ll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩᖲ"): bstack11ll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧᖳ"),
            bstack11ll_opy_ (u"ࠬ࡞࠭ࡃࡕࡗࡅࡈࡑ࠭ࡕࡇࡖࡘࡔࡖࡓࠨᖴ"): bstack11ll_opy_ (u"࠭ࡴࡳࡷࡨࠫᖵ")
        }
        if os.environ.get(bstack11ll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡏ࡝ࡔࠨᖶ"), None):
            headers[bstack11ll_opy_ (u"ࠨࡃࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨᖷ")] = bstack11ll_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࡾࢁࠬᖸ").format(os.environ[bstack11ll_opy_ (u"ࠥࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠦᖹ")])
        return headers
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack11ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᖺ"), None)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack11ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᖻ"), None)
    @staticmethod
    def bstack11llllllll_opy_():
        if getattr(threading.current_thread(), bstack11ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᖼ"), None):
            return {
                bstack11ll_opy_ (u"ࠧࡵࡻࡳࡩࠬᖽ"): bstack11ll_opy_ (u"ࠨࡶࡨࡷࡹ࠭ᖾ"),
                bstack11ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᖿ"): getattr(threading.current_thread(), bstack11ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᗀ"), None)
            }
        if getattr(threading.current_thread(), bstack11ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᗁ"), None):
            return {
                bstack11ll_opy_ (u"ࠬࡺࡹࡱࡧࠪᗂ"): bstack11ll_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᗃ"),
                bstack11ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᗄ"): getattr(threading.current_thread(), bstack11ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᗅ"), None)
            }
        return None
    @staticmethod
    def bstack11lll11l1l_opy_(driver):
        return {
            bstack11l11l1ll1_opy_(): bstack11l11ll1ll_opy_(driver)
        }
    @staticmethod
    def bstack1lll1ll1ll1_opy_(exception_info, report):
        return [{bstack11ll_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬᗆ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack11ll1l1l11_opy_(typename):
        if bstack11ll_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨᗇ") in typename:
            return bstack11ll_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧᗈ")
        return bstack11ll_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨᗉ")
    @staticmethod
    def bstack1lll1lll11l_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l1ll111l1_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack11lll1l111_opy_(test, hook_name=None):
        bstack1lll1ll111l_opy_ = test.parent
        if hook_name in [bstack11ll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫᗊ"), bstack11ll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨᗋ"), bstack11ll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧᗌ"), bstack11ll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫᗍ")]:
            bstack1lll1ll111l_opy_ = test
        scope = []
        while bstack1lll1ll111l_opy_ is not None:
            scope.append(bstack1lll1ll111l_opy_.name)
            bstack1lll1ll111l_opy_ = bstack1lll1ll111l_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1lll1ll1l11_opy_(hook_type):
        if hook_type == bstack11ll_opy_ (u"ࠥࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠣᗎ"):
            return bstack11ll_opy_ (u"ࠦࡘ࡫ࡴࡶࡲࠣ࡬ࡴࡵ࡫ࠣᗏ")
        elif hook_type == bstack11ll_opy_ (u"ࠧࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠤᗐ"):
            return bstack11ll_opy_ (u"ࠨࡔࡦࡣࡵࡨࡴࡽ࡮ࠡࡪࡲࡳࡰࠨᗑ")
    @staticmethod
    def bstack1lll1ll11l1_opy_(bstack1l1l1l111l_opy_):
        try:
            if not bstack1l1ll111l1_opy_.on():
                return bstack1l1l1l111l_opy_
            if os.environ.get(bstack11ll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࠧᗒ"), None) == bstack11ll_opy_ (u"ࠣࡶࡵࡹࡪࠨᗓ"):
                tests = os.environ.get(bstack11ll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘࠨᗔ"), None)
                if tests is None or tests == bstack11ll_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᗕ"):
                    return bstack1l1l1l111l_opy_
                bstack1l1l1l111l_opy_ = tests.split(bstack11ll_opy_ (u"ࠫ࠱࠭ᗖ"))
                return bstack1l1l1l111l_opy_
        except Exception as exc:
            print(bstack11ll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡷ࡫ࡲࡶࡰࠣ࡬ࡦࡴࡤ࡭ࡧࡵ࠾ࠥࠨᗗ"), str(exc))
        return bstack1l1l1l111l_opy_
    @classmethod
    def bstack1l111lllll_opy_(cls, event: str, bstack1l111ll111_opy_: bstack1l11111ll1_opy_):
        bstack11lll1ll1l_opy_ = {
            bstack11ll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᗘ"): event,
            bstack1l111ll111_opy_.bstack1l11111lll_opy_(): bstack1l111ll111_opy_.bstack1l111lll1l_opy_(event)
        }
        bstack1l1ll111l1_opy_.bstack1l1111l1l1_opy_(bstack11lll1ll1l_opy_)