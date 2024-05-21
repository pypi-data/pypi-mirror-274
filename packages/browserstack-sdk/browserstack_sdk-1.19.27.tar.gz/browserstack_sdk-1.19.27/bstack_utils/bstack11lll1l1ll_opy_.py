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
from uuid import uuid4
from bstack_utils.helper import bstack1llll1llll_opy_, bstack11l1111l1l_opy_
from bstack_utils.bstack1llll111l1_opy_ import bstack1lllll1ll1l_opy_
class bstack1l11111ll1_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, bstack1l111ll11l_opy_=None, framework=None, tags=[], scope=[], bstack1llll111lll_opy_=None, bstack1llll111l1l_opy_=True, bstack1llll11llll_opy_=None, bstack1111lll1l_opy_=None, result=None, duration=None, bstack11lll1llll_opy_=None, meta={}):
        self.bstack11lll1llll_opy_ = bstack11lll1llll_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1llll111l1l_opy_:
            self.uuid = uuid4().__str__()
        self.bstack1l111ll11l_opy_ = bstack1l111ll11l_opy_
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1llll111lll_opy_ = bstack1llll111lll_opy_
        self.bstack1llll11llll_opy_ = bstack1llll11llll_opy_
        self.bstack1111lll1l_opy_ = bstack1111lll1l_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
    def bstack11lll11lll_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack1llll1l11ll_opy_(self):
        bstack1llll11lll1_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack11ll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ᒶ"): bstack1llll11lll1_opy_,
            bstack11ll_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࠭ᒷ"): bstack1llll11lll1_opy_,
            bstack11ll_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪᒸ"): bstack1llll11lll1_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack11ll_opy_ (u"ࠨࡕ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸ࠿ࠦࠢᒹ") + key)
            setattr(self, key, val)
    def bstack1llll1l1111_opy_(self):
        return {
            bstack11ll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᒺ"): self.name,
            bstack11ll_opy_ (u"ࠨࡤࡲࡨࡾ࠭ᒻ"): {
                bstack11ll_opy_ (u"ࠩ࡯ࡥࡳ࡭ࠧᒼ"): bstack11ll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪᒽ"),
                bstack11ll_opy_ (u"ࠫࡨࡵࡤࡦࠩᒾ"): self.code
            },
            bstack11ll_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬᒿ"): self.scope,
            bstack11ll_opy_ (u"࠭ࡴࡢࡩࡶࠫᓀ"): self.tags,
            bstack11ll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᓁ"): self.framework,
            bstack11ll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᓂ"): self.bstack1l111ll11l_opy_
        }
    def bstack1llll111l11_opy_(self):
        return {
         bstack11ll_opy_ (u"ࠩࡰࡩࡹࡧࠧᓃ"): self.meta
        }
    def bstack1llll1111l1_opy_(self):
        return {
            bstack11ll_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡕࡩࡷࡻ࡮ࡑࡣࡵࡥࡲ࠭ᓄ"): {
                bstack11ll_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡢࡲࡦࡳࡥࠨᓅ"): self.bstack1llll111lll_opy_
            }
        }
    def bstack1llll1111ll_opy_(self, bstack1llll11ll11_opy_, details):
        step = next(filter(lambda st: st[bstack11ll_opy_ (u"ࠬ࡯ࡤࠨᓆ")] == bstack1llll11ll11_opy_, self.meta[bstack11ll_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᓇ")]), None)
        step.update(details)
    def bstack1llll11l1l1_opy_(self, bstack1llll11ll11_opy_):
        step = next(filter(lambda st: st[bstack11ll_opy_ (u"ࠧࡪࡦࠪᓈ")] == bstack1llll11ll11_opy_, self.meta[bstack11ll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᓉ")]), None)
        step.update({
            bstack11ll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᓊ"): bstack1llll1llll_opy_()
        })
    def bstack11lll1l1l1_opy_(self, bstack1llll11ll11_opy_, result, duration=None):
        bstack1llll11llll_opy_ = bstack1llll1llll_opy_()
        if bstack1llll11ll11_opy_ is not None and self.meta.get(bstack11ll_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᓋ")):
            step = next(filter(lambda st: st[bstack11ll_opy_ (u"ࠫ࡮ࡪࠧᓌ")] == bstack1llll11ll11_opy_, self.meta[bstack11ll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᓍ")]), None)
            step.update({
                bstack11ll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᓎ"): bstack1llll11llll_opy_,
                bstack11ll_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩᓏ"): duration if duration else bstack11l1111l1l_opy_(step[bstack11ll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᓐ")], bstack1llll11llll_opy_),
                bstack11ll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᓑ"): result.result,
                bstack11ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᓒ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1llll11l1ll_opy_):
        if self.meta.get(bstack11ll_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᓓ")):
            self.meta[bstack11ll_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᓔ")].append(bstack1llll11l1ll_opy_)
        else:
            self.meta[bstack11ll_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᓕ")] = [ bstack1llll11l1ll_opy_ ]
    def bstack1llll111ll1_opy_(self):
        return {
            bstack11ll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᓖ"): self.bstack11lll11lll_opy_(),
            **self.bstack1llll1l1111_opy_(),
            **self.bstack1llll1l11ll_opy_(),
            **self.bstack1llll111l11_opy_()
        }
    def bstack1llll1l11l1_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack11ll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᓗ"): self.bstack1llll11llll_opy_,
            bstack11ll_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪᓘ"): self.duration,
            bstack11ll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᓙ"): self.result.result
        }
        if data[bstack11ll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᓚ")] == bstack11ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᓛ"):
            data[bstack11ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬᓜ")] = self.result.bstack11ll1l1l11_opy_()
            data[bstack11ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᓝ")] = [{bstack11ll_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᓞ"): self.result.bstack111ll1lll1_opy_()}]
        return data
    def bstack1llll1l1l11_opy_(self):
        return {
            bstack11ll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᓟ"): self.bstack11lll11lll_opy_(),
            **self.bstack1llll1l1111_opy_(),
            **self.bstack1llll1l11ll_opy_(),
            **self.bstack1llll1l11l1_opy_(),
            **self.bstack1llll111l11_opy_()
        }
    def bstack1l111lll1l_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack11ll_opy_ (u"ࠪࡗࡹࡧࡲࡵࡧࡧࠫᓠ") in event:
            return self.bstack1llll111ll1_opy_()
        elif bstack11ll_opy_ (u"ࠫࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᓡ") in event:
            return self.bstack1llll1l1l11_opy_()
    def bstack1l11111lll_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1llll11llll_opy_ = time if time else bstack1llll1llll_opy_()
        self.duration = duration if duration else bstack11l1111l1l_opy_(self.bstack1l111ll11l_opy_, self.bstack1llll11llll_opy_)
        if result:
            self.result = result
class bstack1l1111ll1l_opy_(bstack1l11111ll1_opy_):
    def __init__(self, hooks=[], bstack11lllll1l1_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack11lllll1l1_opy_ = bstack11lllll1l1_opy_
        super().__init__(*args, **kwargs, bstack1111lll1l_opy_=bstack11ll_opy_ (u"ࠬࡺࡥࡴࡶࠪᓢ"))
    @classmethod
    def bstack1llll1l111l_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11ll_opy_ (u"࠭ࡩࡥࠩᓣ"): id(step),
                bstack11ll_opy_ (u"ࠧࡵࡧࡻࡸࠬᓤ"): step.name,
                bstack11ll_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩᓥ"): step.keyword,
            })
        return bstack1l1111ll1l_opy_(
            **kwargs,
            meta={
                bstack11ll_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࠪᓦ"): {
                    bstack11ll_opy_ (u"ࠪࡲࡦࡳࡥࠨᓧ"): feature.name,
                    bstack11ll_opy_ (u"ࠫࡵࡧࡴࡩࠩᓨ"): feature.filename,
                    bstack11ll_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪᓩ"): feature.description
                },
                bstack11ll_opy_ (u"࠭ࡳࡤࡧࡱࡥࡷ࡯࡯ࠨᓪ"): {
                    bstack11ll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᓫ"): scenario.name
                },
                bstack11ll_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᓬ"): steps,
                bstack11ll_opy_ (u"ࠩࡨࡼࡦࡳࡰ࡭ࡧࡶࠫᓭ"): bstack1lllll1ll1l_opy_(test)
            }
        )
    def bstack1llll11l111_opy_(self):
        return {
            bstack11ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᓮ"): self.hooks
        }
    def bstack1llll11ll1l_opy_(self):
        if self.bstack11lllll1l1_opy_:
            return {
                bstack11ll_opy_ (u"ࠫ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠪᓯ"): self.bstack11lllll1l1_opy_
            }
        return {}
    def bstack1llll1l1l11_opy_(self):
        return {
            **super().bstack1llll1l1l11_opy_(),
            **self.bstack1llll11l111_opy_()
        }
    def bstack1llll111ll1_opy_(self):
        return {
            **super().bstack1llll111ll1_opy_(),
            **self.bstack1llll11ll1l_opy_()
        }
    def bstack1l11111lll_opy_(self):
        return bstack11ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧᓰ")
class bstack1l111111l1_opy_(bstack1l11111ll1_opy_):
    def __init__(self, hook_type, *args, **kwargs):
        self.hook_type = hook_type
        super().__init__(*args, **kwargs, bstack1111lll1l_opy_=bstack11ll_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᓱ"))
    def bstack11llll11ll_opy_(self):
        return self.hook_type
    def bstack1llll11l11l_opy_(self):
        return {
            bstack11ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪᓲ"): self.hook_type
        }
    def bstack1llll1l1l11_opy_(self):
        return {
            **super().bstack1llll1l1l11_opy_(),
            **self.bstack1llll11l11l_opy_()
        }
    def bstack1llll111ll1_opy_(self):
        return {
            **super().bstack1llll111ll1_opy_(),
            **self.bstack1llll11l11l_opy_()
        }
    def bstack1l11111lll_opy_(self):
        return bstack11ll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࠪᓳ")