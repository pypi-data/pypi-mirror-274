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
from urllib.parse import urlparse
from bstack_utils.messages import bstack111l111l11_opy_
def bstack1lllllll111_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1lllllll1l1_opy_(bstack1llllll1lll_opy_, bstack1llllllll11_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1llllll1lll_opy_):
        with open(bstack1llllll1lll_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1lllllll111_opy_(bstack1llllll1lll_opy_):
        pac = get_pac(url=bstack1llllll1lll_opy_)
    else:
        raise Exception(bstack11ll_opy_ (u"ࠨࡒࡤࡧࠥ࡬ࡩ࡭ࡧࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥ࡫ࡸࡪࡵࡷ࠾ࠥࢁࡽࠨᐨ").format(bstack1llllll1lll_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack11ll_opy_ (u"ࠤ࠻࠲࠽࠴࠸࠯࠺ࠥᐩ"), 80))
        bstack1lllllll11l_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1lllllll11l_opy_ = bstack11ll_opy_ (u"ࠪ࠴࠳࠶࠮࠱࠰࠳ࠫᐪ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1llllllll11_opy_, bstack1lllllll11l_opy_)
    return proxy_url
def bstack1ll1l11ll_opy_(config):
    return bstack11ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᐫ") in config or bstack11ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩᐬ") in config
def bstack1ll111lll1_opy_(config):
    if not bstack1ll1l11ll_opy_(config):
        return
    if config.get(bstack11ll_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᐭ")):
        return config.get(bstack11ll_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪᐮ"))
    if config.get(bstack11ll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬᐯ")):
        return config.get(bstack11ll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ᐰ"))
def bstack11ll11l11_opy_(config, bstack1llllllll11_opy_):
    proxy = bstack1ll111lll1_opy_(config)
    proxies = {}
    if config.get(bstack11ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ᐱ")) or config.get(bstack11ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨᐲ")):
        if proxy.endswith(bstack11ll_opy_ (u"ࠬ࠴ࡰࡢࡥࠪᐳ")):
            proxies = bstack11l1ll11l_opy_(proxy, bstack1llllllll11_opy_)
        else:
            proxies = {
                bstack11ll_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᐴ"): proxy
            }
    return proxies
def bstack11l1ll11l_opy_(bstack1llllll1lll_opy_, bstack1llllllll11_opy_):
    proxies = {}
    global bstack1llllllll1l_opy_
    if bstack11ll_opy_ (u"ࠧࡑࡃࡆࡣࡕࡘࡏ࡙࡛ࠪᐵ") in globals():
        return bstack1llllllll1l_opy_
    try:
        proxy = bstack1lllllll1l1_opy_(bstack1llllll1lll_opy_, bstack1llllllll11_opy_)
        if bstack11ll_opy_ (u"ࠣࡆࡌࡖࡊࡉࡔࠣᐶ") in proxy:
            proxies = {}
        elif bstack11ll_opy_ (u"ࠤࡋࡘ࡙ࡖࠢᐷ") in proxy or bstack11ll_opy_ (u"ࠥࡌ࡙࡚ࡐࡔࠤᐸ") in proxy or bstack11ll_opy_ (u"ࠦࡘࡕࡃࡌࡕࠥᐹ") in proxy:
            bstack1lllllll1ll_opy_ = proxy.split(bstack11ll_opy_ (u"ࠧࠦࠢᐺ"))
            if bstack11ll_opy_ (u"ࠨ࠺࠰࠱ࠥᐻ") in bstack11ll_opy_ (u"ࠢࠣᐼ").join(bstack1lllllll1ll_opy_[1:]):
                proxies = {
                    bstack11ll_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᐽ"): bstack11ll_opy_ (u"ࠤࠥᐾ").join(bstack1lllllll1ll_opy_[1:])
                }
            else:
                proxies = {
                    bstack11ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᐿ"): str(bstack1lllllll1ll_opy_[0]).lower() + bstack11ll_opy_ (u"ࠦ࠿࠵࠯ࠣᑀ") + bstack11ll_opy_ (u"ࠧࠨᑁ").join(bstack1lllllll1ll_opy_[1:])
                }
        elif bstack11ll_opy_ (u"ࠨࡐࡓࡑ࡛࡝ࠧᑂ") in proxy:
            bstack1lllllll1ll_opy_ = proxy.split(bstack11ll_opy_ (u"ࠢࠡࠤᑃ"))
            if bstack11ll_opy_ (u"ࠣ࠼࠲࠳ࠧᑄ") in bstack11ll_opy_ (u"ࠤࠥᑅ").join(bstack1lllllll1ll_opy_[1:]):
                proxies = {
                    bstack11ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᑆ"): bstack11ll_opy_ (u"ࠦࠧᑇ").join(bstack1lllllll1ll_opy_[1:])
                }
            else:
                proxies = {
                    bstack11ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᑈ"): bstack11ll_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢᑉ") + bstack11ll_opy_ (u"ࠢࠣᑊ").join(bstack1lllllll1ll_opy_[1:])
                }
        else:
            proxies = {
                bstack11ll_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᑋ"): proxy
            }
    except Exception as e:
        print(bstack11ll_opy_ (u"ࠤࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷࠨᑌ"), bstack111l111l11_opy_.format(bstack1llllll1lll_opy_, str(e)))
    bstack1llllllll1l_opy_ = proxies
    return proxies