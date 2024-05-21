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
import sys
import logging
import tarfile
import io
import os
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack11l1l11111_opy_
import tempfile
import json
bstack111l11lll1_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡩ࡫ࡢࡶࡩ࠱ࡰࡴ࡭ࠧፌ"))
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack11ll_opy_ (u"࠭࡜࡯ࠧࠫࡥࡸࡩࡴࡪ࡯ࡨ࠭ࡸ࡛ࠦࠦࠪࡱࡥࡲ࡫ࠩࡴ࡟࡞ࠩ࠭ࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠪࡵࡠࠤ࠲ࠦࠥࠩ࡯ࡨࡷࡸࡧࡧࡦࠫࡶࠫፍ"),
      datefmt=bstack11ll_opy_ (u"ࠧࠦࡊ࠽ࠩࡒࡀࠥࡔࠩፎ"),
      stream=sys.stdout
    )
  return logger
def bstack111l1l11ll_opy_():
  global bstack111l11lll1_opy_
  if os.path.exists(bstack111l11lll1_opy_):
    os.remove(bstack111l11lll1_opy_)
def bstack111l1l1l1_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack1111l1l1l_opy_(config, log_level):
  bstack111l11l11l_opy_ = log_level
  if bstack11ll_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪፏ") in config:
    bstack111l11l11l_opy_ = bstack11l1l11111_opy_[config[bstack11ll_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫፐ")]]
  if config.get(bstack11ll_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬፑ"), False):
    logging.getLogger().setLevel(bstack111l11l11l_opy_)
    return bstack111l11l11l_opy_
  global bstack111l11lll1_opy_
  bstack111l1l1l1_opy_()
  bstack111l1l11l1_opy_ = logging.Formatter(
    fmt=bstack11ll_opy_ (u"ࠫࡡࡴࠥࠩࡣࡶࡧࡹ࡯࡭ࡦࠫࡶࠤࡠࠫࠨ࡯ࡣࡰࡩ࠮ࡹ࡝࡜ࠧࠫࡰࡪࡼࡥ࡭ࡰࡤࡱࡪ࠯ࡳ࡞ࠢ࠰ࠤࠪ࠮࡭ࡦࡵࡶࡥ࡬࡫ࠩࡴࠩፒ"),
    datefmt=bstack11ll_opy_ (u"ࠬࠫࡈ࠻ࠧࡐ࠾࡙ࠪࠧፓ")
  )
  bstack111l11l1ll_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack111l11lll1_opy_)
  file_handler.setFormatter(bstack111l1l11l1_opy_)
  bstack111l11l1ll_opy_.setFormatter(bstack111l1l11l1_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack111l11l1ll_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack11ll_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠯ࡹࡨࡦࡩࡸࡩࡷࡧࡵ࠲ࡷ࡫࡭ࡰࡶࡨ࠲ࡷ࡫࡭ࡰࡶࡨࡣࡨࡵ࡮࡯ࡧࡦࡸ࡮ࡵ࡮ࠨፔ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack111l11l1ll_opy_.setLevel(bstack111l11l11l_opy_)
  logging.getLogger().addHandler(bstack111l11l1ll_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack111l11l11l_opy_
def bstack111l1l1l11_opy_(config):
  try:
    bstack111l111lll_opy_ = set([
      bstack11ll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩፕ"), bstack11ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫፖ"), bstack11ll_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬፗ"), bstack11ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧፘ"), bstack11ll_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸ࠭ፙ"),
      bstack11ll_opy_ (u"ࠬࡶࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨፚ"), bstack11ll_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡧࡳࡴࠩ፛"), bstack11ll_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨ፜"), bstack11ll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡧࡳࡴࠩ፝")
    ])
    bstack111l11l1l1_opy_ = bstack11ll_opy_ (u"ࠩࠪ፞")
    with open(bstack11ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭፟")) as bstack111l11l111_opy_:
      bstack111l11llll_opy_ = bstack111l11l111_opy_.read()
      bstack111l11l1l1_opy_ = re.sub(bstack11ll_opy_ (u"ࡶࠬࡤࠨ࡝ࡵ࠮࠭ࡄࠩ࠮ࠫࠦ࡟ࡲࠬ፠"), bstack11ll_opy_ (u"ࠬ࠭፡"), bstack111l11llll_opy_, flags=re.M)
      bstack111l11l1l1_opy_ = re.sub(
        bstack11ll_opy_ (u"ࡸࠧ࡟ࠪ࡟ࡷ࠰࠯࠿ࠩࠩ።") + bstack11ll_opy_ (u"ࠧࡽࠩ፣").join(bstack111l111lll_opy_) + bstack11ll_opy_ (u"ࠨࠫ࠱࠮ࠩ࠭፤"),
        bstack11ll_opy_ (u"ࡴࠪࡠ࠷ࡀࠠ࡜ࡔࡈࡈࡆࡉࡔࡆࡆࡠࠫ፥"),
        bstack111l11l1l1_opy_, flags=re.M | re.I
      )
    def bstack111l1l1111_opy_(dic):
      bstack111l1l111l_opy_ = {}
      for key, value in dic.items():
        if key in bstack111l111lll_opy_:
          bstack111l1l111l_opy_[key] = bstack11ll_opy_ (u"ࠪ࡟ࡗࡋࡄࡂࡅࡗࡉࡉࡣࠧ፦")
        else:
          if isinstance(value, dict):
            bstack111l1l111l_opy_[key] = bstack111l1l1111_opy_(value)
          else:
            bstack111l1l111l_opy_[key] = value
      return bstack111l1l111l_opy_
    bstack111l1l111l_opy_ = bstack111l1l1111_opy_(config)
    return {
      bstack11ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠧ፧"): bstack111l11l1l1_opy_,
      bstack11ll_opy_ (u"ࠬ࡬ࡩ࡯ࡣ࡯ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨ፨"): json.dumps(bstack111l1l111l_opy_)
    }
  except Exception as e:
    return {}
def bstack1l1ll11l_opy_(config):
  global bstack111l11lll1_opy_
  try:
    if config.get(bstack11ll_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨ፩"), False):
      return
    uuid = os.getenv(bstack11ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ፪"))
    if not uuid or uuid == bstack11ll_opy_ (u"ࠨࡰࡸࡰࡱ࠭፫"):
      return
    bstack111l11ll1l_opy_ = [bstack11ll_opy_ (u"ࠩࡵࡩࡶࡻࡩࡳࡧࡰࡩࡳࡺࡳ࠯ࡶࡻࡸࠬ፬"), bstack11ll_opy_ (u"ࠪࡔ࡮ࡶࡦࡪ࡮ࡨࠫ፭"), bstack11ll_opy_ (u"ࠫࡵࡿࡰࡳࡱ࡭ࡩࡨࡺ࠮ࡵࡱࡰࡰࠬ፮"), bstack111l11lll1_opy_]
    bstack111l1l1l1_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack11ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠲ࡲ࡯ࡨࡵ࠰ࠫ፯") + uuid + bstack11ll_opy_ (u"࠭࠮ࡵࡣࡵ࠲࡬ࢀࠧ፰"))
    with tarfile.open(output_file, bstack11ll_opy_ (u"ࠢࡸ࠼ࡪࡾࠧ፱")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack111l11ll1l_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack111l1l1l11_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack111l11ll11_opy_ = data.encode()
        tarinfo.size = len(bstack111l11ll11_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack111l11ll11_opy_))
    bstack1ll111llll_opy_ = MultipartEncoder(
      fields= {
        bstack11ll_opy_ (u"ࠨࡦࡤࡸࡦ࠭፲"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack11ll_opy_ (u"ࠩࡵࡦࠬ፳")), bstack11ll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰ࡺ࠰࡫ࡿ࡯ࡰࠨ፴")),
        bstack11ll_opy_ (u"ࠫࡨࡲࡩࡦࡰࡷࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭፵"): uuid
      }
    )
    response = requests.post(
      bstack11ll_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡵࡱ࡮ࡲࡥࡩ࠳࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡦࡰ࡮࡫࡮ࡵ࠯࡯ࡳ࡬ࡹ࠯ࡶࡲ࡯ࡳࡦࡪࠢ፶"),
      data=bstack1ll111llll_opy_,
      headers={bstack11ll_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬ፷"): bstack1ll111llll_opy_.content_type},
      auth=(config[bstack11ll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ፸")], config[bstack11ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ፹")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack11ll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡷࡳࡰࡴࡧࡤࠡ࡮ࡲ࡫ࡸࡀࠠࠨ፺") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack11ll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡩࡳࡪࡩ࡯ࡩࠣࡰࡴ࡭ࡳ࠻ࠩ፻") + str(e))
  finally:
    try:
      bstack111l1l11ll_opy_()
    except:
      pass