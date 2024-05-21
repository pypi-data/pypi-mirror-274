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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.helper import bstack111lll11ll_opy_, bstack1ll111ll1_opy_, bstack1ll1l111ll_opy_, bstack1lllll1ll1_opy_, \
    bstack111ll11lll_opy_
def bstack1llll11l11_opy_(bstack1llll1l1ll1_opy_):
    for driver in bstack1llll1l1ll1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1l1l11l11_opy_(driver, status, reason=bstack11ll_opy_ (u"ࠧࠨᒂ")):
    bstack11llll1l_opy_ = Config.bstack11l1l11l1_opy_()
    if bstack11llll1l_opy_.bstack11lll1111l_opy_():
        return
    bstack1l11l1ll11_opy_ = bstack1lllll111l_opy_(bstack11ll_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᒃ"), bstack11ll_opy_ (u"ࠩࠪᒄ"), status, reason, bstack11ll_opy_ (u"ࠪࠫᒅ"), bstack11ll_opy_ (u"ࠫࠬᒆ"))
    driver.execute_script(bstack1l11l1ll11_opy_)
def bstack1ll11l111l_opy_(page, status, reason=bstack11ll_opy_ (u"ࠬ࠭ᒇ")):
    try:
        if page is None:
            return
        bstack11llll1l_opy_ = Config.bstack11l1l11l1_opy_()
        if bstack11llll1l_opy_.bstack11lll1111l_opy_():
            return
        bstack1l11l1ll11_opy_ = bstack1lllll111l_opy_(bstack11ll_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩᒈ"), bstack11ll_opy_ (u"ࠧࠨᒉ"), status, reason, bstack11ll_opy_ (u"ࠨࠩᒊ"), bstack11ll_opy_ (u"ࠩࠪᒋ"))
        page.evaluate(bstack11ll_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦᒌ"), bstack1l11l1ll11_opy_)
    except Exception as e:
        print(bstack11ll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡬࡯ࡳࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡻࡾࠤᒍ"), e)
def bstack1lllll111l_opy_(type, name, status, reason, bstack111l11l1l_opy_, bstack1ll1111l_opy_):
    bstack1ll111ll11_opy_ = {
        bstack11ll_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬᒎ"): type,
        bstack11ll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᒏ"): {}
    }
    if type == bstack11ll_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩᒐ"):
        bstack1ll111ll11_opy_[bstack11ll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᒑ")][bstack11ll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᒒ")] = bstack111l11l1l_opy_
        bstack1ll111ll11_opy_[bstack11ll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᒓ")][bstack11ll_opy_ (u"ࠫࡩࡧࡴࡢࠩᒔ")] = json.dumps(str(bstack1ll1111l_opy_))
    if type == bstack11ll_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᒕ"):
        bstack1ll111ll11_opy_[bstack11ll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᒖ")][bstack11ll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᒗ")] = name
    if type == bstack11ll_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᒘ"):
        bstack1ll111ll11_opy_[bstack11ll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᒙ")][bstack11ll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᒚ")] = status
        if status == bstack11ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᒛ") and str(reason) != bstack11ll_opy_ (u"ࠧࠨᒜ"):
            bstack1ll111ll11_opy_[bstack11ll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᒝ")][bstack11ll_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧᒞ")] = json.dumps(str(reason))
    bstack1ll1lll11_opy_ = bstack11ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ᒟ").format(json.dumps(bstack1ll111ll11_opy_))
    return bstack1ll1lll11_opy_
def bstack1ll111l111_opy_(url, config, logger, bstack11llll11_opy_=False):
    hostname = bstack1ll111ll1_opy_(url)
    is_private = bstack1lllll1ll1_opy_(hostname)
    try:
        if is_private or bstack11llll11_opy_:
            file_path = bstack111lll11ll_opy_(bstack11ll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᒠ"), bstack11ll_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩᒡ"), logger)
            if os.environ.get(bstack11ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩᒢ")) and eval(
                    os.environ.get(bstack11ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡒࡔ࡚࡟ࡔࡇࡗࡣࡊࡘࡒࡐࡔࠪᒣ"))):
                return
            if (bstack11ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᒤ") in config and not config[bstack11ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫᒥ")]):
                os.environ[bstack11ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭ᒦ")] = str(True)
                bstack1llll1ll111_opy_ = {bstack11ll_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫᒧ"): hostname}
                bstack111ll11lll_opy_(bstack11ll_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩᒨ"), bstack11ll_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩᒩ"), bstack1llll1ll111_opy_, logger)
    except Exception as e:
        pass
def bstack1l1l1l11l1_opy_(caps, bstack1llll1l1l1l_opy_):
    if bstack11ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᒪ") in caps:
        caps[bstack11ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᒫ")][bstack11ll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭ᒬ")] = True
        if bstack1llll1l1l1l_opy_:
            caps[bstack11ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᒭ")][bstack11ll_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᒮ")] = bstack1llll1l1l1l_opy_
    else:
        caps[bstack11ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࠨᒯ")] = True
        if bstack1llll1l1l1l_opy_:
            caps[bstack11ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᒰ")] = bstack1llll1l1l1l_opy_
def bstack1llllll1l11_opy_(bstack1l111l111l_opy_):
    bstack1llll1l1lll_opy_ = bstack1ll1l111ll_opy_(threading.current_thread(), bstack11ll_opy_ (u"ࠬࡺࡥࡴࡶࡖࡸࡦࡺࡵࡴࠩᒱ"), bstack11ll_opy_ (u"࠭ࠧᒲ"))
    if bstack1llll1l1lll_opy_ == bstack11ll_opy_ (u"ࠧࠨᒳ") or bstack1llll1l1lll_opy_ == bstack11ll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᒴ"):
        threading.current_thread().testStatus = bstack1l111l111l_opy_
    else:
        if bstack1l111l111l_opy_ == bstack11ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᒵ"):
            threading.current_thread().testStatus = bstack1l111l111l_opy_