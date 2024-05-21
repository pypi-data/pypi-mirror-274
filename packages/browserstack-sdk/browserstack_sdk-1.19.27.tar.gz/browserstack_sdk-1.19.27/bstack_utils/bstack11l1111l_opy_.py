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
import requests
import logging
from urllib.parse import urlparse
from datetime import datetime
from bstack_utils.constants import bstack11ll11111l_opy_ as bstack11ll111ll1_opy_
from bstack_utils.bstack1l1l1l1ll_opy_ import bstack1l1l1l1ll_opy_
from bstack_utils.helper import bstack1llll1llll_opy_, bstack11l1lllll_opy_, bstack11l1ll1ll1_opy_, bstack11ll111111_opy_, bstack1ll1111l11_opy_, get_host_info, bstack11l1lll1l1_opy_, bstack1l11llll1_opy_, bstack1l111l1l1l_opy_
from browserstack_sdk._version import __version__
logger = logging.getLogger(__name__)
@bstack1l111l1l1l_opy_(class_method=False)
def _11l1lllll1_opy_(driver, bstack1ll1l1ll_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack11ll_opy_ (u"ࠫࡴࡹ࡟࡯ࡣࡰࡩࠬี"): caps.get(bstack11ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠫึ"), None),
        bstack11ll_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪื"): bstack1ll1l1ll_opy_.get(bstack11ll_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰุࠪ"), None),
        bstack11ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡱࡥࡲ࡫ูࠧ"): caps.get(bstack11ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ฺࠧ"), None),
        bstack11ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ฻"): caps.get(bstack11ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ฼"), None)
    }
  except Exception as error:
    logger.debug(bstack11ll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫࡫ࡴࡤࡪ࡬ࡲ࡬ࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡦࡨࡸࡦ࡯࡬ࡴࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࠦ࠺ࠡࠩ฽") + str(error))
  return response
def bstack11111ll11_opy_(config):
  return config.get(bstack11ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭฾"), False) or any([p.get(bstack11ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ฿"), False) == True for p in config.get(bstack11ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫเ"), [])])
def bstack11llll111_opy_(config, bstack1l1l111l_opy_):
  try:
    if not bstack11l1lllll_opy_(config):
      return False
    bstack11l1llll11_opy_ = config.get(bstack11ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩแ"), False)
    bstack11l1ll1lll_opy_ = config[bstack11ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭โ")][bstack1l1l111l_opy_].get(bstack11ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫใ"), None)
    if bstack11l1ll1lll_opy_ != None:
      bstack11l1llll11_opy_ = bstack11l1ll1lll_opy_
    bstack11l1ll1l1l_opy_ = os.getenv(bstack11ll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪไ")) is not None and len(os.getenv(bstack11ll_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫๅ"))) > 0 and os.getenv(bstack11ll_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬๆ")) != bstack11ll_opy_ (u"ࠨࡰࡸࡰࡱ࠭็")
    return bstack11l1llll11_opy_ and bstack11l1ll1l1l_opy_
  except Exception as error:
    logger.debug(bstack11ll_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡸࡨࡶ࡮࡬ࡹࡪࡰࡪࠤࡹ࡮ࡥࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࠦ࠺่ࠡࠩ") + str(error))
  return False
def bstack11ll1lll1_opy_(bstack11ll11l1l1_opy_, test_tags):
  bstack11ll11l1l1_opy_ = os.getenv(bstack11ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏ้ࠫ"))
  if bstack11ll11l1l1_opy_ is None:
    return True
  bstack11ll11l1l1_opy_ = json.loads(bstack11ll11l1l1_opy_)
  try:
    include_tags = bstack11ll11l1l1_opy_[bstack11ll_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦ๊ࠩ")] if bstack11ll_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧ๋ࠪ") in bstack11ll11l1l1_opy_ and isinstance(bstack11ll11l1l1_opy_[bstack11ll_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫ์")], list) else []
    exclude_tags = bstack11ll11l1l1_opy_[bstack11ll_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬํ")] if bstack11ll_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭๎") in bstack11ll11l1l1_opy_ and isinstance(bstack11ll11l1l1_opy_[bstack11ll_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ๏")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack11ll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡸࡤࡰ࡮ࡪࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡨࡥࡧࡱࡵࡩࠥࡹࡣࡢࡰࡱ࡭ࡳ࡭࠮ࠡࡇࡵࡶࡴࡸࠠ࠻ࠢࠥ๐") + str(error))
  return False
def bstack11l11lll1_opy_(config, bstack11ll111lll_opy_, bstack11l1lll1ll_opy_, bstack11l1llllll_opy_):
  bstack11ll11l11l_opy_ = bstack11l1ll1ll1_opy_(config)
  bstack11ll1111l1_opy_ = bstack11ll111111_opy_(config)
  if bstack11ll11l11l_opy_ is None or bstack11ll1111l1_opy_ is None:
    logger.error(bstack11ll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡲࡶࡰࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠽ࠤࡒ࡯ࡳࡴ࡫ࡱ࡫ࠥࡧࡵࡵࡪࡨࡲࡹ࡯ࡣࡢࡶ࡬ࡳࡳࠦࡴࡰ࡭ࡨࡲࠬ๑"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack11ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭๒"), bstack11ll_opy_ (u"࠭ࡻࡾࠩ๓")))
    data = {
        bstack11ll_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬ๔"): config[bstack11ll_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭๕")],
        bstack11ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ๖"): config.get(bstack11ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭๗"), os.path.basename(os.getcwd())),
        bstack11ll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡗ࡭ࡲ࡫ࠧ๘"): bstack1llll1llll_opy_(),
        bstack11ll_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪ๙"): config.get(bstack11ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡉ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩ๚"), bstack11ll_opy_ (u"ࠧࠨ๛")),
        bstack11ll_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ๜"): {
            bstack11ll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡓࡧ࡭ࡦࠩ๝"): bstack11ll111lll_opy_,
            bstack11ll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭๞"): bstack11l1lll1ll_opy_,
            bstack11ll_opy_ (u"ࠫࡸࡪ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ๟"): __version__,
            bstack11ll_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࠧ๠"): bstack11ll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭๡"),
            bstack11ll_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ๢"): bstack11ll_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࠪ๣"),
            bstack11ll_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩ๤"): bstack11l1llllll_opy_
        },
        bstack11ll_opy_ (u"ࠪࡷࡪࡺࡴࡪࡰࡪࡷࠬ๥"): settings,
        bstack11ll_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࡈࡵ࡮ࡵࡴࡲࡰࠬ๦"): bstack11l1lll1l1_opy_(),
        bstack11ll_opy_ (u"ࠬࡩࡩࡊࡰࡩࡳࠬ๧"): bstack1ll1111l11_opy_(),
        bstack11ll_opy_ (u"࠭ࡨࡰࡵࡷࡍࡳ࡬࡯ࠨ๨"): get_host_info(),
        bstack11ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ๩"): bstack11l1lllll_opy_(config)
    }
    headers = {
        bstack11ll_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧ๪"): bstack11ll_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬ๫"),
    }
    config = {
        bstack11ll_opy_ (u"ࠪࡥࡺࡺࡨࠨ๬"): (bstack11ll11l11l_opy_, bstack11ll1111l1_opy_),
        bstack11ll_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬ๭"): headers
    }
    response = bstack1l11llll1_opy_(bstack11ll_opy_ (u"ࠬࡖࡏࡔࡖࠪ๮"), bstack11ll111ll1_opy_ + bstack11ll_opy_ (u"࠭࠯ࡷ࠴࠲ࡸࡪࡹࡴࡠࡴࡸࡲࡸ࠭๯"), data, config)
    bstack11l1lll11l_opy_ = response.json()
    if bstack11l1lll11l_opy_[bstack11ll_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨ๰")]:
      parsed = json.loads(os.getenv(bstack11ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩ๱"), bstack11ll_opy_ (u"ࠩࡾࢁࠬ๲")))
      parsed[bstack11ll_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ๳")] = bstack11l1lll11l_opy_[bstack11ll_opy_ (u"ࠫࡩࡧࡴࡢࠩ๴")][bstack11ll_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭๵")]
      os.environ[bstack11ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧ๶")] = json.dumps(parsed)
      bstack1l1l1l1ll_opy_.bstack11ll11ll1l_opy_(bstack11l1lll11l_opy_[bstack11ll_opy_ (u"ࠧࡥࡣࡷࡥࠬ๷")][bstack11ll_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩ๸")])
      bstack1l1l1l1ll_opy_.bstack11ll11lll1_opy_(bstack11l1lll11l_opy_[bstack11ll_opy_ (u"ࠩࡧࡥࡹࡧࠧ๹")][bstack11ll_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷࠬ๺")])
      bstack1l1l1l1ll_opy_.store()
      return bstack11l1lll11l_opy_[bstack11ll_opy_ (u"ࠫࡩࡧࡴࡢࠩ๻")][bstack11ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࡙ࡵ࡫ࡦࡰࠪ๼")], bstack11l1lll11l_opy_[bstack11ll_opy_ (u"࠭ࡤࡢࡶࡤࠫ๽")][bstack11ll_opy_ (u"ࠧࡪࡦࠪ๾")]
    else:
      logger.error(bstack11ll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡶࡺࡴ࡮ࡪࡰࡪࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠺ࠡࠩ๿") + bstack11l1lll11l_opy_[bstack11ll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ຀")])
      if bstack11l1lll11l_opy_[bstack11ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫກ")] == bstack11ll_opy_ (u"ࠫࡎࡴࡶࡢ࡮࡬ࡨࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥࡶࡡࡴࡵࡨࡨ࠳࠭ຂ"):
        for bstack11ll11llll_opy_ in bstack11l1lll11l_opy_[bstack11ll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡷࠬ຃")]:
          logger.error(bstack11ll11llll_opy_[bstack11ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧຄ")])
      return None, None
  except Exception as error:
    logger.error(bstack11ll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡵࡹࡳࠦࡦࡰࡴࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡀࠠࠣ຅") +  str(error))
    return None, None
def bstack1lll1l1l11_opy_():
  if os.getenv(bstack11ll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ຆ")) is None:
    return {
        bstack11ll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩງ"): bstack11ll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩຈ"),
        bstack11ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬຉ"): bstack11ll_opy_ (u"ࠬࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡨࡢࡦࠣࡪࡦ࡯࡬ࡦࡦ࠱ࠫຊ")
    }
  data = {bstack11ll_opy_ (u"࠭ࡥ࡯ࡦࡗ࡭ࡲ࡫ࠧ຋"): bstack1llll1llll_opy_()}
  headers = {
      bstack11ll_opy_ (u"ࠧࡂࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧຌ"): bstack11ll_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࠩຍ") + os.getenv(bstack11ll_opy_ (u"ࠤࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠢຎ")),
      bstack11ll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩຏ"): bstack11ll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧຐ")
  }
  response = bstack1l11llll1_opy_(bstack11ll_opy_ (u"ࠬࡖࡕࡕࠩຑ"), bstack11ll111ll1_opy_ + bstack11ll_opy_ (u"࠭࠯ࡵࡧࡶࡸࡤࡸࡵ࡯ࡵ࠲ࡷࡹࡵࡰࠨຒ"), data, { bstack11ll_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨຓ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack11ll_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤ࡙࡫ࡳࡵࠢࡕࡹࡳࠦ࡭ࡢࡴ࡮ࡩࡩࠦࡡࡴࠢࡦࡳࡲࡶ࡬ࡦࡶࡨࡨࠥࡧࡴࠡࠤດ") + datetime.utcnow().isoformat() + bstack11ll_opy_ (u"ࠩ࡝ࠫຕ"))
      return {bstack11ll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪຖ"): bstack11ll_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬທ"), bstack11ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ຘ"): bstack11ll_opy_ (u"࠭ࠧນ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack11ll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡧࡴࡳࡰ࡭ࡧࡷ࡭ࡴࡴࠠࡰࡨࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡔࡦࡵࡷࠤࡗࡻ࡮࠻ࠢࠥບ") + str(error))
    return {
        bstack11ll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨປ"): bstack11ll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨຜ"),
        bstack11ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫຝ"): str(error)
    }
def bstack1l11l1ll1l_opy_(caps, options):
  try:
    bstack11ll11l111_opy_ = caps.get(bstack11ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬພ"), {}).get(bstack11ll_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩຟ"), caps.get(bstack11ll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ຠ"), bstack11ll_opy_ (u"ࠧࠨມ")))
    if bstack11ll11l111_opy_:
      logger.warn(bstack11ll_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡆࡨࡷࡰࡺ࡯ࡱࠢࡥࡶࡴࡽࡳࡦࡴࡶ࠲ࠧຢ"))
      return False
    browser = caps.get(bstack11ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧຣ"), bstack11ll_opy_ (u"ࠪࠫ຤")).lower()
    if browser != bstack11ll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫລ"):
      logger.warn(bstack11ll_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡉࡨࡳࡱࡰࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹ࠮ࠣ຦"))
      return False
    browser_version = caps.get(bstack11ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧວ"), caps.get(bstack11ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩຨ")))
    if browser_version and browser_version != bstack11ll_opy_ (u"ࠨ࡮ࡤࡸࡪࡹࡴࠨຩ") and int(browser_version.split(bstack11ll_opy_ (u"ࠩ࠱ࠫສ"))[0]) <= 94:
      logger.warn(bstack11ll_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥ࡭ࡲࡦࡣࡷࡩࡷࠦࡴࡩࡣࡱࠤ࠾࠺࠮ࠣຫ"))
      return False
    if not options is None:
      bstack11ll11ll11_opy_ = options.to_capabilities().get(bstack11ll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩຬ"), {})
      if bstack11ll_opy_ (u"ࠬ࠳࠭ࡩࡧࡤࡨࡱ࡫ࡳࡴࠩອ") in bstack11ll11ll11_opy_.get(bstack11ll_opy_ (u"࠭ࡡࡳࡩࡶࠫຮ"), []):
        logger.warn(bstack11ll_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡱࡳࡹࠦࡲࡶࡰࠣࡳࡳࠦ࡬ࡦࡩࡤࡧࡾࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠠࡔࡹ࡬ࡸࡨ࡮ࠠࡵࡱࠣࡲࡪࡽࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫ࠠࡰࡴࠣࡥࡻࡵࡩࡥࠢࡸࡷ࡮ࡴࡧࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠤຯ"))
        return False
    return True
  except Exception as error:
    logger.debug(bstack11ll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡷࡣ࡯࡭ࡩࡧࡴࡦࠢࡤ࠵࠶ࡿࠠࡴࡷࡳࡴࡴࡸࡴࠡ࠼ࠥະ") + str(error))
    return False
def set_capabilities(caps, config):
  try:
    bstack11ll111l11_opy_ = config.get(bstack11ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩັ"), {})
    bstack11ll111l11_opy_[bstack11ll_opy_ (u"ࠪࡥࡺࡺࡨࡕࡱ࡮ࡩࡳ࠭າ")] = os.getenv(bstack11ll_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩຳ"))
    bstack11ll111l1l_opy_ = json.loads(os.getenv(bstack11ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ິ"), bstack11ll_opy_ (u"࠭ࡻࡾࠩີ"))).get(bstack11ll_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨຶ"))
    caps[bstack11ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨື")] = True
    if bstack11ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵຸࠪ") in caps:
      caps[bstack11ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶູࠫ")][bstack11ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶ຺ࠫ")] = bstack11ll111l11_opy_
      caps[bstack11ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ົ")][bstack11ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ຼ")][bstack11ll_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨຽ")] = bstack11ll111l1l_opy_
    else:
      caps[bstack11ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ຾")] = bstack11ll111l11_opy_
      caps[bstack11ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ຿")][bstack11ll_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫເ")] = bstack11ll111l1l_opy_
  except Exception as error:
    logger.debug(bstack11ll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵ࠱ࠤࡊࡸࡲࡰࡴ࠽ࠤࠧແ") +  str(error))
def bstack11111l11l_opy_(driver, bstack11ll1111ll_opy_):
  try:
    setattr(driver, bstack11ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬໂ"), True)
    session = driver.session_id
    if session:
      bstack11l1lll111_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11l1lll111_opy_ = False
      bstack11l1lll111_opy_ = url.scheme in [bstack11ll_opy_ (u"ࠨࡨࡵࡶࡳࠦໃ"), bstack11ll_opy_ (u"ࠢࡩࡶࡷࡴࡸࠨໄ")]
      if bstack11l1lll111_opy_:
        if bstack11ll1111ll_opy_:
          logger.info(bstack11ll_opy_ (u"ࠣࡕࡨࡸࡺࡶࠠࡧࡱࡵࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡮ࡡࡴࠢࡶࡸࡦࡸࡴࡦࡦ࠱ࠤࡆࡻࡴࡰ࡯ࡤࡸࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡦࡪ࡭ࡩ࡯ࠢࡰࡳࡲ࡫࡮ࡵࡣࡵ࡭ࡱࡿ࠮ࠣ໅"))
      return bstack11ll1111ll_opy_
  except Exception as e:
    logger.error(bstack11ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡷࡥࡷࡺࡩ࡯ࡩࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡥࡤࡲࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧ࠽ࠤࠧໆ") + str(e))
    return False
def bstack1lll1ll1_opy_(driver, class_name, name, module_name, path, bstack1ll1l1ll_opy_):
  try:
    bstack11lll111l1_opy_ = [class_name] if not class_name is None else []
    bstack11ll11l1ll_opy_ = {
        bstack11ll_opy_ (u"ࠥࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠣ໇"): True,
        bstack11ll_opy_ (u"ࠦࡹ࡫ࡳࡵࡆࡨࡸࡦ࡯࡬ࡴࠤ່"): {
            bstack11ll_opy_ (u"ࠧࡴࡡ࡮ࡧ້ࠥ"): name,
            bstack11ll_opy_ (u"ࠨࡴࡦࡵࡷࡖࡺࡴࡉࡥࠤ໊"): os.environ.get(bstack11ll_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡖࡈࡗ࡙ࡥࡒࡖࡐࡢࡍࡉ໋࠭")),
            bstack11ll_opy_ (u"ࠣࡨ࡬ࡰࡪࡖࡡࡵࡪࠥ໌"): str(path),
            bstack11ll_opy_ (u"ࠤࡶࡧࡴࡶࡥࡍ࡫ࡶࡸࠧໍ"): [module_name, *bstack11lll111l1_opy_, name],
        },
        bstack11ll_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧ໎"): _11l1lllll1_opy_(driver, bstack1ll1l1ll_opy_)
    }
    logger.debug(bstack11ll_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡢࡦࡨࡲࡶࡪࠦࡳࡢࡸ࡬ࡲ࡬ࠦࡲࡦࡵࡸࡰࡹࡹࠧ໏"))
    logger.debug(driver.execute_async_script(bstack1l1l1l1ll_opy_.perform_scan, {bstack11ll_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࠧ໐"): name}))
    logger.debug(driver.execute_async_script(bstack1l1l1l1ll_opy_.bstack11ll1l1111_opy_, bstack11ll11l1ll_opy_))
    logger.info(bstack11ll_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠤ໑"))
  except Exception as bstack11l1llll1l_opy_:
    logger.error(bstack11ll_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡥࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡧ࡫ࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡪࡴࡸࠠࡵࡪࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫࠺ࠡࠤ໒") + str(path) + bstack11ll_opy_ (u"ࠣࠢࡈࡶࡷࡵࡲࠡ࠼ࠥ໓") + str(bstack11l1llll1l_opy_))