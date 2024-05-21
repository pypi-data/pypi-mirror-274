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
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
from urllib.parse import urlparse
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import bstack11l1l11lll_opy_, bstack1lllll1ll_opy_, bstack1l1llll1l_opy_, bstack1lll1lll1_opy_
from bstack_utils.messages import bstack111ll1l11_opy_, bstack1ll1llll1_opy_
from bstack_utils.proxy import bstack11ll11l11_opy_, bstack1ll111lll1_opy_
bstack11llll1l_opy_ = Config.bstack11l1l11l1_opy_()
def bstack11l1ll1ll1_opy_(config):
    return config[bstack11ll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩᆇ")]
def bstack11ll111111_opy_(config):
    return config[bstack11ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫᆈ")]
def bstack11lll1l11_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack111lll1ll1_opy_(obj):
    values = []
    bstack111ll11ll1_opy_ = re.compile(bstack11ll_opy_ (u"ࡴࠥࡢࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࡞ࡧ࠯ࠩࠨᆉ"), re.I)
    for key in obj.keys():
        if bstack111ll11ll1_opy_.match(key):
            values.append(obj[key])
    return values
def bstack111lll1l1l_opy_(config):
    tags = []
    tags.extend(bstack111lll1ll1_opy_(os.environ))
    tags.extend(bstack111lll1ll1_opy_(config))
    return tags
def bstack11l11l1lll_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11l1111l11_opy_(bstack11l11111l1_opy_):
    if not bstack11l11111l1_opy_:
        return bstack11ll_opy_ (u"ࠪࠫᆊ")
    return bstack11ll_opy_ (u"ࠦࢀࢃࠠࠩࡽࢀ࠭ࠧᆋ").format(bstack11l11111l1_opy_.name, bstack11l11111l1_opy_.email)
def bstack11l1lll1l1_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack111lllll1l_opy_ = repo.common_dir
        info = {
            bstack11ll_opy_ (u"ࠧࡹࡨࡢࠤᆌ"): repo.head.commit.hexsha,
            bstack11ll_opy_ (u"ࠨࡳࡩࡱࡵࡸࡤࡹࡨࡢࠤᆍ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack11ll_opy_ (u"ࠢࡣࡴࡤࡲࡨ࡮ࠢᆎ"): repo.active_branch.name,
            bstack11ll_opy_ (u"ࠣࡶࡤ࡫ࠧᆏ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack11ll_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡶࡨࡶࠧᆐ"): bstack11l1111l11_opy_(repo.head.commit.committer),
            bstack11ll_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡷࡩࡷࡥࡤࡢࡶࡨࠦᆑ"): repo.head.commit.committed_datetime.isoformat(),
            bstack11ll_opy_ (u"ࠦࡦࡻࡴࡩࡱࡵࠦᆒ"): bstack11l1111l11_opy_(repo.head.commit.author),
            bstack11ll_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࡤࡪࡡࡵࡧࠥᆓ"): repo.head.commit.authored_datetime.isoformat(),
            bstack11ll_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢᆔ"): repo.head.commit.message,
            bstack11ll_opy_ (u"ࠢࡳࡱࡲࡸࠧᆕ"): repo.git.rev_parse(bstack11ll_opy_ (u"ࠣ࠯࠰ࡷ࡭ࡵࡷ࠮ࡶࡲࡴࡱ࡫ࡶࡦ࡮ࠥᆖ")),
            bstack11ll_opy_ (u"ࠤࡦࡳࡲࡳ࡯࡯ࡡࡪ࡭ࡹࡥࡤࡪࡴࠥᆗ"): bstack111lllll1l_opy_,
            bstack11ll_opy_ (u"ࠥࡻࡴࡸ࡫ࡵࡴࡨࡩࡤ࡭ࡩࡵࡡࡧ࡭ࡷࠨᆘ"): subprocess.check_output([bstack11ll_opy_ (u"ࠦ࡬࡯ࡴࠣᆙ"), bstack11ll_opy_ (u"ࠧࡸࡥࡷ࠯ࡳࡥࡷࡹࡥࠣᆚ"), bstack11ll_opy_ (u"ࠨ࠭࠮ࡩ࡬ࡸ࠲ࡩ࡯࡮࡯ࡲࡲ࠲ࡪࡩࡳࠤᆛ")]).strip().decode(
                bstack11ll_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ᆜ")),
            bstack11ll_opy_ (u"ࠣ࡮ࡤࡷࡹࡥࡴࡢࡩࠥᆝ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack11ll_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡵࡢࡷ࡮ࡴࡣࡦࡡ࡯ࡥࡸࡺ࡟ࡵࡣࡪࠦᆞ"): repo.git.rev_list(
                bstack11ll_opy_ (u"ࠥࡿࢂ࠴࠮ࡼࡿࠥᆟ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack111ll1llll_opy_ = []
        for remote in remotes:
            bstack111lllllll_opy_ = {
                bstack11ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᆠ"): remote.name,
                bstack11ll_opy_ (u"ࠧࡻࡲ࡭ࠤᆡ"): remote.url,
            }
            bstack111ll1llll_opy_.append(bstack111lllllll_opy_)
        return {
            bstack11ll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᆢ"): bstack11ll_opy_ (u"ࠢࡨ࡫ࡷࠦᆣ"),
            **info,
            bstack11ll_opy_ (u"ࠣࡴࡨࡱࡴࡺࡥࡴࠤᆤ"): bstack111ll1llll_opy_
        }
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack11ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡲࡴࡺࡲࡡࡵ࡫ࡱ࡫ࠥࡍࡩࡵࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧᆥ").format(err))
        return {}
def bstack1ll1111l11_opy_():
    env = os.environ
    if (bstack11ll_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣ࡚ࡘࡌࠣᆦ") in env and len(env[bstack11ll_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤ࡛ࡒࡍࠤᆧ")]) > 0) or (
            bstack11ll_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡈࡐࡏࡈࠦᆨ") in env and len(env[bstack11ll_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡉࡑࡐࡉࠧᆩ")]) > 0):
        return {
            bstack11ll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᆪ"): bstack11ll_opy_ (u"ࠣࡌࡨࡲࡰ࡯࡮ࡴࠤᆫ"),
            bstack11ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᆬ"): env.get(bstack11ll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨᆭ")),
            bstack11ll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᆮ"): env.get(bstack11ll_opy_ (u"ࠧࡐࡏࡃࡡࡑࡅࡒࡋࠢᆯ")),
            bstack11ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᆰ"): env.get(bstack11ll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᆱ"))
        }
    if env.get(bstack11ll_opy_ (u"ࠣࡅࡌࠦᆲ")) == bstack11ll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᆳ") and bstack111llll1_opy_(env.get(bstack11ll_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡆࡍࠧᆴ"))):
        return {
            bstack11ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᆵ"): bstack11ll_opy_ (u"ࠧࡉࡩࡳࡥ࡯ࡩࡈࡏࠢᆶ"),
            bstack11ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᆷ"): env.get(bstack11ll_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥᆸ")),
            bstack11ll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᆹ"): env.get(bstack11ll_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡡࡍࡓࡇࠨᆺ")),
            bstack11ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᆻ"): env.get(bstack11ll_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࠢᆼ"))
        }
    if env.get(bstack11ll_opy_ (u"ࠧࡉࡉࠣᆽ")) == bstack11ll_opy_ (u"ࠨࡴࡳࡷࡨࠦᆾ") and bstack111llll1_opy_(env.get(bstack11ll_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙ࠢᆿ"))):
        return {
            bstack11ll_opy_ (u"ࠣࡰࡤࡱࡪࠨᇀ"): bstack11ll_opy_ (u"ࠤࡗࡶࡦࡼࡩࡴࠢࡆࡍࠧᇁ"),
            bstack11ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᇂ"): env.get(bstack11ll_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡇ࡛ࡉࡍࡆࡢ࡛ࡊࡈ࡟ࡖࡔࡏࠦᇃ")),
            bstack11ll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᇄ"): env.get(bstack11ll_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᇅ")),
            bstack11ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᇆ"): env.get(bstack11ll_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᇇ"))
        }
    if env.get(bstack11ll_opy_ (u"ࠤࡆࡍࠧᇈ")) == bstack11ll_opy_ (u"ࠥࡸࡷࡻࡥࠣᇉ") and env.get(bstack11ll_opy_ (u"ࠦࡈࡏ࡟ࡏࡃࡐࡉࠧᇊ")) == bstack11ll_opy_ (u"ࠧࡩ࡯ࡥࡧࡶ࡬࡮ࡶࠢᇋ"):
        return {
            bstack11ll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᇌ"): bstack11ll_opy_ (u"ࠢࡄࡱࡧࡩࡸ࡮ࡩࡱࠤᇍ"),
            bstack11ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᇎ"): None,
            bstack11ll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᇏ"): None,
            bstack11ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᇐ"): None
        }
    if env.get(bstack11ll_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡃࡔࡄࡒࡈࡎࠢᇑ")) and env.get(bstack11ll_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡅࡒࡑࡒࡏࡔࠣᇒ")):
        return {
            bstack11ll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᇓ"): bstack11ll_opy_ (u"ࠢࡃ࡫ࡷࡦࡺࡩ࡫ࡦࡶࠥᇔ"),
            bstack11ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᇕ"): env.get(bstack11ll_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡍࡉࡕࡡࡋࡘ࡙ࡖ࡟ࡐࡔࡌࡋࡎࡔࠢᇖ")),
            bstack11ll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᇗ"): None,
            bstack11ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᇘ"): env.get(bstack11ll_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᇙ"))
        }
    if env.get(bstack11ll_opy_ (u"ࠨࡃࡊࠤᇚ")) == bstack11ll_opy_ (u"ࠢࡵࡴࡸࡩࠧᇛ") and bstack111llll1_opy_(env.get(bstack11ll_opy_ (u"ࠣࡆࡕࡓࡓࡋࠢᇜ"))):
        return {
            bstack11ll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᇝ"): bstack11ll_opy_ (u"ࠥࡈࡷࡵ࡮ࡦࠤᇞ"),
            bstack11ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᇟ"): env.get(bstack11ll_opy_ (u"ࠧࡊࡒࡐࡐࡈࡣࡇ࡛ࡉࡍࡆࡢࡐࡎࡔࡋࠣᇠ")),
            bstack11ll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᇡ"): None,
            bstack11ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᇢ"): env.get(bstack11ll_opy_ (u"ࠣࡆࡕࡓࡓࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᇣ"))
        }
    if env.get(bstack11ll_opy_ (u"ࠤࡆࡍࠧᇤ")) == bstack11ll_opy_ (u"ࠥࡸࡷࡻࡥࠣᇥ") and bstack111llll1_opy_(env.get(bstack11ll_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋࠢᇦ"))):
        return {
            bstack11ll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᇧ"): bstack11ll_opy_ (u"ࠨࡓࡦ࡯ࡤࡴ࡭ࡵࡲࡦࠤᇨ"),
            bstack11ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᇩ"): env.get(bstack11ll_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡔࡘࡇࡂࡐࡌ࡞ࡆ࡚ࡉࡐࡐࡢ࡙ࡗࡒࠢᇪ")),
            bstack11ll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᇫ"): env.get(bstack11ll_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᇬ")),
            bstack11ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᇭ"): env.get(bstack11ll_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡌࡒࡆࡤࡏࡄࠣᇮ"))
        }
    if env.get(bstack11ll_opy_ (u"ࠨࡃࡊࠤᇯ")) == bstack11ll_opy_ (u"ࠢࡵࡴࡸࡩࠧᇰ") and bstack111llll1_opy_(env.get(bstack11ll_opy_ (u"ࠣࡉࡌࡘࡑࡇࡂࡠࡅࡌࠦᇱ"))):
        return {
            bstack11ll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᇲ"): bstack11ll_opy_ (u"ࠥࡋ࡮ࡺࡌࡢࡤࠥᇳ"),
            bstack11ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᇴ"): env.get(bstack11ll_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤ࡛ࡒࡍࠤᇵ")),
            bstack11ll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᇶ"): env.get(bstack11ll_opy_ (u"ࠢࡄࡋࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᇷ")),
            bstack11ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᇸ"): env.get(bstack11ll_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡌࡈࠧᇹ"))
        }
    if env.get(bstack11ll_opy_ (u"ࠥࡇࡎࠨᇺ")) == bstack11ll_opy_ (u"ࠦࡹࡸࡵࡦࠤᇻ") and bstack111llll1_opy_(env.get(bstack11ll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࠣᇼ"))):
        return {
            bstack11ll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᇽ"): bstack11ll_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡱࡩࡵࡧࠥᇾ"),
            bstack11ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᇿ"): env.get(bstack11ll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣሀ")),
            bstack11ll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧሁ"): env.get(bstack11ll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡍࡃࡅࡉࡑࠨሂ")) or env.get(bstack11ll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡒࡆࡓࡅࠣሃ")),
            bstack11ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧሄ"): env.get(bstack11ll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤህ"))
        }
    if bstack111llll1_opy_(env.get(bstack11ll_opy_ (u"ࠣࡖࡉࡣࡇ࡛ࡉࡍࡆࠥሆ"))):
        return {
            bstack11ll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢሇ"): bstack11ll_opy_ (u"࡚ࠥ࡮ࡹࡵࡢ࡮ࠣࡗࡹࡻࡤࡪࡱࠣࡘࡪࡧ࡭ࠡࡕࡨࡶࡻ࡯ࡣࡦࡵࠥለ"),
            bstack11ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢሉ"): bstack11ll_opy_ (u"ࠧࢁࡽࡼࡿࠥሊ").format(env.get(bstack11ll_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡊࡔ࡛ࡎࡅࡃࡗࡍࡔࡔࡓࡆࡔ࡙ࡉࡗ࡛ࡒࡊࠩላ")), env.get(bstack11ll_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡕࡘࡏࡋࡇࡆࡘࡎࡊࠧሌ"))),
            bstack11ll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥል"): env.get(bstack11ll_opy_ (u"ࠤࡖ࡝ࡘ࡚ࡅࡎࡡࡇࡉࡋࡏࡎࡊࡖࡌࡓࡓࡏࡄࠣሎ")),
            bstack11ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤሏ"): env.get(bstack11ll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦሐ"))
        }
    if bstack111llll1_opy_(env.get(bstack11ll_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘࠢሑ"))):
        return {
            bstack11ll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦሒ"): bstack11ll_opy_ (u"ࠢࡂࡲࡳࡺࡪࡿ࡯ࡳࠤሓ"),
            bstack11ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦሔ"): bstack11ll_opy_ (u"ࠤࡾࢁ࠴ࡶࡲࡰ࡬ࡨࡧࡹ࠵ࡻࡾ࠱ࡾࢁ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽࠣሕ").format(env.get(bstack11ll_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤ࡛ࡒࡍࠩሖ")), env.get(bstack11ll_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡁࡄࡅࡒ࡙ࡓ࡚࡟ࡏࡃࡐࡉࠬሗ")), env.get(bstack11ll_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡕࡏ࡙ࡌ࠭መ")), env.get(bstack11ll_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪሙ"))),
            bstack11ll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤሚ"): env.get(bstack11ll_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧማ")),
            bstack11ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣሜ"): env.get(bstack11ll_opy_ (u"ࠥࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦም"))
        }
    if env.get(bstack11ll_opy_ (u"ࠦࡆࡠࡕࡓࡇࡢࡌ࡙࡚ࡐࡠࡗࡖࡉࡗࡥࡁࡈࡇࡑࡘࠧሞ")) and env.get(bstack11ll_opy_ (u"࡚ࠧࡆࡠࡄࡘࡍࡑࡊࠢሟ")):
        return {
            bstack11ll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦሠ"): bstack11ll_opy_ (u"ࠢࡂࡼࡸࡶࡪࠦࡃࡊࠤሡ"),
            bstack11ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦሢ"): bstack11ll_opy_ (u"ࠤࡾࢁࢀࢃ࠯ࡠࡤࡸ࡭ࡱࡪ࠯ࡳࡧࡶࡹࡱࡺࡳࡀࡤࡸ࡭ࡱࡪࡉࡥ࠿ࡾࢁࠧሣ").format(env.get(bstack11ll_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡇࡑࡘࡒࡉࡇࡔࡊࡑࡑࡗࡊࡘࡖࡆࡔࡘࡖࡎ࠭ሤ")), env.get(bstack11ll_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡒࡕࡓࡏࡋࡃࡕࠩሥ")), env.get(bstack11ll_opy_ (u"ࠬࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠬሦ"))),
            bstack11ll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣሧ"): env.get(bstack11ll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢረ")),
            bstack11ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢሩ"): env.get(bstack11ll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠤሪ"))
        }
    if any([env.get(bstack11ll_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣራ")), env.get(bstack11ll_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡓࡇࡖࡓࡑ࡜ࡅࡅࡡࡖࡓ࡚ࡘࡃࡆࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥሬ")), env.get(bstack11ll_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡕࡒ࡙ࡗࡉࡅࡠࡘࡈࡖࡘࡏࡏࡏࠤር"))]):
        return {
            bstack11ll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦሮ"): bstack11ll_opy_ (u"ࠢࡂ࡙ࡖࠤࡈࡵࡤࡦࡄࡸ࡭ࡱࡪࠢሯ"),
            bstack11ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦሰ"): env.get(bstack11ll_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡖࡕࡃࡎࡌࡇࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣሱ")),
            bstack11ll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧሲ"): env.get(bstack11ll_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤሳ")),
            bstack11ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦሴ"): env.get(bstack11ll_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦስ"))
        }
    if env.get(bstack11ll_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡣࡷ࡬ࡰࡩࡔࡵ࡮ࡤࡨࡶࠧሶ")):
        return {
            bstack11ll_opy_ (u"ࠣࡰࡤࡱࡪࠨሷ"): bstack11ll_opy_ (u"ࠤࡅࡥࡲࡨ࡯ࡰࠤሸ"),
            bstack11ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨሹ"): env.get(bstack11ll_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡕࡩࡸࡻ࡬ࡵࡵࡘࡶࡱࠨሺ")),
            bstack11ll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢሻ"): env.get(bstack11ll_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡳࡩࡱࡵࡸࡏࡵࡢࡏࡣࡰࡩࠧሼ")),
            bstack11ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨሽ"): env.get(bstack11ll_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡎࡶ࡯ࡥࡩࡷࠨሾ"))
        }
    if env.get(bstack11ll_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࠥሿ")) or env.get(bstack11ll_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡒࡇࡉࡏࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡘ࡚ࡁࡓࡖࡈࡈࠧቀ")):
        return {
            bstack11ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤቁ"): bstack11ll_opy_ (u"ࠧ࡝ࡥࡳࡥ࡮ࡩࡷࠨቂ"),
            bstack11ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤቃ"): env.get(bstack11ll_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦቄ")),
            bstack11ll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥቅ"): bstack11ll_opy_ (u"ࠤࡐࡥ࡮ࡴࠠࡑ࡫ࡳࡩࡱ࡯࡮ࡦࠤቆ") if env.get(bstack11ll_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡒࡇࡉࡏࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡘ࡚ࡁࡓࡖࡈࡈࠧቇ")) else None,
            bstack11ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥቈ"): env.get(bstack11ll_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡇࡊࡖࡢࡇࡔࡓࡍࡊࡖࠥ቉"))
        }
    if any([env.get(bstack11ll_opy_ (u"ࠨࡇࡄࡒࡢࡔࡗࡕࡊࡆࡅࡗࠦቊ")), env.get(bstack11ll_opy_ (u"ࠢࡈࡅࡏࡓ࡚ࡊ࡟ࡑࡔࡒࡎࡊࡉࡔࠣቋ")), env.get(bstack11ll_opy_ (u"ࠣࡉࡒࡓࡌࡒࡅࡠࡅࡏࡓ࡚ࡊ࡟ࡑࡔࡒࡎࡊࡉࡔࠣቌ"))]):
        return {
            bstack11ll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢቍ"): bstack11ll_opy_ (u"ࠥࡋࡴࡵࡧ࡭ࡧࠣࡇࡱࡵࡵࡥࠤ቎"),
            bstack11ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ቏"): None,
            bstack11ll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢቐ"): env.get(bstack11ll_opy_ (u"ࠨࡐࡓࡑࡍࡉࡈ࡚࡟ࡊࡆࠥቑ")),
            bstack11ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨቒ"): env.get(bstack11ll_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥቓ"))
        }
    if env.get(bstack11ll_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࠧቔ")):
        return {
            bstack11ll_opy_ (u"ࠥࡲࡦࡳࡥࠣቕ"): bstack11ll_opy_ (u"ࠦࡘ࡮ࡩࡱࡲࡤࡦࡱ࡫ࠢቖ"),
            bstack11ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ቗"): env.get(bstack11ll_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧቘ")),
            bstack11ll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ቙"): bstack11ll_opy_ (u"ࠣࡌࡲࡦࠥࠩࡻࡾࠤቚ").format(env.get(bstack11ll_opy_ (u"ࠩࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡐࡏࡃࡡࡌࡈࠬቛ"))) if env.get(bstack11ll_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡊࡐࡄࡢࡍࡉࠨቜ")) else None,
            bstack11ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥቝ"): env.get(bstack11ll_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢ቞"))
        }
    if bstack111llll1_opy_(env.get(bstack11ll_opy_ (u"ࠨࡎࡆࡖࡏࡍࡋ࡟ࠢ቟"))):
        return {
            bstack11ll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧበ"): bstack11ll_opy_ (u"ࠣࡐࡨࡸࡱ࡯ࡦࡺࠤቡ"),
            bstack11ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧቢ"): env.get(bstack11ll_opy_ (u"ࠥࡈࡊࡖࡌࡐ࡛ࡢ࡙ࡗࡒࠢባ")),
            bstack11ll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨቤ"): env.get(bstack11ll_opy_ (u"࡙ࠧࡉࡕࡇࡢࡒࡆࡓࡅࠣብ")),
            bstack11ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧቦ"): env.get(bstack11ll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡉࡅࠤቧ"))
        }
    if bstack111llll1_opy_(env.get(bstack11ll_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠࡃࡆࡘࡎࡕࡎࡔࠤቨ"))):
        return {
            bstack11ll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢቩ"): bstack11ll_opy_ (u"ࠥࡋ࡮ࡺࡈࡶࡤࠣࡅࡨࡺࡩࡰࡰࡶࠦቪ"),
            bstack11ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢቫ"): bstack11ll_opy_ (u"ࠧࢁࡽ࠰ࡽࢀ࠳ࡦࡩࡴࡪࡱࡱࡷ࠴ࡸࡵ࡯ࡵ࠲ࡿࢂࠨቬ").format(env.get(bstack11ll_opy_ (u"࠭ࡇࡊࡖࡋ࡙ࡇࡥࡓࡆࡔ࡙ࡉࡗࡥࡕࡓࡎࠪቭ")), env.get(bstack11ll_opy_ (u"ࠧࡈࡋࡗࡌ࡚ࡈ࡟ࡓࡇࡓࡓࡘࡏࡔࡐࡔ࡜ࠫቮ")), env.get(bstack11ll_opy_ (u"ࠨࡉࡌࡘࡍ࡛ࡂࡠࡔࡘࡒࡤࡏࡄࠨቯ"))),
            bstack11ll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦተ"): env.get(bstack11ll_opy_ (u"ࠥࡋࡎ࡚ࡈࡖࡄࡢ࡛ࡔࡘࡋࡇࡎࡒ࡛ࠧቱ")),
            bstack11ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥቲ"): env.get(bstack11ll_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤࡘࡕࡏࡡࡌࡈࠧታ"))
        }
    if env.get(bstack11ll_opy_ (u"ࠨࡃࡊࠤቴ")) == bstack11ll_opy_ (u"ࠢࡵࡴࡸࡩࠧት") and env.get(bstack11ll_opy_ (u"ࠣࡘࡈࡖࡈࡋࡌࠣቶ")) == bstack11ll_opy_ (u"ࠤ࠴ࠦቷ"):
        return {
            bstack11ll_opy_ (u"ࠥࡲࡦࡳࡥࠣቸ"): bstack11ll_opy_ (u"࡛ࠦ࡫ࡲࡤࡧ࡯ࠦቹ"),
            bstack11ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣቺ"): bstack11ll_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࡻࡾࠤቻ").format(env.get(bstack11ll_opy_ (u"ࠧࡗࡇࡕࡇࡊࡒ࡟ࡖࡔࡏࠫቼ"))),
            bstack11ll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥች"): None,
            bstack11ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣቾ"): None,
        }
    if env.get(bstack11ll_opy_ (u"ࠥࡘࡊࡇࡍࡄࡋࡗ࡝ࡤ࡜ࡅࡓࡕࡌࡓࡓࠨቿ")):
        return {
            bstack11ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤኀ"): bstack11ll_opy_ (u"࡚ࠧࡥࡢ࡯ࡦ࡭ࡹࡿࠢኁ"),
            bstack11ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤኂ"): None,
            bstack11ll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤኃ"): env.get(bstack11ll_opy_ (u"ࠣࡖࡈࡅࡒࡉࡉࡕ࡛ࡢࡔࡗࡕࡊࡆࡅࡗࡣࡓࡇࡍࡆࠤኄ")),
            bstack11ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣኅ"): env.get(bstack11ll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤኆ"))
        }
    if any([env.get(bstack11ll_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋࠢኇ")), env.get(bstack11ll_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࡠࡗࡕࡐࠧኈ")), env.get(bstack11ll_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࡡࡘࡗࡊࡘࡎࡂࡏࡈࠦ኉")), env.get(bstack11ll_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࡢࡘࡊࡇࡍࠣኊ"))]):
        return {
            bstack11ll_opy_ (u"ࠣࡰࡤࡱࡪࠨኋ"): bstack11ll_opy_ (u"ࠤࡆࡳࡳࡩ࡯ࡶࡴࡶࡩࠧኌ"),
            bstack11ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨኍ"): None,
            bstack11ll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ኎"): env.get(bstack11ll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨ኏")) or None,
            bstack11ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧነ"): env.get(bstack11ll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡉࡅࠤኑ"), 0)
        }
    if env.get(bstack11ll_opy_ (u"ࠣࡉࡒࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨኒ")):
        return {
            bstack11ll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢና"): bstack11ll_opy_ (u"ࠥࡋࡴࡉࡄࠣኔ"),
            bstack11ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢን"): None,
            bstack11ll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢኖ"): env.get(bstack11ll_opy_ (u"ࠨࡇࡐࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦኗ")),
            bstack11ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨኘ"): env.get(bstack11ll_opy_ (u"ࠣࡉࡒࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡃࡐࡗࡑࡘࡊࡘࠢኙ"))
        }
    if env.get(bstack11ll_opy_ (u"ࠤࡆࡊࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢኚ")):
        return {
            bstack11ll_opy_ (u"ࠥࡲࡦࡳࡥࠣኛ"): bstack11ll_opy_ (u"ࠦࡈࡵࡤࡦࡈࡵࡩࡸ࡮ࠢኜ"),
            bstack11ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣኝ"): env.get(bstack11ll_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧኞ")),
            bstack11ll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤኟ"): env.get(bstack11ll_opy_ (u"ࠣࡅࡉࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡎࡂࡏࡈࠦአ")),
            bstack11ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣኡ"): env.get(bstack11ll_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣኢ"))
        }
    return {bstack11ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥኣ"): None}
def get_host_info():
    return {
        bstack11ll_opy_ (u"ࠧ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠢኤ"): platform.node(),
        bstack11ll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠣእ"): platform.system(),
        bstack11ll_opy_ (u"ࠢࡵࡻࡳࡩࠧኦ"): platform.machine(),
        bstack11ll_opy_ (u"ࠣࡸࡨࡶࡸ࡯࡯࡯ࠤኧ"): platform.version(),
        bstack11ll_opy_ (u"ࠤࡤࡶࡨ࡮ࠢከ"): platform.architecture()[0]
    }
def bstack1111lll1_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11l11l1ll1_opy_():
    if bstack11llll1l_opy_.get_property(bstack11ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫኩ")):
        return bstack11ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪኪ")
    return bstack11ll_opy_ (u"ࠬࡻ࡮࡬ࡰࡲࡻࡳࡥࡧࡳ࡫ࡧࠫካ")
def bstack11l11ll1ll_opy_(driver):
    info = {
        bstack11ll_opy_ (u"࠭ࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬኬ"): driver.capabilities,
        bstack11ll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠫክ"): driver.session_id,
        bstack11ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩኮ"): driver.capabilities.get(bstack11ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧኯ"), None),
        bstack11ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬኰ"): driver.capabilities.get(bstack11ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ኱"), None),
        bstack11ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࠧኲ"): driver.capabilities.get(bstack11ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬኳ"), None),
    }
    if bstack11l11l1ll1_opy_() == bstack11ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ኴ"):
        info[bstack11ll_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩኵ")] = bstack11ll_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨ኶") if bstack111111l1_opy_() else bstack11ll_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ኷")
    return info
