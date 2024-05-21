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
class bstack11l1ll111l_opy_(object):
  bstack1ll1llllll_opy_ = os.path.join(os.path.expanduser(bstack11ll_opy_ (u"ࠩࢁࠫ໔")), bstack11ll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ໕"))
  bstack11l1ll11ll_opy_ = os.path.join(bstack1ll1llllll_opy_, bstack11ll_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠴ࡪࡴࡱࡱࠫ໖"))
  bstack11l1ll1111_opy_ = None
  perform_scan = None
  bstack1lll11l1ll_opy_ = None
  bstack1l11ll1111_opy_ = None
  bstack11ll1l1111_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack11ll_opy_ (u"ࠬ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠧ໗")):
      cls.instance = super(bstack11l1ll111l_opy_, cls).__new__(cls)
      cls.instance.bstack11l1ll1l11_opy_()
    return cls.instance
  def bstack11l1ll1l11_opy_(self):
    try:
      with open(self.bstack11l1ll11ll_opy_, bstack11ll_opy_ (u"࠭ࡲࠨ໘")) as bstack11l1l111l_opy_:
        bstack11l1l1llll_opy_ = bstack11l1l111l_opy_.read()
        data = json.loads(bstack11l1l1llll_opy_)
        if bstack11ll_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩ໙") in data:
          self.bstack11ll11lll1_opy_(data[bstack11ll_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࠪ໚")])
        if bstack11ll_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࠪ໛") in data:
          self.bstack11ll11ll1l_opy_(data[bstack11ll_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫໜ")])
    except:
      pass
  def bstack11ll11ll1l_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts[bstack11ll_opy_ (u"ࠫࡸࡩࡡ࡯ࠩໝ")]
      self.bstack1lll11l1ll_opy_ = scripts[bstack11ll_opy_ (u"ࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠩໞ")]
      self.bstack1l11ll1111_opy_ = scripts[bstack11ll_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࡖࡹࡲࡳࡡࡳࡻࠪໟ")]
      self.bstack11ll1l1111_opy_ = scripts[bstack11ll_opy_ (u"ࠧࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠬ໠")]
  def bstack11ll11lll1_opy_(self, bstack11l1ll1111_opy_):
    if bstack11l1ll1111_opy_ != None and len(bstack11l1ll1111_opy_) != 0:
      self.bstack11l1ll1111_opy_ = bstack11l1ll1111_opy_
  def store(self):
    try:
      with open(self.bstack11l1ll11ll_opy_, bstack11ll_opy_ (u"ࠨࡹࠪ໡")) as file:
        json.dump({
          bstack11ll_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡶࠦ໢"): self.bstack11l1ll1111_opy_,
          bstack11ll_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࡶࠦ໣"): {
            bstack11ll_opy_ (u"ࠦࡸࡩࡡ࡯ࠤ໤"): self.perform_scan,
            bstack11ll_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠤ໥"): self.bstack1lll11l1ll_opy_,
            bstack11ll_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࡖࡹࡲࡳࡡࡳࡻࠥ໦"): self.bstack1l11ll1111_opy_,
            bstack11ll_opy_ (u"ࠢࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠧ໧"): self.bstack11ll1l1111_opy_
          }
        }, file)
    except:
      pass
  def bstack111l1llll_opy_(self, bstack11l1ll11l1_opy_):
    try:
      return any(command.get(bstack11ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭໨")) == bstack11l1ll11l1_opy_ for command in self.bstack11l1ll1111_opy_)
    except:
      return False
bstack1l1l1l1ll_opy_ = bstack11l1ll111l_opy_()