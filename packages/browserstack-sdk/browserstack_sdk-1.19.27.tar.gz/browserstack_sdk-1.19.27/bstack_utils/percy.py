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
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack1l111ll11_opy_, bstack1l11llll1_opy_
class bstack1l1111ll1_opy_:
  working_dir = os.getcwd()
  bstack111111l1_opy_ = False
  config = {}
  binary_path = bstack11ll_opy_ (u"ࠬ࠭Ꮓ")
  bstack11111lll11_opy_ = bstack11ll_opy_ (u"࠭ࠧᏄ")
  bstack1111l1lll_opy_ = False
  bstack11111ll1ll_opy_ = None
  bstack11111l1ll1_opy_ = {}
  bstack1111l1lll1_opy_ = 300
  bstack11111ll1l1_opy_ = False
  logger = None
  bstack1111l1l111_opy_ = False
  bstack1111ll1l1l_opy_ = bstack11ll_opy_ (u"ࠧࠨᏅ")
  bstack11111l1l1l_opy_ = {
    bstack11ll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨᏆ") : 1,
    bstack11ll_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࠪᏇ") : 2,
    bstack11ll_opy_ (u"ࠪࡩࡩ࡭ࡥࠨᏈ") : 3,
    bstack11ll_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫᏉ") : 4
  }
  def __init__(self) -> None: pass
  def bstack1111l111l1_opy_(self):
    bstack1111l1l1l1_opy_ = bstack11ll_opy_ (u"ࠬ࠭Ꮚ")
    bstack1111llll1l_opy_ = sys.platform
    bstack1111l1llll_opy_ = bstack11ll_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬᏋ")
    if re.match(bstack11ll_opy_ (u"ࠢࡥࡣࡵࡻ࡮ࡴࡼ࡮ࡣࡦࠤࡴࡹࠢᏌ"), bstack1111llll1l_opy_) != None:
      bstack1111l1l1l1_opy_ = bstack11l11lllll_opy_ + bstack11ll_opy_ (u"ࠣ࠱ࡳࡩࡷࡩࡹ࠮ࡱࡶࡼ࠳ࢀࡩࡱࠤᏍ")
      self.bstack1111ll1l1l_opy_ = bstack11ll_opy_ (u"ࠩࡰࡥࡨ࠭Ꮞ")
    elif re.match(bstack11ll_opy_ (u"ࠥࡱࡸࡽࡩ࡯ࡾࡰࡷࡾࡹࡼ࡮࡫ࡱ࡫ࡼࢂࡣࡺࡩࡺ࡭ࡳࢂࡢࡤࡥࡺ࡭ࡳࢂࡷࡪࡰࡦࡩࢁ࡫࡭ࡤࡾࡺ࡭ࡳ࠹࠲ࠣᏏ"), bstack1111llll1l_opy_) != None:
      bstack1111l1l1l1_opy_ = bstack11l11lllll_opy_ + bstack11ll_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠱ࡼ࡯࡮࠯ࡼ࡬ࡴࠧᏐ")
      bstack1111l1llll_opy_ = bstack11ll_opy_ (u"ࠧࡶࡥࡳࡥࡼ࠲ࡪࡾࡥࠣᏑ")
      self.bstack1111ll1l1l_opy_ = bstack11ll_opy_ (u"࠭ࡷࡪࡰࠪᏒ")
    else:
      bstack1111l1l1l1_opy_ = bstack11l11lllll_opy_ + bstack11ll_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠭࡭࡫ࡱࡹࡽ࠴ࡺࡪࡲࠥᏓ")
      self.bstack1111ll1l1l_opy_ = bstack11ll_opy_ (u"ࠨ࡮࡬ࡲࡺࡾࠧᏔ")
    return bstack1111l1l1l1_opy_, bstack1111l1llll_opy_
  def bstack111111lll1_opy_(self):
    try:
      bstack1111lll11l_opy_ = [os.path.join(expanduser(bstack11ll_opy_ (u"ࠤࢁࠦᏕ")), bstack11ll_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᏖ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1111lll11l_opy_:
        if(self.bstack11111l11l1_opy_(path)):
          return path
      raise bstack11ll_opy_ (u"࡚ࠦࡴࡡ࡭ࡤࡨࠤࡹࡵࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠣᏗ")
    except Exception as e:
      self.logger.error(bstack11ll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦࠢࡳࡥࡹ࡮ࠠࡧࡱࡵࠤࡵ࡫ࡲࡤࡻࠣࡨࡴࡽ࡮࡭ࡱࡤࡨ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࠰ࠤࢀࢃࠢᏘ").format(e))
  def bstack11111l11l1_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack1111l11ll1_opy_(self, bstack1111l1l1l1_opy_, bstack1111l1llll_opy_):
    try:
      bstack11111lll1l_opy_ = self.bstack111111lll1_opy_()
      bstack11111ll11l_opy_ = os.path.join(bstack11111lll1l_opy_, bstack11ll_opy_ (u"࠭ࡰࡦࡴࡦࡽ࠳ࢀࡩࡱࠩᏙ"))
      bstack1111ll11ll_opy_ = os.path.join(bstack11111lll1l_opy_, bstack1111l1llll_opy_)
      if os.path.exists(bstack1111ll11ll_opy_):
        self.logger.info(bstack11ll_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡦࡰࡷࡱࡨࠥ࡯࡮ࠡࡽࢀ࠰ࠥࡹ࡫ࡪࡲࡳ࡭ࡳ࡭ࠠࡥࡱࡺࡲࡱࡵࡡࡥࠤᏚ").format(bstack1111ll11ll_opy_))
        return bstack1111ll11ll_opy_
      if os.path.exists(bstack11111ll11l_opy_):
        self.logger.info(bstack11ll_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡻ࡫ࡳࠤ࡫ࡵࡵ࡯ࡦࠣ࡭ࡳࠦࡻࡾ࠮ࠣࡹࡳࢀࡩࡱࡲ࡬ࡲ࡬ࠨᏛ").format(bstack11111ll11l_opy_))
        return self.bstack1111llllll_opy_(bstack11111ll11l_opy_, bstack1111l1llll_opy_)
      self.logger.info(bstack11ll_opy_ (u"ࠤࡇࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡦࡳࡱࡰࠤࢀࢃࠢᏜ").format(bstack1111l1l1l1_opy_))
      response = bstack1l11llll1_opy_(bstack11ll_opy_ (u"ࠪࡋࡊ࡚ࠧᏝ"), bstack1111l1l1l1_opy_, {}, {})
      if response.status_code == 200:
        with open(bstack11111ll11l_opy_, bstack11ll_opy_ (u"ࠫࡼࡨࠧᏞ")) as file:
          file.write(response.content)
        self.logger.info(bstack11ll_opy_ (u"ࠧࡊ࡯ࡸࡰ࡯ࡳࡦࡪࡥࡥࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡣࡱࡨࠥࡹࡡࡷࡧࡧࠤࡦࡺࠠࡼࡿࠥᏟ").format(bstack11111ll11l_opy_))
        return self.bstack1111llllll_opy_(bstack11111ll11l_opy_, bstack1111l1llll_opy_)
      else:
        raise(bstack11ll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡹ࡮ࡥࠡࡨ࡬ࡰࡪ࠴ࠠࡔࡶࡤࡸࡺࡹࠠࡤࡱࡧࡩ࠿ࠦࡻࡾࠤᏠ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack11ll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼ࠾ࠥࢁࡽࠣᏡ").format(e))
  def bstack1111llll11_opy_(self, bstack1111l1l1l1_opy_, bstack1111l1llll_opy_):
    try:
      retry = 2
      bstack1111ll11ll_opy_ = None
      bstack1111l1ll11_opy_ = False
      while retry > 0:
        bstack1111ll11ll_opy_ = self.bstack1111l11ll1_opy_(bstack1111l1l1l1_opy_, bstack1111l1llll_opy_)
        bstack1111l1ll11_opy_ = self.bstack1111ll1ll1_opy_(bstack1111l1l1l1_opy_, bstack1111l1llll_opy_, bstack1111ll11ll_opy_)
        if bstack1111l1ll11_opy_:
          break
        retry -= 1
      return bstack1111ll11ll_opy_, bstack1111l1ll11_opy_
    except Exception as e:
      self.logger.error(bstack11ll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡬࡫ࡴࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡱࡣࡷ࡬ࠧᏢ").format(e))
    return bstack1111ll11ll_opy_, False
  def bstack1111ll1ll1_opy_(self, bstack1111l1l1l1_opy_, bstack1111l1llll_opy_, bstack1111ll11ll_opy_, bstack11111l11ll_opy_ = 0):
    if bstack11111l11ll_opy_ > 1:
      return False
    if bstack1111ll11ll_opy_ == None or os.path.exists(bstack1111ll11ll_opy_) == False:
      self.logger.warn(bstack11ll_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡲࡤࡸ࡭ࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥ࠮ࠣࡶࡪࡺࡲࡺ࡫ࡱ࡫ࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠢᏣ"))
      return False
    bstack11111llll1_opy_ = bstack11ll_opy_ (u"ࠥࡢ࠳࠰ࡀࡱࡧࡵࡧࡾࡢ࠯ࡤ࡮࡬ࠤࡡࡪ࠮࡝ࡦ࠮࠲ࡡࡪࠫࠣᏤ")
    command = bstack11ll_opy_ (u"ࠫࢀࢃࠠ࠮࠯ࡹࡩࡷࡹࡩࡰࡰࠪᏥ").format(bstack1111ll11ll_opy_)
    bstack1111lllll1_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack11111llll1_opy_, bstack1111lllll1_opy_) != None:
      return True
    else:
      self.logger.error(bstack11ll_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡩࡨࡦࡥ࡮ࠤ࡫ࡧࡩ࡭ࡧࡧࠦᏦ"))
      return False
  def bstack1111llllll_opy_(self, bstack11111ll11l_opy_, bstack1111l1llll_opy_):
    try:
      working_dir = os.path.dirname(bstack11111ll11l_opy_)
      shutil.unpack_archive(bstack11111ll11l_opy_, working_dir)
      bstack1111ll11ll_opy_ = os.path.join(working_dir, bstack1111l1llll_opy_)
      os.chmod(bstack1111ll11ll_opy_, 0o755)
      return bstack1111ll11ll_opy_
    except Exception as e:
      self.logger.error(bstack11ll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡸࡲࡿ࡯ࡰࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠢᏧ"))
  def bstack1111ll111l_opy_(self):
    try:
      percy = str(self.config.get(bstack11ll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭Ꮸ"), bstack11ll_opy_ (u"ࠣࡨࡤࡰࡸ࡫ࠢᏩ"))).lower()
      if percy != bstack11ll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᏪ"):
        return False
      self.bstack1111l1lll_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack11ll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡦࡶࡨࡧࡹࠦࡰࡦࡴࡦࡽ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧᏫ").format(e))
  def bstack1111ll1l11_opy_(self):
    try:
      bstack1111ll1l11_opy_ = str(self.config.get(bstack11ll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡆࡥࡵࡺࡵࡳࡧࡐࡳࡩ࡫ࠧᏬ"), bstack11ll_opy_ (u"ࠧࡧࡵࡵࡱࠥᏭ"))).lower()
      return bstack1111ll1l11_opy_
    except Exception as e:
      self.logger.error(bstack11ll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡩࡹ࡫ࡣࡵࠢࡳࡩࡷࡩࡹࠡࡥࡤࡴࡹࡻࡲࡦࠢࡰࡳࡩ࡫ࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᏮ").format(e))
  def init(self, bstack111111l1_opy_, config, logger):
    self.bstack111111l1_opy_ = bstack111111l1_opy_
    self.config = config
    self.logger = logger
    if not self.bstack1111ll111l_opy_():
      return
    self.bstack11111l1ll1_opy_ = config.get(bstack11ll_opy_ (u"ࠧࡱࡧࡵࡧࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭Ꮿ"), {})
    self.bstack1111l1111l_opy_ = config.get(bstack11ll_opy_ (u"ࠨࡲࡨࡶࡨࡿࡃࡢࡲࡷࡹࡷ࡫ࡍࡰࡦࡨࠫᏰ"), bstack11ll_opy_ (u"ࠤࡤࡹࡹࡵࠢᏱ"))
    try:
      bstack1111l1l1l1_opy_, bstack1111l1llll_opy_ = self.bstack1111l111l1_opy_()
      bstack1111ll11ll_opy_, bstack1111l1ll11_opy_ = self.bstack1111llll11_opy_(bstack1111l1l1l1_opy_, bstack1111l1llll_opy_)
      if bstack1111l1ll11_opy_:
        self.binary_path = bstack1111ll11ll_opy_
        thread = Thread(target=self.bstack11111l1l11_opy_)
        thread.start()
      else:
        self.bstack1111l1l111_opy_ = True
        self.logger.error(bstack11ll_opy_ (u"ࠥࡍࡳࡼࡡ࡭࡫ࡧࠤࡵ࡫ࡲࡤࡻࠣࡴࡦࡺࡨࠡࡨࡲࡹࡳࡪࠠ࠮ࠢࡾࢁ࠱ࠦࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡒࡨࡶࡨࡿࠢᏲ").format(bstack1111ll11ll_opy_))
    except Exception as e:
      self.logger.error(bstack11ll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡰࡦࡴࡦࡽ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧᏳ").format(e))
  def bstack111111ll1l_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack11ll_opy_ (u"ࠬࡲ࡯ࡨࠩᏴ"), bstack11ll_opy_ (u"࠭ࡰࡦࡴࡦࡽ࠳ࡲ࡯ࡨࠩᏵ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack11ll_opy_ (u"ࠢࡑࡷࡶ࡬࡮ࡴࡧࠡࡲࡨࡶࡨࡿࠠ࡭ࡱࡪࡷࠥࡧࡴࠡࡽࢀࠦ᏶").format(logfile))
      self.bstack11111lll11_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack11ll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸ࡫ࡴࠡࡲࡨࡶࡨࡿࠠ࡭ࡱࡪࠤࡵࡧࡴࡩ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤ᏷").format(e))
  def bstack11111l1l11_opy_(self):
    bstack1111l1l1ll_opy_ = self.bstack1111ll1lll_opy_()
    if bstack1111l1l1ll_opy_ == None:
      self.bstack1111l1l111_opy_ = True
      self.logger.error(bstack11ll_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡶࡲ࡯ࡪࡴࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦ࠯ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡰࡦࡴࡦࡽࠧᏸ"))
      return False
    command_args = [bstack11ll_opy_ (u"ࠥࡥࡵࡶ࠺ࡦࡺࡨࡧ࠿ࡹࡴࡢࡴࡷࠦᏹ") if self.bstack111111l1_opy_ else bstack11ll_opy_ (u"ࠫࡪࡾࡥࡤ࠼ࡶࡸࡦࡸࡴࠨᏺ")]
    bstack11111l111l_opy_ = self.bstack1111lll111_opy_()
    if bstack11111l111l_opy_ != None:
      command_args.append(bstack11ll_opy_ (u"ࠧ࠳ࡣࠡࡽࢀࠦᏻ").format(bstack11111l111l_opy_))
    env = os.environ.copy()
    env[bstack11ll_opy_ (u"ࠨࡐࡆࡔࡆ࡝ࡤ࡚ࡏࡌࡇࡑࠦᏼ")] = bstack1111l1l1ll_opy_
    bstack11111lllll_opy_ = [self.binary_path]
    self.bstack111111ll1l_opy_()
    self.bstack11111ll1ll_opy_ = self.bstack1111l11l1l_opy_(bstack11111lllll_opy_ + command_args, env)
    self.logger.debug(bstack11ll_opy_ (u"ࠢࡔࡶࡤࡶࡹ࡯࡮ࡨࠢࡋࡩࡦࡲࡴࡩࠢࡆ࡬ࡪࡩ࡫ࠣᏽ"))
    bstack11111l11ll_opy_ = 0
    while self.bstack11111ll1ll_opy_.poll() == None:
      bstack11111ll111_opy_ = self.bstack1111l1ll1l_opy_()
      if bstack11111ll111_opy_:
        self.logger.debug(bstack11ll_opy_ (u"ࠣࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠠࡴࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠦ᏾"))
        self.bstack11111ll1l1_opy_ = True
        return True
      bstack11111l11ll_opy_ += 1
      self.logger.debug(bstack11ll_opy_ (u"ࠤࡋࡩࡦࡲࡴࡩࠢࡆ࡬ࡪࡩ࡫ࠡࡔࡨࡸࡷࡿࠠ࠮ࠢࡾࢁࠧ᏿").format(bstack11111l11ll_opy_))
      time.sleep(2)
    self.logger.error(bstack11ll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠤࡋࡧࡩ࡭ࡧࡧࠤࡦ࡬ࡴࡦࡴࠣࡿࢂࠦࡡࡵࡶࡨࡱࡵࡺࡳࠣ᐀").format(bstack11111l11ll_opy_))
    self.bstack1111l1l111_opy_ = True
    return False
  def bstack1111l1ll1l_opy_(self, bstack11111l11ll_opy_ = 0):
    try:
      if bstack11111l11ll_opy_ > 10:
        return False
      bstack111111llll_opy_ = os.environ.get(bstack11ll_opy_ (u"ࠫࡕࡋࡒࡄ࡛ࡢࡗࡊࡘࡖࡆࡔࡢࡅࡉࡊࡒࡆࡕࡖࠫᐁ"), bstack11ll_opy_ (u"ࠬ࡮ࡴࡵࡲ࠽࠳࠴ࡲ࡯ࡤࡣ࡯࡬ࡴࡹࡴ࠻࠷࠶࠷࠽࠭ᐂ"))
      bstack1111l1l11l_opy_ = bstack111111llll_opy_ + bstack11l1l111l1_opy_
      response = requests.get(bstack1111l1l11l_opy_)
      return True if response.json() else False
    except:
      return False
  def bstack1111ll1lll_opy_(self):
    bstack1111l11l11_opy_ = bstack11ll_opy_ (u"࠭ࡡࡱࡲࠪᐃ") if self.bstack111111l1_opy_ else bstack11ll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩᐄ")
    bstack11l111l1ll_opy_ = bstack11ll_opy_ (u"ࠣࡣࡳ࡭࠴ࡧࡰࡱࡡࡳࡩࡷࡩࡹ࠰ࡩࡨࡸࡤࡶࡲࡰ࡬ࡨࡧࡹࡥࡴࡰ࡭ࡨࡲࡄࡴࡡ࡮ࡧࡀࡿࢂࠬࡴࡺࡲࡨࡁࢀࢃࠢᐅ").format(self.config[bstack11ll_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᐆ")], bstack1111l11l11_opy_)
    uri = bstack1l111ll11_opy_(bstack11l111l1ll_opy_)
    try:
      response = bstack1l11llll1_opy_(bstack11ll_opy_ (u"ࠪࡋࡊ࡚ࠧᐇ"), uri, {}, {bstack11ll_opy_ (u"ࠫࡦࡻࡴࡩࠩᐈ"): (self.config[bstack11ll_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧᐉ")], self.config[bstack11ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩᐊ")])})
      if response.status_code == 200:
        bstack1111lll1l1_opy_ = response.json()
        if bstack11ll_opy_ (u"ࠢࡵࡱ࡮ࡩࡳࠨᐋ") in bstack1111lll1l1_opy_:
          return bstack1111lll1l1_opy_[bstack11ll_opy_ (u"ࠣࡶࡲ࡯ࡪࡴࠢᐌ")]
        else:
          raise bstack11ll_opy_ (u"ࠩࡗࡳࡰ࡫࡮ࠡࡐࡲࡸࠥࡌ࡯ࡶࡰࡧࠤ࠲ࠦࡻࡾࠩᐍ").format(bstack1111lll1l1_opy_)
      else:
        raise bstack11ll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡶࡥࡳࡥࡼࠤࡹࡵ࡫ࡦࡰ࠯ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࠦࡳࡵࡣࡷࡹࡸࠦ࠭ࠡࡽࢀ࠰ࠥࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡃࡱࡧࡽࠥ࠳ࠠࡼࡿࠥᐎ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack11ll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡶࡥࡳࡥࡼࠤࡵࡸ࡯࡫ࡧࡦࡸࠧᐏ").format(e))
  def bstack1111lll111_opy_(self):
    bstack1111l11lll_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll_opy_ (u"ࠧࡶࡥࡳࡥࡼࡇࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠣᐐ"))
    try:
      if bstack11ll_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧᐑ") not in self.bstack11111l1ll1_opy_:
        self.bstack11111l1ll1_opy_[bstack11ll_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨᐒ")] = 2
      with open(bstack1111l11lll_opy_, bstack11ll_opy_ (u"ࠨࡹࠪᐓ")) as fp:
        json.dump(self.bstack11111l1ll1_opy_, fp)
      return bstack1111l11lll_opy_
    except Exception as e:
      self.logger.error(bstack11ll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡩࡲࡦࡣࡷࡩࠥࡶࡥࡳࡥࡼࠤࡨࡵ࡮ࡧ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᐔ").format(e))
  def bstack1111l11l1l_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack1111ll1l1l_opy_ == bstack11ll_opy_ (u"ࠪࡻ࡮ࡴࠧᐕ"):
        bstack1111l111ll_opy_ = [bstack11ll_opy_ (u"ࠫࡨࡳࡤ࠯ࡧࡻࡩࠬᐖ"), bstack11ll_opy_ (u"ࠬ࠵ࡣࠨᐗ")]
        cmd = bstack1111l111ll_opy_ + cmd
      cmd = bstack11ll_opy_ (u"࠭ࠠࠨᐘ").join(cmd)
      self.logger.debug(bstack11ll_opy_ (u"ࠢࡓࡷࡱࡲ࡮ࡴࡧࠡࡽࢀࠦᐙ").format(cmd))
      with open(self.bstack11111lll11_opy_, bstack11ll_opy_ (u"ࠣࡣࠥᐚ")) as bstack1111ll1111_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1111ll1111_opy_, text=True, stderr=bstack1111ll1111_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1111l1l111_opy_ = True
      self.logger.error(bstack11ll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻࠣࡻ࡮ࡺࡨࠡࡥࡰࡨࠥ࠳ࠠࡼࡿ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠦᐛ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack11111ll1l1_opy_:
        self.logger.info(bstack11ll_opy_ (u"ࠥࡗࡹࡵࡰࡱ࡫ࡱ࡫ࠥࡖࡥࡳࡥࡼࠦᐜ"))
        cmd = [self.binary_path, bstack11ll_opy_ (u"ࠦࡪࡾࡥࡤ࠼ࡶࡸࡴࡶࠢᐝ")]
        self.bstack1111l11l1l_opy_(cmd)
        self.bstack11111ll1l1_opy_ = False
    except Exception as e:
      self.logger.error(bstack11ll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡳࡵࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡸ࡫ࡷ࡬ࠥࡩ࡯࡮࡯ࡤࡲࡩࠦ࠭ࠡࡽࢀ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧᐞ").format(cmd, e))
  def bstack111l11l1_opy_(self):
    if not self.bstack1111l1lll_opy_:
      return
    try:
      bstack11111l1111_opy_ = 0
      while not self.bstack11111ll1l1_opy_ and bstack11111l1111_opy_ < self.bstack1111l1lll1_opy_:
        if self.bstack1111l1l111_opy_:
          self.logger.info(bstack11ll_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡹࡥࡵࡷࡳࠤ࡫ࡧࡩ࡭ࡧࡧࠦᐟ"))
          return
        time.sleep(1)
        bstack11111l1111_opy_ += 1
      os.environ[bstack11ll_opy_ (u"ࠧࡑࡇࡕࡇ࡞ࡥࡂࡆࡕࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒ࠭ᐠ")] = str(self.bstack1111lll1ll_opy_())
      self.logger.info(bstack11ll_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡴࡧࡷࡹࡵࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࡥࠤᐡ"))
    except Exception as e:
      self.logger.error(bstack11ll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡥࡵࡷࡳࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥᐢ").format(e))
  def bstack1111lll1ll_opy_(self):
    if self.bstack111111l1_opy_:
      return
    try:
      bstack1111l11111_opy_ = [platform[bstack11ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᐣ")].lower() for platform in self.config.get(bstack11ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᐤ"), [])]
      bstack1111ll11l1_opy_ = sys.maxsize
      bstack11111l1lll_opy_ = bstack11ll_opy_ (u"ࠬ࠭ᐥ")
      for browser in bstack1111l11111_opy_:
        if browser in self.bstack11111l1l1l_opy_:
          bstack111l111111_opy_ = self.bstack11111l1l1l_opy_[browser]
        if bstack111l111111_opy_ < bstack1111ll11l1_opy_:
          bstack1111ll11l1_opy_ = bstack111l111111_opy_
          bstack11111l1lll_opy_ = browser
      return bstack11111l1lll_opy_
    except Exception as e:
      self.logger.error(bstack11ll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡣࡧࡶࡸࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᐦ").format(e))