def bstack111111l1_opy_():
    if bstack11llll1l_opy_.get_property(bstack11ll_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪኸ")):
        return True
    if bstack111llll1_opy_(os.environ.get(bstack11ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ኹ"), None)):
        return True
    return False
def bstack1l11llll1_opy_(bstack11l111l1l1_opy_, url, data, config):
    headers = config.get(bstack11ll_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧኺ"), None)
    proxies = bstack11ll11l11_opy_(config, url)
    auth = config.get(bstack11ll_opy_ (u"ࠧࡢࡷࡷ࡬ࠬኻ"), None)
    response = requests.request(
            bstack11l111l1l1_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack11l11lll_opy_(bstack1l11l1l1_opy_, size):
    bstack1l11111l_opy_ = []
    while len(bstack1l11l1l1_opy_) > size:
        bstack1ll11111_opy_ = bstack1l11l1l1_opy_[:size]
        bstack1l11111l_opy_.append(bstack1ll11111_opy_)
        bstack1l11l1l1_opy_ = bstack1l11l1l1_opy_[size:]
    bstack1l11111l_opy_.append(bstack1l11l1l1_opy_)
    return bstack1l11111l_opy_
def bstack111lll1111_opy_(message, bstack11l111l11l_opy_=False):
    os.write(1, bytes(message, bstack11ll_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧኼ")))
    os.write(1, bytes(bstack11ll_opy_ (u"ࠩ࡟ࡲࠬኽ"), bstack11ll_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩኾ")))
    if bstack11l111l11l_opy_:
        with open(bstack11ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠱ࡴ࠷࠱ࡺ࠯ࠪ኿") + os.environ[bstack11ll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫዀ")] + bstack11ll_opy_ (u"࠭࠮࡭ࡱࡪࠫ዁"), bstack11ll_opy_ (u"ࠧࡢࠩዂ")) as f:
            f.write(message + bstack11ll_opy_ (u"ࠨ࡞ࡱࠫዃ"))
def bstack11l11l11l1_opy_():
    return os.environ[bstack11ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬዄ")].lower() == bstack11ll_opy_ (u"ࠪࡸࡷࡻࡥࠨዅ")
def bstack1l111ll11_opy_(bstack11l111l1ll_opy_):
    return bstack11ll_opy_ (u"ࠫࢀࢃ࠯ࡼࡿࠪ዆").format(bstack11l1l11lll_opy_, bstack11l111l1ll_opy_)
def bstack1llll1llll_opy_():
    return datetime.datetime.utcnow().isoformat() + bstack11ll_opy_ (u"ࠬࡠࠧ዇")
def bstack11l1111l1l_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack11ll_opy_ (u"࡚࠭ࠨወ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack11ll_opy_ (u"࡛ࠧࠩዉ")))).total_seconds() * 1000
def bstack11l1111lll_opy_(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp).isoformat() + bstack11ll_opy_ (u"ࠨ࡜ࠪዊ")
def bstack111lll1l11_opy_(bstack11l111ll11_opy_):
    date_format = bstack11ll_opy_ (u"ࠩࠨ࡝ࠪࡳࠥࡥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖ࠲ࠪ࡬ࠧዋ")
    bstack11l1111111_opy_ = datetime.datetime.strptime(bstack11l111ll11_opy_, date_format)
    return bstack11l1111111_opy_.isoformat() + bstack11ll_opy_ (u"ࠪ࡞ࠬዌ")
def bstack11l11lll11_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack11ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫው")
    else:
        return bstack11ll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬዎ")
def bstack111llll1_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack11ll_opy_ (u"࠭ࡴࡳࡷࡨࠫዏ")
def bstack111llll111_opy_(val):
    return val.__str__().lower() == bstack11ll_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ዐ")
def bstack1l111l1l1l_opy_(bstack111ll1l1l1_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack111ll1l1l1_opy_ as e:
                print(bstack11ll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡾࢁࠥ࠳࠾ࠡࡽࢀ࠾ࠥࢁࡽࠣዑ").format(func.__name__, bstack111ll1l1l1_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11l11111ll_opy_(bstack111lll11l1_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack111lll11l1_opy_(cls, *args, **kwargs)
            except bstack111ll1l1l1_opy_ as e:
                print(bstack11ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡿࢂࠦ࠭࠿ࠢࡾࢁ࠿ࠦࡻࡾࠤዒ").format(bstack111lll11l1_opy_.__name__, bstack111ll1l1l1_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11l11111ll_opy_
    else:
        return decorator
def bstack11l1lllll_opy_(bstack11lll11111_opy_):
    if bstack11ll_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧዓ") in bstack11lll11111_opy_ and bstack111llll111_opy_(bstack11lll11111_opy_[bstack11ll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨዔ")]):
        return False
    if bstack11ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧዕ") in bstack11lll11111_opy_ and bstack111llll111_opy_(bstack11lll11111_opy_[bstack11ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨዖ")]):
        return False
    return True
def bstack111l1lll1_opy_():
    try:
        from pytest_bdd import reporting
        return True
    except Exception as e:
        return False
def bstack1ll11l1l_opy_(hub_url):
    if bstack1ll11lll_opy_() <= version.parse(bstack11ll_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧ዗")):
        if hub_url != bstack11ll_opy_ (u"ࠨࠩዘ"):
            return bstack11ll_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥዙ") + hub_url + bstack11ll_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢዚ")
        return bstack1l1llll1l_opy_
    if hub_url != bstack11ll_opy_ (u"ࠫࠬዛ"):
        return bstack11ll_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢዜ") + hub_url + bstack11ll_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢዝ")
    return bstack1lll1lll1_opy_
def bstack11l111lll1_opy_():
    return isinstance(os.getenv(bstack11ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡍࡗࡊࡍࡓ࠭ዞ")), str)
def bstack1ll111ll1_opy_(url):
    return urlparse(url).hostname
def bstack1lllll1ll1_opy_(hostname):
    for bstack1ll1ll11l1_opy_ in bstack1lllll1ll_opy_:
        regex = re.compile(bstack1ll1ll11l1_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack111lll11ll_opy_(bstack11l11ll11l_opy_, file_name, logger):
    bstack1ll1llllll_opy_ = os.path.join(os.path.expanduser(bstack11ll_opy_ (u"ࠨࢀࠪዟ")), bstack11l11ll11l_opy_)
    try:
        if not os.path.exists(bstack1ll1llllll_opy_):
            os.makedirs(bstack1ll1llllll_opy_)
        file_path = os.path.join(os.path.expanduser(bstack11ll_opy_ (u"ࠩࢁࠫዠ")), bstack11l11ll11l_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack11ll_opy_ (u"ࠪࡻࠬዡ")):
                pass
            with open(file_path, bstack11ll_opy_ (u"ࠦࡼ࠱ࠢዢ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack111ll1l11_opy_.format(str(e)))
def bstack111ll11lll_opy_(file_name, key, value, logger):
    file_path = bstack111lll11ll_opy_(bstack11ll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬዣ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1l1lllllll_opy_ = json.load(open(file_path, bstack11ll_opy_ (u"࠭ࡲࡣࠩዤ")))
        else:
            bstack1l1lllllll_opy_ = {}
        bstack1l1lllllll_opy_[key] = value
        with open(file_path, bstack11ll_opy_ (u"ࠢࡸ࠭ࠥዥ")) as outfile:
            json.dump(bstack1l1lllllll_opy_, outfile)
def bstack1111l1ll_opy_(file_name, logger):
    file_path = bstack111lll11ll_opy_(bstack11ll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨዦ"), file_name, logger)
    bstack1l1lllllll_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack11ll_opy_ (u"ࠩࡵࠫዧ")) as bstack11l1l111l_opy_:
            bstack1l1lllllll_opy_ = json.load(bstack11l1l111l_opy_)
    return bstack1l1lllllll_opy_
def bstack1llll1lll1_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack11ll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡪࡥ࡭ࡧࡷ࡭ࡳ࡭ࠠࡧ࡫࡯ࡩ࠿ࠦࠧየ") + file_path + bstack11ll_opy_ (u"ࠫࠥ࠭ዩ") + str(e))
def bstack1ll11lll_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack11ll_opy_ (u"ࠧࡂࡎࡐࡖࡖࡉ࡙ࡄࠢዪ")
def bstack1ll1l11lll_opy_(config):
    if bstack11ll_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬያ") in config:
        del (config[bstack11ll_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ዬ")])
        return False
    if bstack1ll11lll_opy_() < version.parse(bstack11ll_opy_ (u"ࠨ࠵࠱࠸࠳࠶ࠧይ")):
        return False
    if bstack1ll11lll_opy_() >= version.parse(bstack11ll_opy_ (u"ࠩ࠷࠲࠶࠴࠵ࠨዮ")):
        return True
    if bstack11ll_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪዯ") in config and config[bstack11ll_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫደ")] is False:
        return False
    else:
        return True
def bstack1l1lll1lll_opy_(args_list, bstack11l11l111l_opy_):
    index = -1
    for value in bstack11l11l111l_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1l11111l1l_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1l11111l1l_opy_ = bstack1l11111l1l_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack11ll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬዱ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack11ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ዲ"), exception=exception)
    def bstack11ll1l1l11_opy_(self):
        if self.result != bstack11ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧዳ"):
            return None
        if bstack11ll_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦዴ") in self.exception_type:
            return bstack11ll_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥድ")
        return bstack11ll_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦዶ")
    def bstack111ll1lll1_opy_(self):
        if self.result != bstack11ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫዷ"):
            return None
        if self.bstack1l11111l1l_opy_:
            return self.bstack1l11111l1l_opy_
        return bstack11l111l111_opy_(self.exception)
def bstack11l111l111_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack111ll1ll11_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1ll1l111ll_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1l11ll1l_opy_(config, logger):
    try:
        import playwright
        bstack11l1111ll1_opy_ = playwright.__file__
        bstack11l11l1l11_opy_ = os.path.split(bstack11l1111ll1_opy_)
        bstack111lllll11_opy_ = bstack11l11l1l11_opy_[0] + bstack11ll_opy_ (u"ࠬ࠵ࡤࡳ࡫ࡹࡩࡷ࠵ࡰࡢࡥ࡮ࡥ࡬࡫࠯࡭࡫ࡥ࠳ࡨࡲࡩ࠰ࡥ࡯࡭࠳ࡰࡳࠨዸ")
        os.environ[bstack11ll_opy_ (u"࠭ࡇࡍࡑࡅࡅࡑࡥࡁࡈࡇࡑࡘࡤࡎࡔࡕࡒࡢࡔࡗࡕࡘ࡚ࠩዹ")] = bstack1ll111lll1_opy_(config)
        with open(bstack111lllll11_opy_, bstack11ll_opy_ (u"ࠧࡳࠩዺ")) as f:
            bstack11ll1ll1_opy_ = f.read()
            bstack111ll11l1l_opy_ = bstack11ll_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠧዻ")
            bstack11l111ll1l_opy_ = bstack11ll1ll1_opy_.find(bstack111ll11l1l_opy_)
            if bstack11l111ll1l_opy_ == -1:
              process = subprocess.Popen(bstack11ll_opy_ (u"ࠤࡱࡴࡲࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡨ࡮ࡲࡦࡦࡲ࠭ࡢࡩࡨࡲࡹࠨዼ"), shell=True, cwd=bstack11l11l1l11_opy_[0])
              process.wait()
              bstack111ll11l11_opy_ = bstack11ll_opy_ (u"ࠪࠦࡺࡹࡥࠡࡵࡷࡶ࡮ࡩࡴࠣ࠽ࠪዽ")
              bstack11l11ll1l1_opy_ = bstack11ll_opy_ (u"ࠦࠧࠨࠠ࡝ࠤࡸࡷࡪࠦࡳࡵࡴ࡬ࡧࡹࡢࠢ࠼ࠢࡦࡳࡳࡹࡴࠡࡽࠣࡦࡴࡵࡴࡴࡶࡵࡥࡵࠦࡽࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠬ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠫ࠮ࡁࠠࡪࡨࠣࠬࡵࡸ࡯ࡤࡧࡶࡷ࠳࡫࡮ࡷ࠰ࡊࡐࡔࡈࡁࡍࡡࡄࡋࡊࡔࡔࡠࡊࡗࡘࡕࡥࡐࡓࡑ࡛࡝࠮ࠦࡢࡰࡱࡷࡷࡹࡸࡡࡱࠪࠬ࠿ࠥࠨࠢࠣዾ")
              bstack11l111111l_opy_ = bstack11ll1ll1_opy_.replace(bstack111ll11l11_opy_, bstack11l11ll1l1_opy_)
              with open(bstack111lllll11_opy_, bstack11ll_opy_ (u"ࠬࡽࠧዿ")) as f:
                f.write(bstack11l111111l_opy_)
    except Exception as e:
        logger.error(bstack1ll1llll1_opy_.format(str(e)))
def bstack1lllll1lll_opy_():
  try:
    bstack111lll1lll_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll_opy_ (u"࠭࡯ࡱࡶ࡬ࡱࡦࡲ࡟ࡩࡷࡥࡣࡺࡸ࡬࠯࡬ࡶࡳࡳ࠭ጀ"))
    bstack111llll1ll_opy_ = []
    if os.path.exists(bstack111lll1lll_opy_):
      with open(bstack111lll1lll_opy_) as f:
        bstack111llll1ll_opy_ = json.load(f)
      os.remove(bstack111lll1lll_opy_)
    return bstack111llll1ll_opy_
  except:
    pass
  return []
def bstack1l1l1ll11_opy_(bstack1l111lll1_opy_):
  try:
    bstack111llll1ll_opy_ = []
    bstack111lll1lll_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll_opy_ (u"ࠧࡰࡲࡷ࡭ࡲࡧ࡬ࡠࡪࡸࡦࡤࡻࡲ࡭࠰࡭ࡷࡴࡴࠧጁ"))
    if os.path.exists(bstack111lll1lll_opy_):
      with open(bstack111lll1lll_opy_) as f:
        bstack111llll1ll_opy_ = json.load(f)
    bstack111llll1ll_opy_.append(bstack1l111lll1_opy_)
    with open(bstack111lll1lll_opy_, bstack11ll_opy_ (u"ࠨࡹࠪጂ")) as f:
        json.dump(bstack111llll1ll_opy_, f)
  except:
    pass
def bstack1111l11ll_opy_(logger, bstack111ll1l11l_opy_ = False):
  try:
    test_name = os.environ.get(bstack11ll_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬጃ"), bstack11ll_opy_ (u"ࠪࠫጄ"))
    if test_name == bstack11ll_opy_ (u"ࠫࠬጅ"):
        test_name = threading.current_thread().__dict__.get(bstack11ll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡇࡪࡤࡠࡶࡨࡷࡹࡥ࡮ࡢ࡯ࡨࠫጆ"), bstack11ll_opy_ (u"࠭ࠧጇ"))
    bstack11l11l11ll_opy_ = bstack11ll_opy_ (u"ࠧ࠭ࠢࠪገ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack111ll1l11l_opy_:
        bstack1l1l111l_opy_ = os.environ.get(bstack11ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨጉ"), bstack11ll_opy_ (u"ࠩ࠳ࠫጊ"))
        bstack1l1l1ll1l1_opy_ = {bstack11ll_opy_ (u"ࠪࡲࡦࡳࡥࠨጋ"): test_name, bstack11ll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪጌ"): bstack11l11l11ll_opy_, bstack11ll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫግ"): bstack1l1l111l_opy_}
        bstack111llllll1_opy_ = []
        bstack11l11lll1l_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡰࡱࡲࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬጎ"))
        if os.path.exists(bstack11l11lll1l_opy_):
            with open(bstack11l11lll1l_opy_) as f:
                bstack111llllll1_opy_ = json.load(f)
        bstack111llllll1_opy_.append(bstack1l1l1ll1l1_opy_)
        with open(bstack11l11lll1l_opy_, bstack11ll_opy_ (u"ࠧࡸࠩጏ")) as f:
            json.dump(bstack111llllll1_opy_, f)
    else:
        bstack1l1l1ll1l1_opy_ = {bstack11ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ጐ"): test_name, bstack11ll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ጑"): bstack11l11l11ll_opy_, bstack11ll_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩጒ"): str(multiprocessing.current_process().name)}
        if bstack11ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴࠨጓ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1l1l1ll1l1_opy_)
  except Exception as e:
      logger.warn(bstack11ll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡱࡻࡷࡩࡸࡺࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤጔ").format(e))
def bstack1ll111ll1l_opy_(error_message, test_name, index, logger):
  try:
    bstack111ll1l111_opy_ = []
    bstack1l1l1ll1l1_opy_ = {bstack11ll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫጕ"): test_name, bstack11ll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭጖"): error_message, bstack11ll_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ጗"): index}
    bstack111llll11l_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll_opy_ (u"ࠩࡵࡳࡧࡵࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪጘ"))
    if os.path.exists(bstack111llll11l_opy_):
        with open(bstack111llll11l_opy_) as f:
            bstack111ll1l111_opy_ = json.load(f)
    bstack111ll1l111_opy_.append(bstack1l1l1ll1l1_opy_)
    with open(bstack111llll11l_opy_, bstack11ll_opy_ (u"ࠪࡻࠬጙ")) as f:
        json.dump(bstack111ll1l111_opy_, f)
  except Exception as e:
    logger.warn(bstack11ll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡲࡰࡤࡲࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢጚ").format(e))
def bstack11111ll1_opy_(bstack1ll1l1l1l_opy_, name, logger):
  try:
    bstack1l1l1ll1l1_opy_ = {bstack11ll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪጛ"): name, bstack11ll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬጜ"): bstack1ll1l1l1l_opy_, bstack11ll_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ጝ"): str(threading.current_thread()._name)}
    return bstack1l1l1ll1l1_opy_
  except Exception as e:
    logger.warn(bstack11ll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡦࡪ࡮ࡡࡷࡧࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧጞ").format(e))
  return
def bstack111ll1l1ll_opy_():
    return platform.system() == bstack11ll_opy_ (u"࡚ࠩ࡭ࡳࡪ࡯ࡸࡵࠪጟ")
def bstack1ll1lll1ll_opy_(bstack111lll111l_opy_, config, logger):
    bstack11l111llll_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack111lll111l_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack11ll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪ࡮ࡷࡩࡷࠦࡣࡰࡰࡩ࡭࡬ࠦ࡫ࡦࡻࡶࠤࡧࡿࠠࡳࡧࡪࡩࡽࠦ࡭ࡢࡶࡦ࡬࠿ࠦࡻࡾࠤጠ").format(e))
    return bstack11l111llll_opy_
def bstack11l11l1111_opy_(bstack11l11ll111_opy_, bstack111ll1ll1l_opy_):
    bstack111llll1l1_opy_ = version.parse(bstack11l11ll111_opy_)
    bstack11l11l1l1l_opy_ = version.parse(bstack111ll1ll1l_opy_)
    if bstack111llll1l1_opy_ > bstack11l11l1l1l_opy_:
        return 1
    elif bstack111llll1l1_opy_ < bstack11l11l1l1l_opy_:
        return -1
    else:
        return 0