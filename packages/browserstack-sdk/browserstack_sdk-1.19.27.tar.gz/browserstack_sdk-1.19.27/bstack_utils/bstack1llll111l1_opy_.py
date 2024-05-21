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
import re
from bstack_utils.bstack1llllll111_opy_ import bstack1llllll1l11_opy_
def bstack1lllll1l11l_opy_(fixture_name):
    if fixture_name.startswith(bstack11ll_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᑍ")):
        return bstack11ll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᑎ")
    elif fixture_name.startswith(bstack11ll_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᑏ")):
        return bstack11ll_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬᑐ")
    elif fixture_name.startswith(bstack11ll_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᑑ")):
        return bstack11ll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᑒ")
    elif fixture_name.startswith(bstack11ll_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᑓ")):
        return bstack11ll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬᑔ")
def bstack1llllll11ll_opy_(fixture_name):
    return bool(re.match(bstack11ll_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠࠪࡩࡹࡳࡩࡴࡪࡱࡱࢀࡲࡵࡤࡶ࡮ࡨ࠭ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥ࠮ࠫࠩᑕ"), fixture_name))
def bstack1lllll1l1l1_opy_(fixture_name):
    return bool(re.match(bstack11ll_opy_ (u"ࠬࡤ࡟ࡹࡷࡱ࡭ࡹࡥࠨࡴࡧࡷࡹࡵࢂࡴࡦࡣࡵࡨࡴࡽ࡮ࠪࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭ᑖ"), fixture_name))
def bstack1llllll111l_opy_(fixture_name):
    return bool(re.match(bstack11ll_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࡢ࠲࠯࠭ᑗ"), fixture_name))
def bstack1llllll1ll1_opy_(fixture_name):
    if fixture_name.startswith(bstack11ll_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᑘ")):
        return bstack11ll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᑙ"), bstack11ll_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧᑚ")
    elif fixture_name.startswith(bstack11ll_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᑛ")):
        return bstack11ll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡱࡴࡪࡵ࡭ࡧࠪᑜ"), bstack11ll_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩᑝ")
    elif fixture_name.startswith(bstack11ll_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᑞ")):
        return bstack11ll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫᑟ"), bstack11ll_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬᑠ")
    elif fixture_name.startswith(bstack11ll_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᑡ")):
        return bstack11ll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬᑢ"), bstack11ll_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧᑣ")
    return None, None
def bstack1llllll1111_opy_(hook_name):
    if hook_name in [bstack11ll_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᑤ"), bstack11ll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨᑥ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1lllll1lll1_opy_(hook_name):
    if hook_name in [bstack11ll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᑦ"), bstack11ll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧᑧ")]:
        return bstack11ll_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧᑨ")
    elif hook_name in [bstack11ll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩᑩ"), bstack11ll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩᑪ")]:
        return bstack11ll_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩᑫ")
    elif hook_name in [bstack11ll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪᑬ"), bstack11ll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩᑭ")]:
        return bstack11ll_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬᑮ")
    elif hook_name in [bstack11ll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫᑯ"), bstack11ll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫᑰ")]:
        return bstack11ll_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡅࡑࡒࠧᑱ")
    return hook_name
def bstack1lllll1llll_opy_(node, scenario):
    if hasattr(node, bstack11ll_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧᑲ")):
        parts = node.nodeid.rsplit(bstack11ll_opy_ (u"ࠨ࡛ࠣᑳ"))
        params = parts[-1]
        return bstack11ll_opy_ (u"ࠢࡼࡿࠣ࡟ࢀࢃࠢᑴ").format(scenario.name, params)
    return scenario.name
def bstack1lllll1ll1l_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack11ll_opy_ (u"ࠨࡥࡤࡰࡱࡹࡰࡦࡥࠪᑵ")):
            examples = list(node.callspec.params[bstack11ll_opy_ (u"ࠩࡢࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡦࡺࡤࡱࡵࡲࡥࠨᑶ")].values())
        return examples
    except:
        return []
def bstack1lllll1l1ll_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1llllll11l1_opy_(report):
    try:
        status = bstack11ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᑷ")
        if report.passed or (report.failed and hasattr(report, bstack11ll_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨᑸ"))):
            status = bstack11ll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᑹ")
        elif report.skipped:
            status = bstack11ll_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᑺ")
        bstack1llllll1l11_opy_(status)
    except:
        pass
def bstack111l1l11l_opy_(status):
    try:
        bstack1lllll1ll11_opy_ = bstack11ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᑻ")
        if status == bstack11ll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᑼ"):
            bstack1lllll1ll11_opy_ = bstack11ll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᑽ")
        elif status == bstack11ll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᑾ"):
            bstack1lllll1ll11_opy_ = bstack11ll_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᑿ")
        bstack1llllll1l11_opy_(bstack1lllll1ll11_opy_)
    except:
        pass
def bstack1llllll1l1l_opy_(item=None, report=None, summary=None, extra=None):
    return