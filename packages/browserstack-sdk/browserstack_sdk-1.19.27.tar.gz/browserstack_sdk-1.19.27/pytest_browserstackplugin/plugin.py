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
import atexit
import datetime
import inspect
import logging
import os
import signal
import sys
import threading
from uuid import uuid4
from bstack_utils.percy_sdk import PercySDK
import tempfile
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1llll1l111_opy_, bstack1l11ll1l1l_opy_, update, bstack11l111l1l_opy_,
                                       bstack1ll1111ll_opy_, bstack11111111_opy_, bstack1ll11ll11_opy_, bstack1l1ll1llll_opy_,
                                       bstack1111l11l_opy_, bstack1ll1111lll_opy_, bstack1l111l11l_opy_, bstack11lll11l_opy_,
                                       bstack11111111l_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1l1ll1111_opy_)
from browserstack_sdk.bstack1llll1111l_opy_ import bstack11l1l1ll_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack1ll1l11l11_opy_
from bstack_utils.capture import bstack1l1111l11l_opy_
from bstack_utils.config import Config
from bstack_utils.constants import bstack111l1111_opy_, bstack1l1ll11l1l_opy_, bstack11l1lll11_opy_, \
    bstack1ll11l111_opy_
from bstack_utils.helper import bstack1ll1l111ll_opy_, bstack1111lll1_opy_, bstack11l11l11l1_opy_, bstack1llll1llll_opy_, \
    bstack11l11lll11_opy_, \
    bstack11l11l1lll_opy_, bstack1ll11lll_opy_, bstack1ll11l1l_opy_, bstack11l111lll1_opy_, bstack111l1lll1_opy_, Notset, \
    bstack1ll1l11lll_opy_, bstack11l1111l1l_opy_, bstack11l111l111_opy_, Result, bstack11l1111lll_opy_, bstack111ll1ll11_opy_, bstack1l111l1l1l_opy_, \
    bstack1l1l1ll11_opy_, bstack1111l11ll_opy_, bstack111llll1_opy_, bstack111ll1l1ll_opy_
from bstack_utils.bstack111l1ll111_opy_ import bstack111l1l1ll1_opy_
from bstack_utils.messages import bstack1ll1llll11_opy_, bstack1l111l11_opy_, bstack11lll1111_opy_, bstack1ll1ll1ll1_opy_, bstack1l11lll1l_opy_, \
    bstack1ll1llll1_opy_, bstack1ll11lll1_opy_, bstack11ll11l1l_opy_, bstack1l111111_opy_, bstack11l11l1l1_opy_, \
    bstack11l111l11_opy_, bstack1ll111l1ll_opy_
from bstack_utils.proxy import bstack1ll111lll1_opy_, bstack11l1ll11l_opy_
from bstack_utils.bstack1llll111l1_opy_ import bstack1llllll1l1l_opy_, bstack1llllll1111_opy_, bstack1lllll1lll1_opy_, bstack1lllll1l1l1_opy_, \
    bstack1llllll111l_opy_, bstack1lllll1llll_opy_, bstack1lllll1l1ll_opy_, bstack111l1l11l_opy_, bstack1llllll11l1_opy_
from bstack_utils.bstack1l1ll1ll1_opy_ import bstack1ll111l1l_opy_
from bstack_utils.bstack1llllll111_opy_ import bstack1lllll111l_opy_, bstack1ll111l111_opy_, bstack1l1l1l11l1_opy_, \
    bstack1l1l11l11_opy_, bstack1ll11l111l_opy_
from bstack_utils.bstack11lll1l1ll_opy_ import bstack1l1111ll1l_opy_
from bstack_utils.bstack11ll11111_opy_ import bstack1l1ll111l1_opy_
import bstack_utils.bstack11l1111l_opy_ as bstack1l1l11111l_opy_
from bstack_utils.bstack1l1l1l1ll_opy_ import bstack1l1l1l1ll_opy_
bstack11l1lll1_opy_ = None
bstack11lll111_opy_ = None
bstack1l1ll11ll_opy_ = None
bstack1l1l1lll11_opy_ = None
bstack1l1ll11111_opy_ = None
bstack1l1lll1ll_opy_ = None
bstack1l1l1lll1l_opy_ = None
bstack1ll11ll1l_opy_ = None
bstack1l1ll111l_opy_ = None
bstack11l1l111_opy_ = None
bstack1llll1ll_opy_ = None
bstack111lll11_opy_ = None
bstack1l11lllll1_opy_ = None
bstack1l11ll1ll_opy_ = bstack11ll_opy_ (u"ࠧࠨᗙ")
CONFIG = {}
bstack1lllll11_opy_ = False
bstack1l1l111ll_opy_ = bstack11ll_opy_ (u"ࠨࠩᗚ")
bstack1111ll1ll_opy_ = bstack11ll_opy_ (u"ࠩࠪᗛ")
bstack1ll1l11l_opy_ = False
bstack1111111l1_opy_ = []
bstack1l11l1lll_opy_ = bstack111l1111_opy_
bstack1lll11ll111_opy_ = bstack11ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᗜ")
bstack1lll111ll1l_opy_ = False
bstack111llllll_opy_ = {}
bstack1l1l1l111_opy_ = False
logger = bstack1ll1l11l11_opy_.get_logger(__name__, bstack1l11l1lll_opy_)
store = {
    bstack11ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᗝ"): []
}
bstack1lll111l1ll_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_11llll1ll1_opy_ = {}
current_test_uuid = None
def bstack1ll11l1ll_opy_(page, bstack1l1ll1ll11_opy_):
    try:
        page.evaluate(bstack11ll_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨᗞ"),
                      bstack11ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠪᗟ") + json.dumps(
                          bstack1l1ll1ll11_opy_) + bstack11ll_opy_ (u"ࠢࡾࡿࠥᗠ"))
    except Exception as e:
        print(bstack11ll_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣࡿࢂࠨᗡ"), e)
def bstack1111llll1_opy_(page, message, level):
    try:
        page.evaluate(bstack11ll_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥᗢ"), bstack11ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨᗣ") + json.dumps(
            message) + bstack11ll_opy_ (u"ࠫ࠱ࠨ࡬ࡦࡸࡨࡰࠧࡀࠧᗤ") + json.dumps(level) + bstack11ll_opy_ (u"ࠬࢃࡽࠨᗥ"))
    except Exception as e:
        print(bstack11ll_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡤࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠦࡻࡾࠤᗦ"), e)
def pytest_configure(config):
    bstack11llll1l_opy_ = Config.bstack11l1l11l1_opy_()
    config.args = bstack1l1ll111l1_opy_.bstack1lll1ll11l1_opy_(config.args)
    bstack11llll1l_opy_.bstack1l11llllll_opy_(bstack111llll1_opy_(config.getoption(bstack11ll_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᗧ"))))
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack1lll1l111l1_opy_ = item.config.getoption(bstack11ll_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᗨ"))
    plugins = item.config.getoption(bstack11ll_opy_ (u"ࠤࡳࡰࡺ࡭ࡩ࡯ࡵࠥᗩ"))
    report = outcome.get_result()
    bstack1lll1l111ll_opy_(item, call, report)
    if bstack11ll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡲ࡯ࡹ࡬࡯࡮ࠣᗪ") not in plugins or bstack111l1lll1_opy_():
        return
    summary = []
    driver = getattr(item, bstack11ll_opy_ (u"ࠦࡤࡪࡲࡪࡸࡨࡶࠧᗫ"), None)
    page = getattr(item, bstack11ll_opy_ (u"ࠧࡥࡰࡢࡩࡨࠦᗬ"), None)
    try:
        if (driver == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack1lll1l11l11_opy_(item, report, summary, bstack1lll1l111l1_opy_)
    if (page is not None):
        bstack1lll11ll11l_opy_(item, report, summary, bstack1lll1l111l1_opy_)
def bstack1lll1l11l11_opy_(item, report, summary, bstack1lll1l111l1_opy_):
    if report.when == bstack11ll_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᗭ") and report.skipped:
        bstack1llllll11l1_opy_(report)
    if report.when in [bstack11ll_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨᗮ"), bstack11ll_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥᗯ")]:
        return
    if not bstack11l11l11l1_opy_():
        return
    try:
        if (str(bstack1lll1l111l1_opy_).lower() != bstack11ll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᗰ")):
            item._driver.execute_script(
                bstack11ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠠࠨᗱ") + json.dumps(
                    report.nodeid) + bstack11ll_opy_ (u"ࠫࢂࢃࠧᗲ"))
        os.environ[bstack11ll_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨᗳ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack11ll_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡲࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥ࠻ࠢࡾ࠴ࢂࠨᗴ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11ll_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤᗵ")))
    bstack1lll1ll1l1_opy_ = bstack11ll_opy_ (u"ࠣࠤᗶ")
    bstack1llllll11l1_opy_(report)
    if not passed:
        try:
            bstack1lll1ll1l1_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack11ll_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡷ࡫ࡡࡴࡱࡱ࠾ࠥࢁ࠰ࡾࠤᗷ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1lll1ll1l1_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack11ll_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧᗸ")))
        bstack1lll1ll1l1_opy_ = bstack11ll_opy_ (u"ࠦࠧᗹ")
        if not passed:
            try:
                bstack1lll1ll1l1_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11ll_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡳࡧࡤࡷࡴࡴ࠺ࠡࡽ࠳ࢁࠧᗺ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1lll1ll1l1_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack11ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤ࡬ࡲ࡫ࡵࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡧࡥࡹࡧࠢ࠻ࠢࠪᗻ")
                    + json.dumps(bstack11ll_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠡࠣᗼ"))
                    + bstack11ll_opy_ (u"ࠣ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࠦᗽ")
                )
            else:
                item._driver.execute_script(
                    bstack11ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡫ࡲࡳࡱࡵࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡤࡢࡶࡤࠦ࠿ࠦࠧᗾ")
                    + json.dumps(str(bstack1lll1ll1l1_opy_))
                    + bstack11ll_opy_ (u"ࠥࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࠨᗿ")
                )
        except Exception as e:
            summary.append(bstack11ll_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡤࡲࡳࡵࡴࡢࡶࡨ࠾ࠥࢁ࠰ࡾࠤᘀ").format(e))
def bstack1lll11lll11_opy_(test_name, error_message):
    try:
        bstack1lll1l1ll1l_opy_ = []
        bstack1l1l111l_opy_ = os.environ.get(bstack11ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᘁ"), bstack11ll_opy_ (u"࠭࠰ࠨᘂ"))
        bstack1l1l1ll1l1_opy_ = {bstack11ll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᘃ"): test_name, bstack11ll_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᘄ"): error_message, bstack11ll_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨᘅ"): bstack1l1l111l_opy_}
        bstack1lll1l11lll_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll_opy_ (u"ࠪࡴࡼࡥࡰࡺࡶࡨࡷࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨᘆ"))
        if os.path.exists(bstack1lll1l11lll_opy_):
            with open(bstack1lll1l11lll_opy_) as f:
                bstack1lll1l1ll1l_opy_ = json.load(f)
        bstack1lll1l1ll1l_opy_.append(bstack1l1l1ll1l1_opy_)
        with open(bstack1lll1l11lll_opy_, bstack11ll_opy_ (u"ࠫࡼ࠭ᘇ")) as f:
            json.dump(bstack1lll1l1ll1l_opy_, f)
    except Exception as e:
        logger.debug(bstack11ll_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡧࡵࡷ࡮ࡹࡴࡪࡰࡪࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡲࡼࡸࡪࡹࡴࠡࡧࡵࡶࡴࡸࡳ࠻ࠢࠪᘈ") + str(e))
def bstack1lll11ll11l_opy_(item, report, summary, bstack1lll1l111l1_opy_):
    if report.when in [bstack11ll_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧᘉ"), bstack11ll_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤᘊ")]:
        return
    if (str(bstack1lll1l111l1_opy_).lower() != bstack11ll_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᘋ")):
        bstack1ll11l1ll_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11ll_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦᘌ")))
    bstack1lll1ll1l1_opy_ = bstack11ll_opy_ (u"ࠥࠦᘍ")
    bstack1llllll11l1_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1lll1ll1l1_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11ll_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡲࡦࡣࡶࡳࡳࡀࠠࡼ࠲ࢀࠦᘎ").format(e)
                )
        try:
            if passed:
                bstack1ll11l111l_opy_(getattr(item, bstack11ll_opy_ (u"ࠬࡥࡰࡢࡩࡨࠫᘏ"), None), bstack11ll_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨᘐ"))
            else:
                error_message = bstack11ll_opy_ (u"ࠧࠨᘑ")
                if bstack1lll1ll1l1_opy_:
                    bstack1111llll1_opy_(item._page, str(bstack1lll1ll1l1_opy_), bstack11ll_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢᘒ"))
                    bstack1ll11l111l_opy_(getattr(item, bstack11ll_opy_ (u"ࠩࡢࡴࡦ࡭ࡥࠨᘓ"), None), bstack11ll_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᘔ"), str(bstack1lll1ll1l1_opy_))
                    error_message = str(bstack1lll1ll1l1_opy_)
                else:
                    bstack1ll11l111l_opy_(getattr(item, bstack11ll_opy_ (u"ࠫࡤࡶࡡࡨࡧࠪᘕ"), None), bstack11ll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᘖ"))
                bstack1lll11lll11_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack11ll_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡺࡶࡤࡢࡶࡨࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻ࠱ࡿࠥᘗ").format(e))
try:
    from typing import Generator
    import pytest_playwright.pytest_playwright as p
    @pytest.fixture
    def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
        page = context.new_page()
        request.node._page = page
        yield page
except:
    pass
def pytest_addoption(parser):
    parser.addoption(bstack11ll_opy_ (u"ࠢ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦᘘ"), default=bstack11ll_opy_ (u"ࠣࡈࡤࡰࡸ࡫ࠢᘙ"), help=bstack11ll_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡧࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠣᘚ"))
    parser.addoption(bstack11ll_opy_ (u"ࠥ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤᘛ"), default=bstack11ll_opy_ (u"ࠦࡋࡧ࡬ࡴࡧࠥᘜ"), help=bstack11ll_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡯ࡣࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠦᘝ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack11ll_opy_ (u"ࠨ࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠣᘞ"), action=bstack11ll_opy_ (u"ࠢࡴࡶࡲࡶࡪࠨᘟ"), default=bstack11ll_opy_ (u"ࠣࡥ࡫ࡶࡴࡳࡥࠣᘠ"),
                         help=bstack11ll_opy_ (u"ࠤࡇࡶ࡮ࡼࡥࡳࠢࡷࡳࠥࡸࡵ࡯ࠢࡷࡩࡸࡺࡳࠣᘡ"))
def bstack1l11l111ll_opy_(log):
    if not (log[bstack11ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᘢ")] and log[bstack11ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᘣ")].strip()):
        return
    active = bstack11llllllll_opy_()
    log = {
        bstack11ll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᘤ"): log[bstack11ll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᘥ")],
        bstack11ll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᘦ"): datetime.datetime.utcnow().isoformat() + bstack11ll_opy_ (u"ࠨ࡜ࠪᘧ"),
        bstack11ll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᘨ"): log[bstack11ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᘩ")],
    }
    if active:
        if active[bstack11ll_opy_ (u"ࠫࡹࡿࡰࡦࠩᘪ")] == bstack11ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᘫ"):
            log[bstack11ll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᘬ")] = active[bstack11ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᘭ")]
        elif active[bstack11ll_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᘮ")] == bstack11ll_opy_ (u"ࠩࡷࡩࡸࡺࠧᘯ"):
            log[bstack11ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᘰ")] = active[bstack11ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᘱ")]
    bstack1l1ll111l1_opy_.bstack1l1ll11l_opy_([log])
def bstack11llllllll_opy_():
    if len(store[bstack11ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᘲ")]) > 0 and store[bstack11ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᘳ")][-1]:
        return {
            bstack11ll_opy_ (u"ࠧࡵࡻࡳࡩࠬᘴ"): bstack11ll_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᘵ"),
            bstack11ll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᘶ"): store[bstack11ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᘷ")][-1]
        }
    if store.get(bstack11ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᘸ"), None):
        return {
            bstack11ll_opy_ (u"ࠬࡺࡹࡱࡧࠪᘹ"): bstack11ll_opy_ (u"࠭ࡴࡦࡵࡷࠫᘺ"),
            bstack11ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᘻ"): store[bstack11ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᘼ")]
        }
    return None
bstack11lllll11l_opy_ = bstack1l1111l11l_opy_(bstack1l11l111ll_opy_)
def pytest_runtest_call(item):
    try:
        global CONFIG
        global bstack1lll111ll1l_opy_
        item._1lll1l1111l_opy_ = True
        bstack1lll111l11_opy_ = bstack1l1l11111l_opy_.bstack11ll1lll1_opy_(CONFIG, bstack11l11l1lll_opy_(item.own_markers))
        item._a11y_test_case = bstack1lll111l11_opy_
        if bstack1lll111ll1l_opy_:
            driver = getattr(item, bstack11ll_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪᘽ"), None)
            item._a11y_started = bstack1l1l11111l_opy_.bstack11111l11l_opy_(driver, bstack1lll111l11_opy_)
        if not bstack1l1ll111l1_opy_.on() or bstack1lll11ll111_opy_ != bstack11ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᘾ"):
            return
        global current_test_uuid, bstack11lllll11l_opy_
        bstack11lllll11l_opy_.start()
        bstack1l1111lll1_opy_ = {
            bstack11ll_opy_ (u"ࠫࡺࡻࡩࡥࠩᘿ"): uuid4().__str__(),
            bstack11ll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᙀ"): datetime.datetime.utcnow().isoformat() + bstack11ll_opy_ (u"࡚࠭ࠨᙁ")
        }
        current_test_uuid = bstack1l1111lll1_opy_[bstack11ll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᙂ")]
        store[bstack11ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᙃ")] = bstack1l1111lll1_opy_[bstack11ll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᙄ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _11llll1ll1_opy_[item.nodeid] = {**_11llll1ll1_opy_[item.nodeid], **bstack1l1111lll1_opy_}
        bstack1lll1l1l11l_opy_(item, _11llll1ll1_opy_[item.nodeid], bstack11ll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᙅ"))
    except Exception as err:
        print(bstack11ll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡨࡧ࡬࡭࠼ࠣࡿࢂ࠭ᙆ"), str(err))
def pytest_runtest_setup(item):
    global bstack1lll111l1ll_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack11l111lll1_opy_():
        atexit.register(bstack1llll11l11_opy_)
        if not bstack1lll111l1ll_opy_:
            try:
                bstack1lll1l1l1l1_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack111ll1l1ll_opy_():
                    bstack1lll1l1l1l1_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1lll1l1l1l1_opy_:
                    signal.signal(s, bstack1lll1l11ll1_opy_)
                bstack1lll111l1ll_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack11ll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡳࡧࡪ࡭ࡸࡺࡥࡳࠢࡶ࡭࡬ࡴࡡ࡭ࠢ࡫ࡥࡳࡪ࡬ࡦࡴࡶ࠾ࠥࠨᙇ") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1llllll1l1l_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack11ll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᙈ")
    try:
        if not bstack1l1ll111l1_opy_.on():
            return
        bstack11lllll11l_opy_.start()
        uuid = uuid4().__str__()
        bstack1l1111lll1_opy_ = {
            bstack11ll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᙉ"): uuid,
            bstack11ll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᙊ"): datetime.datetime.utcnow().isoformat() + bstack11ll_opy_ (u"ࠩ࡝ࠫᙋ"),
            bstack11ll_opy_ (u"ࠪࡸࡾࡶࡥࠨᙌ"): bstack11ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᙍ"),
            bstack11ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨᙎ"): bstack11ll_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫᙏ"),
            bstack11ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪᙐ"): bstack11ll_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᙑ")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack11ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭ᙒ")] = item
        store[bstack11ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᙓ")] = [uuid]
        if not _11llll1ll1_opy_.get(item.nodeid, None):
            _11llll1ll1_opy_[item.nodeid] = {bstack11ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᙔ"): [], bstack11ll_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧᙕ"): []}
        _11llll1ll1_opy_[item.nodeid][bstack11ll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᙖ")].append(bstack1l1111lll1_opy_[bstack11ll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᙗ")])
        _11llll1ll1_opy_[item.nodeid + bstack11ll_opy_ (u"ࠨ࠯ࡶࡩࡹࡻࡰࠨᙘ")] = bstack1l1111lll1_opy_
        bstack1lll1l11l1l_opy_(item, bstack1l1111lll1_opy_, bstack11ll_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᙙ"))
    except Exception as err:
        print(bstack11ll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡵࡹࡳࡺࡥࡴࡶࡢࡷࡪࡺࡵࡱ࠼ࠣࡿࢂ࠭ᙚ"), str(err))
def pytest_runtest_teardown(item):
    try:
        global bstack111llllll_opy_
        if CONFIG.get(bstack11ll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪᙛ"), False):
            if CONFIG.get(bstack11ll_opy_ (u"ࠬࡶࡥࡳࡥࡼࡇࡦࡶࡴࡶࡴࡨࡑࡴࡪࡥࠨᙜ"), bstack11ll_opy_ (u"ࠨࡡࡶࡶࡲࠦᙝ")) == bstack11ll_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤᙞ"):
                bstack1lll11l11l1_opy_ = bstack1ll1l111ll_opy_(threading.current_thread(), bstack11ll_opy_ (u"ࠨࡲࡨࡶࡨࡿࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᙟ"), None)
                bstack111l1lll_opy_ = bstack1lll11l11l1_opy_ + bstack11ll_opy_ (u"ࠤ࠰ࡸࡪࡹࡴࡤࡣࡶࡩࠧᙠ")
                driver = getattr(item, bstack11ll_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫᙡ"), None)
                PercySDK.screenshot(driver, bstack111l1lll_opy_)
        if getattr(item, bstack11ll_opy_ (u"ࠫࡤࡧ࠱࠲ࡻࡢࡷࡹࡧࡲࡵࡧࡧࠫᙢ"), False):
            bstack11l1l1ll_opy_.bstack1l111llll_opy_(getattr(item, bstack11ll_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭ᙣ"), None), bstack111llllll_opy_, logger, item)
        if not bstack1l1ll111l1_opy_.on():
            return
        bstack1l1111lll1_opy_ = {
            bstack11ll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᙤ"): uuid4().__str__(),
            bstack11ll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᙥ"): datetime.datetime.utcnow().isoformat() + bstack11ll_opy_ (u"ࠨ࡜ࠪᙦ"),
            bstack11ll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᙧ"): bstack11ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨᙨ"),
            bstack11ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧᙩ"): bstack11ll_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩᙪ"),
            bstack11ll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩᙫ"): bstack11ll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩᙬ")
        }
        _11llll1ll1_opy_[item.nodeid + bstack11ll_opy_ (u"ࠨ࠯ࡷࡩࡦࡸࡤࡰࡹࡱࠫ᙭")] = bstack1l1111lll1_opy_
        bstack1lll1l11l1l_opy_(item, bstack1l1111lll1_opy_, bstack11ll_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ᙮"))
    except Exception as err:
        print(bstack11ll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡵࡹࡳࡺࡥࡴࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲ࠿ࠦࡻࡾࠩᙯ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack1l1ll111l1_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack1lllll1l1l1_opy_(fixturedef.argname):
        store[bstack11ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡯ࡴࡦ࡯ࠪᙰ")] = request.node
    elif bstack1llllll111l_opy_(fixturedef.argname):
        store[bstack11ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡣ࡭ࡣࡶࡷࡤ࡯ࡴࡦ࡯ࠪᙱ")] = request.node
    outcome = yield
    try:
        fixture = {
            bstack11ll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᙲ"): fixturedef.argname,
            bstack11ll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᙳ"): bstack11l11lll11_opy_(outcome),
            bstack11ll_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪᙴ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack11ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭ᙵ")]
        if not _11llll1ll1_opy_.get(current_test_item.nodeid, None):
            _11llll1ll1_opy_[current_test_item.nodeid] = {bstack11ll_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬᙶ"): []}
        _11llll1ll1_opy_[current_test_item.nodeid][bstack11ll_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭ᙷ")].append(fixture)
    except Exception as err:
        logger.debug(bstack11ll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࡤࡹࡥࡵࡷࡳ࠾ࠥࢁࡽࠨᙸ"), str(err))
if bstack111l1lll1_opy_() and bstack1l1ll111l1_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _11llll1ll1_opy_[request.node.nodeid][bstack11ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᙹ")].bstack1llll11l1l1_opy_(id(step))
        except Exception as err:
            print(bstack11ll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰ࠻ࠢࡾࢁࠬᙺ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _11llll1ll1_opy_[request.node.nodeid][bstack11ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᙻ")].bstack11lll1l1l1_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack11ll_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡹࡴࡦࡲࡢࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂ࠭ᙼ"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack11lll1l1ll_opy_: bstack1l1111ll1l_opy_ = _11llll1ll1_opy_[request.node.nodeid][bstack11ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᙽ")]
            bstack11lll1l1ll_opy_.bstack11lll1l1l1_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack11ll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡴࡶࡨࡴࡤ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠨᙾ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1lll11ll111_opy_
        try:
            if not bstack1l1ll111l1_opy_.on() or bstack1lll11ll111_opy_ != bstack11ll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠩᙿ"):
                return
            global bstack11lllll11l_opy_
            bstack11lllll11l_opy_.start()
            driver = bstack1ll1l111ll_opy_(threading.current_thread(), bstack11ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ "), None)
            if not _11llll1ll1_opy_.get(request.node.nodeid, None):
                _11llll1ll1_opy_[request.node.nodeid] = {}
            bstack11lll1l1ll_opy_ = bstack1l1111ll1l_opy_.bstack1llll1l111l_opy_(
                scenario, feature, request.node,
                name=bstack1lllll1llll_opy_(request.node, scenario),
                bstack1l111ll11l_opy_=bstack1llll1llll_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack11ll_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺ࠭ࡤࡷࡦࡹࡲࡨࡥࡳࠩᚁ"),
                tags=bstack1lllll1l1ll_opy_(feature, scenario),
                bstack11lllll1l1_opy_=bstack1l1ll111l1_opy_.bstack11lll11l1l_opy_(driver) if driver and driver.session_id else {}
            )
            _11llll1ll1_opy_[request.node.nodeid][bstack11ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᚂ")] = bstack11lll1l1ll_opy_
            bstack1lll11l11ll_opy_(bstack11lll1l1ll_opy_.uuid)
            bstack1l1ll111l1_opy_.bstack1l111lllll_opy_(bstack11ll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᚃ"), bstack11lll1l1ll_opy_)
        except Exception as err:
            print(bstack11ll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯࠻ࠢࡾࢁࠬᚄ"), str(err))
def bstack1lll1l1ll11_opy_(bstack1lll11lll1l_opy_):
    if bstack1lll11lll1l_opy_ in store[bstack11ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᚅ")]:
        store[bstack11ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᚆ")].remove(bstack1lll11lll1l_opy_)
def bstack1lll11l11ll_opy_(bstack1lll11l1111_opy_):
    store[bstack11ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᚇ")] = bstack1lll11l1111_opy_
    threading.current_thread().current_test_uuid = bstack1lll11l1111_opy_
@bstack1l1ll111l1_opy_.bstack1lll1lll11l_opy_
def bstack1lll1l111ll_opy_(item, call, report):
    global bstack1lll11ll111_opy_
    bstack1l1lllll_opy_ = bstack1llll1llll_opy_()
    if hasattr(report, bstack11ll_opy_ (u"ࠧࡴࡶࡲࡴࠬᚈ")):
        bstack1l1lllll_opy_ = bstack11l1111lll_opy_(report.stop)
    elif hasattr(report, bstack11ll_opy_ (u"ࠨࡵࡷࡥࡷࡺࠧᚉ")):
        bstack1l1lllll_opy_ = bstack11l1111lll_opy_(report.start)
    try:
        if getattr(report, bstack11ll_opy_ (u"ࠩࡺ࡬ࡪࡴࠧᚊ"), bstack11ll_opy_ (u"ࠪࠫᚋ")) == bstack11ll_opy_ (u"ࠫࡨࡧ࡬࡭ࠩᚌ"):
            bstack11lllll11l_opy_.reset()
        if getattr(report, bstack11ll_opy_ (u"ࠬࡽࡨࡦࡰࠪᚍ"), bstack11ll_opy_ (u"࠭ࠧᚎ")) == bstack11ll_opy_ (u"ࠧࡤࡣ࡯ࡰࠬᚏ"):
            if bstack1lll11ll111_opy_ == bstack11ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨᚐ"):
                _11llll1ll1_opy_[item.nodeid][bstack11ll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᚑ")] = bstack1l1lllll_opy_
                bstack1lll1l1l11l_opy_(item, _11llll1ll1_opy_[item.nodeid], bstack11ll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᚒ"), report, call)
                store[bstack11ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᚓ")] = None
            elif bstack1lll11ll111_opy_ == bstack11ll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠤᚔ"):
                bstack11lll1l1ll_opy_ = _11llll1ll1_opy_[item.nodeid][bstack11ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᚕ")]
                bstack11lll1l1ll_opy_.set(hooks=_11llll1ll1_opy_[item.nodeid].get(bstack11ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᚖ"), []))
                exception, bstack1l11111l1l_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack1l11111l1l_opy_ = [call.excinfo.exconly(), getattr(report, bstack11ll_opy_ (u"ࠨ࡮ࡲࡲ࡬ࡸࡥࡱࡴࡷࡩࡽࡺࠧᚗ"), bstack11ll_opy_ (u"ࠩࠪᚘ"))]
                bstack11lll1l1ll_opy_.stop(time=bstack1l1lllll_opy_, result=Result(result=getattr(report, bstack11ll_opy_ (u"ࠪࡳࡺࡺࡣࡰ࡯ࡨࠫᚙ"), bstack11ll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᚚ")), exception=exception, bstack1l11111l1l_opy_=bstack1l11111l1l_opy_))
                bstack1l1ll111l1_opy_.bstack1l111lllll_opy_(bstack11ll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ᚛"), _11llll1ll1_opy_[item.nodeid][bstack11ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ᚜")])
        elif getattr(report, bstack11ll_opy_ (u"ࠧࡸࡪࡨࡲࠬ᚝"), bstack11ll_opy_ (u"ࠨࠩ᚞")) in [bstack11ll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ᚟"), bstack11ll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬᚠ")]:
            bstack11llllll11_opy_ = item.nodeid + bstack11ll_opy_ (u"ࠫ࠲࠭ᚡ") + getattr(report, bstack11ll_opy_ (u"ࠬࡽࡨࡦࡰࠪᚢ"), bstack11ll_opy_ (u"࠭ࠧᚣ"))
            if getattr(report, bstack11ll_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᚤ"), False):
                hook_type = bstack11ll_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭ᚥ") if getattr(report, bstack11ll_opy_ (u"ࠩࡺ࡬ࡪࡴࠧᚦ"), bstack11ll_opy_ (u"ࠪࠫᚧ")) == bstack11ll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪᚨ") else bstack11ll_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩᚩ")
                _11llll1ll1_opy_[bstack11llllll11_opy_] = {
                    bstack11ll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᚪ"): uuid4().__str__(),
                    bstack11ll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᚫ"): bstack1l1lllll_opy_,
                    bstack11ll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫᚬ"): hook_type
                }
            _11llll1ll1_opy_[bstack11llllll11_opy_][bstack11ll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᚭ")] = bstack1l1lllll_opy_
            bstack1lll1l1ll11_opy_(_11llll1ll1_opy_[bstack11llllll11_opy_][bstack11ll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᚮ")])
            bstack1lll1l11l1l_opy_(item, _11llll1ll1_opy_[bstack11llllll11_opy_], bstack11ll_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᚯ"), report, call)
            if getattr(report, bstack11ll_opy_ (u"ࠬࡽࡨࡦࡰࠪᚰ"), bstack11ll_opy_ (u"࠭ࠧᚱ")) == bstack11ll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ᚲ"):
                if getattr(report, bstack11ll_opy_ (u"ࠨࡱࡸࡸࡨࡵ࡭ࡦࠩᚳ"), bstack11ll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᚴ")) == bstack11ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᚵ"):
                    bstack1l1111lll1_opy_ = {
                        bstack11ll_opy_ (u"ࠫࡺࡻࡩࡥࠩᚶ"): uuid4().__str__(),
                        bstack11ll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᚷ"): bstack1llll1llll_opy_(),
                        bstack11ll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᚸ"): bstack1llll1llll_opy_()
                    }
                    _11llll1ll1_opy_[item.nodeid] = {**_11llll1ll1_opy_[item.nodeid], **bstack1l1111lll1_opy_}
                    bstack1lll1l1l11l_opy_(item, _11llll1ll1_opy_[item.nodeid], bstack11ll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᚹ"))
                    bstack1lll1l1l11l_opy_(item, _11llll1ll1_opy_[item.nodeid], bstack11ll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᚺ"), report, call)
    except Exception as err:
        print(bstack11ll_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡤࡲࡩࡲࡥࡠࡱ࠴࠵ࡾࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶ࠽ࠤࢀࢃࠧᚻ"), str(err))
def bstack1lll11l111l_opy_(test, bstack1l1111lll1_opy_, result=None, call=None, bstack1111lll1l_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack11lll1l1ll_opy_ = {
        bstack11ll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᚼ"): bstack1l1111lll1_opy_[bstack11ll_opy_ (u"ࠫࡺࡻࡩࡥࠩᚽ")],
        bstack11ll_opy_ (u"ࠬࡺࡹࡱࡧࠪᚾ"): bstack11ll_opy_ (u"࠭ࡴࡦࡵࡷࠫᚿ"),
        bstack11ll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᛀ"): test.name,
        bstack11ll_opy_ (u"ࠨࡤࡲࡨࡾ࠭ᛁ"): {
            bstack11ll_opy_ (u"ࠩ࡯ࡥࡳ࡭ࠧᛂ"): bstack11ll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪᛃ"),
            bstack11ll_opy_ (u"ࠫࡨࡵࡤࡦࠩᛄ"): inspect.getsource(test.obj)
        },
        bstack11ll_opy_ (u"ࠬ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᛅ"): test.name,
        bstack11ll_opy_ (u"࠭ࡳࡤࡱࡳࡩࠬᛆ"): test.name,
        bstack11ll_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧᛇ"): bstack1l1ll111l1_opy_.bstack11lll1l111_opy_(test),
        bstack11ll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫᛈ"): file_path,
        bstack11ll_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫᛉ"): file_path,
        bstack11ll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᛊ"): bstack11ll_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬᛋ"),
        bstack11ll_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪᛌ"): file_path,
        bstack11ll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᛍ"): bstack1l1111lll1_opy_[bstack11ll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᛎ")],
        bstack11ll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᛏ"): bstack11ll_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩᛐ"),
        bstack11ll_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡕࡩࡷࡻ࡮ࡑࡣࡵࡥࡲ࠭ᛑ"): {
            bstack11ll_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡢࡲࡦࡳࡥࠨᛒ"): test.nodeid
        },
        bstack11ll_opy_ (u"ࠬࡺࡡࡨࡵࠪᛓ"): bstack11l11l1lll_opy_(test.own_markers)
    }
    if bstack1111lll1l_opy_ in [bstack11ll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧᛔ"), bstack11ll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᛕ")]:
        bstack11lll1l1ll_opy_[bstack11ll_opy_ (u"ࠨ࡯ࡨࡸࡦ࠭ᛖ")] = {
            bstack11ll_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫᛗ"): bstack1l1111lll1_opy_.get(bstack11ll_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬᛘ"), [])
        }
    if bstack1111lll1l_opy_ == bstack11ll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬᛙ"):
        bstack11lll1l1ll_opy_[bstack11ll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᛚ")] = bstack11ll_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᛛ")
        bstack11lll1l1ll_opy_[bstack11ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᛜ")] = bstack1l1111lll1_opy_[bstack11ll_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᛝ")]
        bstack11lll1l1ll_opy_[bstack11ll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᛞ")] = bstack1l1111lll1_opy_[bstack11ll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᛟ")]
    if result:
        bstack11lll1l1ll_opy_[bstack11ll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᛠ")] = result.outcome
        bstack11lll1l1ll_opy_[bstack11ll_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭ᛡ")] = result.duration * 1000
        bstack11lll1l1ll_opy_[bstack11ll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᛢ")] = bstack1l1111lll1_opy_[bstack11ll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᛣ")]
        if result.failed:
            bstack11lll1l1ll_opy_[bstack11ll_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧᛤ")] = bstack1l1ll111l1_opy_.bstack11ll1l1l11_opy_(call.excinfo.typename)
            bstack11lll1l1ll_opy_[bstack11ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᛥ")] = bstack1l1ll111l1_opy_.bstack1lll1ll1ll1_opy_(call.excinfo, result)
        bstack11lll1l1ll_opy_[bstack11ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᛦ")] = bstack1l1111lll1_opy_[bstack11ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᛧ")]
    if outcome:
        bstack11lll1l1ll_opy_[bstack11ll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᛨ")] = bstack11l11lll11_opy_(outcome)
        bstack11lll1l1ll_opy_[bstack11ll_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧᛩ")] = 0
        bstack11lll1l1ll_opy_[bstack11ll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᛪ")] = bstack1l1111lll1_opy_[bstack11ll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭᛫")]
        if bstack11lll1l1ll_opy_[bstack11ll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ᛬")] == bstack11ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ᛭"):
            bstack11lll1l1ll_opy_[bstack11ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪᛮ")] = bstack11ll_opy_ (u"࡛ࠬ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷ࠭ᛯ")  # bstack1lll11lllll_opy_
            bstack11lll1l1ll_opy_[bstack11ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᛰ")] = [{bstack11ll_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᛱ"): [bstack11ll_opy_ (u"ࠨࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠬᛲ")]}]
        bstack11lll1l1ll_opy_[bstack11ll_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᛳ")] = bstack1l1111lll1_opy_[bstack11ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᛴ")]
    return bstack11lll1l1ll_opy_
def bstack1lll11l1lll_opy_(test, bstack11llll1111_opy_, bstack1111lll1l_opy_, result, call, outcome, bstack1lll111lll1_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack11llll1111_opy_[bstack11ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧᛵ")]
    hook_name = bstack11llll1111_opy_[bstack11ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨᛶ")]
    hook_data = {
        bstack11ll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᛷ"): bstack11llll1111_opy_[bstack11ll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᛸ")],
        bstack11ll_opy_ (u"ࠨࡶࡼࡴࡪ࠭᛹"): bstack11ll_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ᛺"),
        bstack11ll_opy_ (u"ࠪࡲࡦࡳࡥࠨ᛻"): bstack11ll_opy_ (u"ࠫࢀࢃࠧ᛼").format(bstack1llllll1111_opy_(hook_name)),
        bstack11ll_opy_ (u"ࠬࡨ࡯ࡥࡻࠪ᛽"): {
            bstack11ll_opy_ (u"࠭࡬ࡢࡰࡪࠫ᛾"): bstack11ll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ᛿"),
            bstack11ll_opy_ (u"ࠨࡥࡲࡨࡪ࠭ᜀ"): None
        },
        bstack11ll_opy_ (u"ࠩࡶࡧࡴࡶࡥࠨᜁ"): test.name,
        bstack11ll_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪᜂ"): bstack1l1ll111l1_opy_.bstack11lll1l111_opy_(test, hook_name),
        bstack11ll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧᜃ"): file_path,
        bstack11ll_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠧᜄ"): file_path,
        bstack11ll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᜅ"): bstack11ll_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨᜆ"),
        bstack11ll_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭ᜇ"): file_path,
        bstack11ll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᜈ"): bstack11llll1111_opy_[bstack11ll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᜉ")],
        bstack11ll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᜊ"): bstack11ll_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸ࠲ࡩࡵࡤࡷࡰࡦࡪࡸࠧᜋ") if bstack1lll11ll111_opy_ == bstack11ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪᜌ") else bstack11ll_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺࠧᜍ"),
        bstack11ll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫᜎ"): hook_type
    }
    bstack1lll1l1l1ll_opy_ = bstack11lllll1ll_opy_(_11llll1ll1_opy_.get(test.nodeid, None))
    if bstack1lll1l1l1ll_opy_:
        hook_data[bstack11ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣ࡮ࡪࠧᜏ")] = bstack1lll1l1l1ll_opy_
    if result:
        hook_data[bstack11ll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᜐ")] = result.outcome
        hook_data[bstack11ll_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬᜑ")] = result.duration * 1000
        hook_data[bstack11ll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᜒ")] = bstack11llll1111_opy_[bstack11ll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᜓ")]
        if result.failed:
            hook_data[bstack11ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ᜔࠭")] = bstack1l1ll111l1_opy_.bstack11ll1l1l11_opy_(call.excinfo.typename)
            hook_data[bstack11ll_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦ᜕ࠩ")] = bstack1l1ll111l1_opy_.bstack1lll1ll1ll1_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack11ll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ᜖")] = bstack11l11lll11_opy_(outcome)
        hook_data[bstack11ll_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫ᜗")] = 100
        hook_data[bstack11ll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ᜘")] = bstack11llll1111_opy_[bstack11ll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ᜙")]
        if hook_data[bstack11ll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭᜚")] == bstack11ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ᜛"):
            hook_data[bstack11ll_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧ᜜")] = bstack11ll_opy_ (u"ࠩࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠪ᜝")  # bstack1lll11lllll_opy_
            hook_data[bstack11ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫ᜞")] = [{bstack11ll_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᜟ"): [bstack11ll_opy_ (u"ࠬࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠩᜠ")]}]
    if bstack1lll111lll1_opy_:
        hook_data[bstack11ll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᜡ")] = bstack1lll111lll1_opy_.result
        hook_data[bstack11ll_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨᜢ")] = bstack11l1111l1l_opy_(bstack11llll1111_opy_[bstack11ll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᜣ")], bstack11llll1111_opy_[bstack11ll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᜤ")])
        hook_data[bstack11ll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᜥ")] = bstack11llll1111_opy_[bstack11ll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᜦ")]
        if hook_data[bstack11ll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᜧ")] == bstack11ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᜨ"):
            hook_data[bstack11ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭ᜩ")] = bstack1l1ll111l1_opy_.bstack11ll1l1l11_opy_(bstack1lll111lll1_opy_.exception_type)
            hook_data[bstack11ll_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩᜪ")] = [{bstack11ll_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬᜫ"): bstack11l111l111_opy_(bstack1lll111lll1_opy_.exception)}]
    return hook_data
def bstack1lll1l1l11l_opy_(test, bstack1l1111lll1_opy_, bstack1111lll1l_opy_, result=None, call=None, outcome=None):
    bstack11lll1l1ll_opy_ = bstack1lll11l111l_opy_(test, bstack1l1111lll1_opy_, result, call, bstack1111lll1l_opy_, outcome)
    driver = getattr(test, bstack11ll_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫᜬ"), None)
    if bstack1111lll1l_opy_ == bstack11ll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᜭ") and driver:
        bstack11lll1l1ll_opy_[bstack11ll_opy_ (u"ࠬ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࠫᜮ")] = bstack1l1ll111l1_opy_.bstack11lll11l1l_opy_(driver)
    if bstack1111lll1l_opy_ == bstack11ll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧᜯ"):
        bstack1111lll1l_opy_ = bstack11ll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᜰ")
    bstack11lll1ll1l_opy_ = {
        bstack11ll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᜱ"): bstack1111lll1l_opy_,
        bstack11ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫᜲ"): bstack11lll1l1ll_opy_
    }
    bstack1l1ll111l1_opy_.bstack1l1111l1l1_opy_(bstack11lll1ll1l_opy_)
def bstack1lll1l11l1l_opy_(test, bstack1l1111lll1_opy_, bstack1111lll1l_opy_, result=None, call=None, outcome=None, bstack1lll111lll1_opy_=None):
    hook_data = bstack1lll11l1lll_opy_(test, bstack1l1111lll1_opy_, bstack1111lll1l_opy_, result, call, outcome, bstack1lll111lll1_opy_)
    bstack11lll1ll1l_opy_ = {
        bstack11ll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᜳ"): bstack1111lll1l_opy_,
        bstack11ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳ᜴࠭"): hook_data
    }
    bstack1l1ll111l1_opy_.bstack1l1111l1l1_opy_(bstack11lll1ll1l_opy_)
def bstack11lllll1ll_opy_(bstack1l1111lll1_opy_):
    if not bstack1l1111lll1_opy_:
        return None
    if bstack1l1111lll1_opy_.get(bstack11ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ᜵"), None):
        return getattr(bstack1l1111lll1_opy_[bstack11ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ᜶")], bstack11ll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ᜷"), None)
    return bstack1l1111lll1_opy_.get(bstack11ll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭᜸"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack1l1ll111l1_opy_.on():
            return
        places = [bstack11ll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ᜹"), bstack11ll_opy_ (u"ࠪࡧࡦࡲ࡬ࠨ᜺"), bstack11ll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭᜻")]
        bstack1l111l11ll_opy_ = []
        for bstack1lll11l1ll1_opy_ in places:
            records = caplog.get_records(bstack1lll11l1ll1_opy_)
            bstack1lll11llll1_opy_ = bstack11ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ᜼") if bstack1lll11l1ll1_opy_ == bstack11ll_opy_ (u"࠭ࡣࡢ࡮࡯ࠫ᜽") else bstack11ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ᜾")
            bstack1lll1l1l111_opy_ = request.node.nodeid + (bstack11ll_opy_ (u"ࠨࠩ᜿") if bstack1lll11l1ll1_opy_ == bstack11ll_opy_ (u"ࠩࡦࡥࡱࡲࠧᝀ") else bstack11ll_opy_ (u"ࠪ࠱ࠬᝁ") + bstack1lll11l1ll1_opy_)
            bstack1lll11l1111_opy_ = bstack11lllll1ll_opy_(_11llll1ll1_opy_.get(bstack1lll1l1l111_opy_, None))
            if not bstack1lll11l1111_opy_:
                continue
            for record in records:
                if bstack111ll1ll11_opy_(record.message):
                    continue
                bstack1l111l11ll_opy_.append({
                    bstack11ll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᝂ"): datetime.datetime.utcfromtimestamp(record.created).isoformat() + bstack11ll_opy_ (u"ࠬࡠࠧᝃ"),
                    bstack11ll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᝄ"): record.levelname,
                    bstack11ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᝅ"): record.message,
                    bstack1lll11llll1_opy_: bstack1lll11l1111_opy_
                })
        if len(bstack1l111l11ll_opy_) > 0:
            bstack1l1ll111l1_opy_.bstack1l1ll11l_opy_(bstack1l111l11ll_opy_)
    except Exception as err:
        print(bstack11ll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡧࡦࡳࡳࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥ࠻ࠢࡾࢁࠬᝆ"), str(err))
def bstack1llll1l11_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack1l1l1l111_opy_
    bstack1l1l1l1l_opy_ = bstack1ll1l111ll_opy_(threading.current_thread(), bstack11ll_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ᝇ"), None) and bstack1ll1l111ll_opy_(
            threading.current_thread(), bstack11ll_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᝈ"), None)
    bstack1l1111lll_opy_ = getattr(driver, bstack11ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫᝉ"), None) != None and getattr(driver, bstack11ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬᝊ"), None) == True
    if sequence == bstack11ll_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭ᝋ") and driver != None:
      if not bstack1l1l1l111_opy_ and bstack11l11l11l1_opy_() and bstack11ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᝌ") in CONFIG and CONFIG[bstack11ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᝍ")] == True and bstack1l1l1l1ll_opy_.bstack111l1llll_opy_(driver_command) and (bstack1l1111lll_opy_ or bstack1l1l1l1l_opy_) and not bstack1l1ll1111_opy_(args):
        try:
          bstack1l1l1l111_opy_ = True
          logger.debug(bstack11ll_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤ࡫ࡵࡲࠡࡽࢀࠫᝎ").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack11ll_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡦࡴࡩࡳࡷࡳࠠࡴࡥࡤࡲࠥࢁࡽࠨᝏ").format(str(err)))
        bstack1l1l1l111_opy_ = False
    if sequence == bstack11ll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪᝐ"):
        if driver_command == bstack11ll_opy_ (u"ࠬࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠩᝑ"):
            bstack1l1ll111l1_opy_.bstack1111l1l11_opy_({
                bstack11ll_opy_ (u"࠭ࡩ࡮ࡣࡪࡩࠬᝒ"): response[bstack11ll_opy_ (u"ࠧࡷࡣ࡯ࡹࡪ࠭ᝓ")],
                bstack11ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ᝔"): store[bstack11ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭᝕")]
            })
def bstack1llll11l11_opy_():
    global bstack1111111l1_opy_
    bstack1ll1l11l11_opy_.bstack111l1l1l1_opy_()
    logging.shutdown()
    bstack1l1ll111l1_opy_.bstack11lll1l11l_opy_()
    for driver in bstack1111111l1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1lll1l11ll1_opy_(*args):
    global bstack1111111l1_opy_
    bstack1l1ll111l1_opy_.bstack11lll1l11l_opy_()
    for driver in bstack1111111l1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack11lll111l_opy_(self, *args, **kwargs):
    bstack1lll1ll1l_opy_ = bstack11l1lll1_opy_(self, *args, **kwargs)
    bstack1l1ll111l1_opy_.bstack1ll1ll1ll_opy_(self)
    return bstack1lll1ll1l_opy_
def bstack1l1llll1_opy_(framework_name):
    global bstack1l11ll1ll_opy_
    global bstack11l1l1l1_opy_
    bstack1l11ll1ll_opy_ = framework_name
    logger.info(bstack1ll111l1ll_opy_.format(bstack1l11ll1ll_opy_.split(bstack11ll_opy_ (u"ࠪ࠱ࠬ᝖"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack11l11l11l1_opy_():
            Service.start = bstack1ll11ll11_opy_
            Service.stop = bstack1l1ll1llll_opy_
            webdriver.Remote.__init__ = bstack1l11llll1l_opy_
            webdriver.Remote.get = bstack1l1llll111_opy_
            if not isinstance(os.getenv(bstack11ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡆࡘࡁࡍࡎࡈࡐࠬ᝗")), str):
                return
            WebDriver.close = bstack1111l11l_opy_
            WebDriver.quit = bstack1l11l1111_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        if not bstack11l11l11l1_opy_() and bstack1l1ll111l1_opy_.on():
            webdriver.Remote.__init__ = bstack11lll111l_opy_
        bstack11l1l1l1_opy_ = True
    except Exception as e:
        pass
    bstack1111l11l1_opy_()
    if os.environ.get(bstack11ll_opy_ (u"࡙ࠬࡅࡍࡇࡑࡍ࡚ࡓ࡟ࡐࡔࡢࡔࡑࡇ࡙ࡘࡔࡌࡋࡍ࡚࡟ࡊࡐࡖࡘࡆࡒࡌࡆࡆࠪ᝘")):
        bstack11l1l1l1_opy_ = eval(os.environ.get(bstack11ll_opy_ (u"࠭ࡓࡆࡎࡈࡒࡎ࡛ࡍࡠࡑࡕࡣࡕࡒࡁ࡚࡙ࡕࡍࡌࡎࡔࡠࡋࡑࡗ࡙ࡇࡌࡍࡇࡇࠫ᝙")))
    if not bstack11l1l1l1_opy_:
        bstack1l111l11l_opy_(bstack11ll_opy_ (u"ࠢࡑࡣࡦ࡯ࡦ࡭ࡥࡴࠢࡱࡳࡹࠦࡩ࡯ࡵࡷࡥࡱࡲࡥࡥࠤ᝚"), bstack11l111l11_opy_)
    if bstack1llll11ll1_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._get_proxy_url = bstack1l1lll1ll1_opy_
        except Exception as e:
            logger.error(bstack1ll1llll1_opy_.format(str(e)))
    if bstack11ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ᝛") in str(framework_name).lower():
        if not bstack11l11l11l1_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1ll1111ll_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack11111111_opy_
            Config.getoption = bstack1l1l111l1l_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1lll1lll1l_opy_
        except Exception as e:
            pass
def bstack1l11l1111_opy_(self):
    global bstack1l11ll1ll_opy_
    global bstack1l11lllll_opy_
    global bstack11lll111_opy_
    try:
        if bstack11ll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ᝜") in bstack1l11ll1ll_opy_ and self.session_id != None and bstack1ll1l111ll_opy_(threading.current_thread(), bstack11ll_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧ᝝"), bstack11ll_opy_ (u"ࠫࠬ᝞")) != bstack11ll_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭᝟"):
            bstack1l111ll1_opy_ = bstack11ll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᝠ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᝡ")
            bstack1111l11ll_opy_(logger, True)
            if self != None:
                bstack1l1l11l11_opy_(self, bstack1l111ll1_opy_, bstack11ll_opy_ (u"ࠨ࠮ࠣࠫᝢ").join(threading.current_thread().bstackTestErrorMessages))
        item = store.get(bstack11ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭ᝣ"), None)
        if item is not None and bstack1lll111ll1l_opy_:
            bstack11l1l1ll_opy_.bstack1l111llll_opy_(self, bstack111llllll_opy_, logger, item)
        threading.current_thread().testStatus = bstack11ll_opy_ (u"ࠪࠫᝤ")
    except Exception as e:
        logger.debug(bstack11ll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࠧᝥ") + str(e))
    bstack11lll111_opy_(self)
    self.session_id = None
def bstack1l11llll1l_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1l11lllll_opy_
    global bstack1lll1l11l_opy_
    global bstack1ll1l11l_opy_
    global bstack1l11ll1ll_opy_
    global bstack11l1lll1_opy_
    global bstack1111111l1_opy_
    global bstack1l1l111ll_opy_
    global bstack1111ll1ll_opy_
    global bstack1lll111ll1l_opy_
    global bstack111llllll_opy_
    CONFIG[bstack11ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧᝦ")] = str(bstack1l11ll1ll_opy_) + str(__version__)
    command_executor = bstack1ll11l1l_opy_(bstack1l1l111ll_opy_)
    logger.debug(bstack1ll1ll1ll1_opy_.format(command_executor))
    proxy = bstack11111111l_opy_(CONFIG, proxy)
    bstack1l1l111l_opy_ = 0
    try:
        if bstack1ll1l11l_opy_ is True:
            bstack1l1l111l_opy_ = int(os.environ.get(bstack11ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᝧ")))
    except:
        bstack1l1l111l_opy_ = 0
    bstack1l1l1l1lll_opy_ = bstack1llll1l111_opy_(CONFIG, bstack1l1l111l_opy_)
    logger.debug(bstack11ll11l1l_opy_.format(str(bstack1l1l1l1lll_opy_)))
    bstack111llllll_opy_ = CONFIG.get(bstack11ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᝨ"))[bstack1l1l111l_opy_]
    if bstack11ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᝩ") in CONFIG and CONFIG[bstack11ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᝪ")]:
        bstack1l1l1l11l1_opy_(bstack1l1l1l1lll_opy_, bstack1111ll1ll_opy_)
    if bstack1l1l11111l_opy_.bstack11llll111_opy_(CONFIG, bstack1l1l111l_opy_) and bstack1l1l11111l_opy_.bstack1l11l1ll1l_opy_(bstack1l1l1l1lll_opy_, options):
        bstack1lll111ll1l_opy_ = True
        bstack1l1l11111l_opy_.set_capabilities(bstack1l1l1l1lll_opy_, CONFIG)
    if desired_capabilities:
        bstack11llll1ll_opy_ = bstack1l11ll1l1l_opy_(desired_capabilities)
        bstack11llll1ll_opy_[bstack11ll_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪᝫ")] = bstack1ll1l11lll_opy_(CONFIG)
        bstack1l1l1l1l11_opy_ = bstack1llll1l111_opy_(bstack11llll1ll_opy_)
        if bstack1l1l1l1l11_opy_:
            bstack1l1l1l1lll_opy_ = update(bstack1l1l1l1l11_opy_, bstack1l1l1l1lll_opy_)
        desired_capabilities = None
    if options:
        bstack1ll1111lll_opy_(options, bstack1l1l1l1lll_opy_)
    if not options:
        options = bstack11l111l1l_opy_(bstack1l1l1l1lll_opy_)
    if proxy and bstack1ll11lll_opy_() >= version.parse(bstack11ll_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫᝬ")):
        options.proxy(proxy)
    if options and bstack1ll11lll_opy_() >= version.parse(bstack11ll_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫ᝭")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1ll11lll_opy_() < version.parse(bstack11ll_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬᝮ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1l1l1l1lll_opy_)
    logger.info(bstack11lll1111_opy_)
    if bstack1ll11lll_opy_() >= version.parse(bstack11ll_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧᝯ")):
        bstack11l1lll1_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1ll11lll_opy_() >= version.parse(bstack11ll_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧᝰ")):
        bstack11l1lll1_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1ll11lll_opy_() >= version.parse(bstack11ll_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩ᝱")):
        bstack11l1lll1_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack11l1lll1_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack1l111lll1_opy_ = bstack11ll_opy_ (u"ࠪࠫᝲ")
        if bstack1ll11lll_opy_() >= version.parse(bstack11ll_opy_ (u"ࠫ࠹࠴࠰࠯࠲ࡥ࠵ࠬᝳ")):
            bstack1l111lll1_opy_ = self.caps.get(bstack11ll_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧ᝴"))
        else:
            bstack1l111lll1_opy_ = self.capabilities.get(bstack11ll_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨ᝵"))
        if bstack1l111lll1_opy_:
            bstack1l1l1ll11_opy_(bstack1l111lll1_opy_)
            if bstack1ll11lll_opy_() <= version.parse(bstack11ll_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧ᝶")):
                self.command_executor._url = bstack11ll_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ᝷") + bstack1l1l111ll_opy_ + bstack11ll_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨ᝸")
            else:
                self.command_executor._url = bstack11ll_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧ᝹") + bstack1l111lll1_opy_ + bstack11ll_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧ᝺")
            logger.debug(bstack1l111l11_opy_.format(bstack1l111lll1_opy_))
        else:
            logger.debug(bstack1ll1llll11_opy_.format(bstack11ll_opy_ (u"ࠧࡕࡰࡵ࡫ࡰࡥࡱࠦࡈࡶࡤࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠨ᝻")))
    except Exception as e:
        logger.debug(bstack1ll1llll11_opy_.format(e))
    bstack1l11lllll_opy_ = self.session_id
    if bstack11ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭᝼") in bstack1l11ll1ll_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack11ll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ᝽"), None)
        if item:
            bstack1lll1l11111_opy_ = getattr(item, bstack11ll_opy_ (u"ࠨࡡࡷࡩࡸࡺ࡟ࡤࡣࡶࡩࡤࡹࡴࡢࡴࡷࡩࡩ࠭᝾"), False)
            if not getattr(item, bstack11ll_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪ᝿"), None) and bstack1lll1l11111_opy_:
                setattr(store[bstack11ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧក")], bstack11ll_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬខ"), self)
        bstack1l1ll111l1_opy_.bstack1ll1ll1ll_opy_(self)
    bstack1111111l1_opy_.append(self)
    if bstack11ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨគ") in CONFIG and bstack11ll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫឃ") in CONFIG[bstack11ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪង")][bstack1l1l111l_opy_]:
        bstack1lll1l11l_opy_ = CONFIG[bstack11ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫច")][bstack1l1l111l_opy_][bstack11ll_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧឆ")]
    logger.debug(bstack11l11l1l1_opy_.format(bstack1l11lllll_opy_))
def bstack1l1llll111_opy_(self, url):
    global bstack1l1ll111l_opy_
    global CONFIG
    try:
        bstack1ll111l111_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1l111111_opy_.format(str(err)))
    try:
        bstack1l1ll111l_opy_(self, url)
    except Exception as e:
        try:
            bstack1ll11lll1l_opy_ = str(e)
            if any(err_msg in bstack1ll11lll1l_opy_ for err_msg in bstack11l1lll11_opy_):
                bstack1ll111l111_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1l111111_opy_.format(str(err)))
        raise e
def bstack1l1111ll_opy_(item, when):
    global bstack111lll11_opy_
    try:
        bstack111lll11_opy_(item, when)
    except Exception as e:
        pass
def bstack1lll1lll1l_opy_(item, call, rep):
    global bstack1l11lllll1_opy_
    global bstack1111111l1_opy_
    name = bstack11ll_opy_ (u"ࠪࠫជ")
    try:
        if rep.when == bstack11ll_opy_ (u"ࠫࡨࡧ࡬࡭ࠩឈ"):
            bstack1l11lllll_opy_ = threading.current_thread().bstackSessionId
            bstack1lll1l111l1_opy_ = item.config.getoption(bstack11ll_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧញ"))
            try:
                if (str(bstack1lll1l111l1_opy_).lower() != bstack11ll_opy_ (u"࠭ࡴࡳࡷࡨࠫដ")):
                    name = str(rep.nodeid)
                    bstack1l11l1ll11_opy_ = bstack1lllll111l_opy_(bstack11ll_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨឋ"), name, bstack11ll_opy_ (u"ࠨࠩឌ"), bstack11ll_opy_ (u"ࠩࠪឍ"), bstack11ll_opy_ (u"ࠪࠫណ"), bstack11ll_opy_ (u"ࠫࠬត"))
                    os.environ[bstack11ll_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨថ")] = name
                    for driver in bstack1111111l1_opy_:
                        if bstack1l11lllll_opy_ == driver.session_id:
                            driver.execute_script(bstack1l11l1ll11_opy_)
            except Exception as e:
                logger.debug(bstack11ll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠠࡧࡱࡵࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡵࡨࡷࡸ࡯࡯࡯࠼ࠣࡿࢂ࠭ទ").format(str(e)))
            try:
                bstack111l1l11l_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack11ll_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨធ"):
                    status = bstack11ll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨន") if rep.outcome.lower() == bstack11ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩប") else bstack11ll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪផ")
                    reason = bstack11ll_opy_ (u"ࠫࠬព")
                    if status == bstack11ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬភ"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack11ll_opy_ (u"࠭ࡩ࡯ࡨࡲࠫម") if status == bstack11ll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧយ") else bstack11ll_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧរ")
                    data = name + bstack11ll_opy_ (u"ࠩࠣࡴࡦࡹࡳࡦࡦࠤࠫល") if status == bstack11ll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪវ") else name + bstack11ll_opy_ (u"ࠫࠥ࡬ࡡࡪ࡮ࡨࡨࠦࠦࠧឝ") + reason
                    bstack1lll11l1_opy_ = bstack1lllll111l_opy_(bstack11ll_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧឞ"), bstack11ll_opy_ (u"࠭ࠧស"), bstack11ll_opy_ (u"ࠧࠨហ"), bstack11ll_opy_ (u"ࠨࠩឡ"), level, data)
                    for driver in bstack1111111l1_opy_:
                        if bstack1l11lllll_opy_ == driver.session_id:
                            driver.execute_script(bstack1lll11l1_opy_)
            except Exception as e:
                logger.debug(bstack11ll_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡣࡰࡰࡷࡩࡽࡺࠠࡧࡱࡵࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡵࡨࡷࡸ࡯࡯࡯࠼ࠣࡿࢂ࠭អ").format(str(e)))
    except Exception as e:
        logger.debug(bstack11ll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡵࡣࡷࡩࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࢀࢃࠧឣ").format(str(e)))
    bstack1l11lllll1_opy_(item, call, rep)
notset = Notset()
def bstack1l1l111l1l_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1llll1ll_opy_
    if str(name).lower() == bstack11ll_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࠫឤ"):
        return bstack11ll_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠦឥ")
    else:
        return bstack1llll1ll_opy_(self, name, default, skip)
def bstack1l1lll1ll1_opy_(self):
    global CONFIG
    global bstack1l1l1lll1l_opy_
    try:
        proxy = bstack1ll111lll1_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack11ll_opy_ (u"࠭࠮ࡱࡣࡦࠫឦ")):
                proxies = bstack11l1ll11l_opy_(proxy, bstack1ll11l1l_opy_())
                if len(proxies) > 0:
                    protocol, bstack1ll1l1111l_opy_ = proxies.popitem()
                    if bstack11ll_opy_ (u"ࠢ࠻࠱࠲ࠦឧ") in bstack1ll1l1111l_opy_:
                        return bstack1ll1l1111l_opy_
                    else:
                        return bstack11ll_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤឨ") + bstack1ll1l1111l_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack11ll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡶࡲࡰࡺࡼࠤࡺࡸ࡬ࠡ࠼ࠣࡿࢂࠨឩ").format(str(e)))
    return bstack1l1l1lll1l_opy_(self)
def bstack1llll11ll1_opy_():
    return (bstack11ll_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ឪ") in CONFIG or bstack11ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨឫ") in CONFIG) and bstack1111lll1_opy_() and bstack1ll11lll_opy_() >= version.parse(
        bstack1l1ll11l1l_opy_)
def bstack1l11l1l1l_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack1lll1l11l_opy_
    global bstack1ll1l11l_opy_
    global bstack1l11ll1ll_opy_
    CONFIG[bstack11ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧឬ")] = str(bstack1l11ll1ll_opy_) + str(__version__)
    bstack1l1l111l_opy_ = 0
    try:
        if bstack1ll1l11l_opy_ is True:
            bstack1l1l111l_opy_ = int(os.environ.get(bstack11ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ឭ")))
    except:
        bstack1l1l111l_opy_ = 0
    CONFIG[bstack11ll_opy_ (u"ࠢࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨឮ")] = True
    bstack1l1l1l1lll_opy_ = bstack1llll1l111_opy_(CONFIG, bstack1l1l111l_opy_)
    logger.debug(bstack11ll11l1l_opy_.format(str(bstack1l1l1l1lll_opy_)))
    if CONFIG.get(bstack11ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬឯ")):
        bstack1l1l1l11l1_opy_(bstack1l1l1l1lll_opy_, bstack1111ll1ll_opy_)
    if bstack11ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬឰ") in CONFIG and bstack11ll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨឱ") in CONFIG[bstack11ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧឲ")][bstack1l1l111l_opy_]:
        bstack1lll1l11l_opy_ = CONFIG[bstack11ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨឳ")][bstack1l1l111l_opy_][bstack11ll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ឴")]
    import urllib
    import json
    bstack111ll11l_opy_ = bstack11ll_opy_ (u"ࠧࡸࡵࡶ࠾࠴࠵ࡣࡥࡲ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡂࡧࡦࡶࡳ࠾ࠩ឵") + urllib.parse.quote(json.dumps(bstack1l1l1l1lll_opy_))
    browser = self.connect(bstack111ll11l_opy_)
    return browser
def bstack1111l11l1_opy_():
    global bstack11l1l1l1_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1l11l1l1l_opy_
        bstack11l1l1l1_opy_ = True
    except Exception as e:
        pass
def bstack1lll11ll1l1_opy_():
    global CONFIG
    global bstack1lllll11_opy_
    global bstack1l1l111ll_opy_
    global bstack1111ll1ll_opy_
    global bstack1ll1l11l_opy_
    global bstack1l11l1lll_opy_
    CONFIG = json.loads(os.environ.get(bstack11ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍࠧា")))
    bstack1lllll11_opy_ = eval(os.environ.get(bstack11ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪិ")))
    bstack1l1l111ll_opy_ = os.environ.get(bstack11ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡋ࡙ࡇࡥࡕࡓࡎࠪី"))
    bstack11lll11l_opy_(CONFIG, bstack1lllll11_opy_)
    bstack1l11l1lll_opy_ = bstack1ll1l11l11_opy_.bstack1111l1l1l_opy_(CONFIG, bstack1l11l1lll_opy_)
    global bstack11l1lll1_opy_
    global bstack11lll111_opy_
    global bstack1l1ll11ll_opy_
    global bstack1l1l1lll11_opy_
    global bstack1l1ll11111_opy_
    global bstack1l1lll1ll_opy_
    global bstack1ll11ll1l_opy_
    global bstack1l1ll111l_opy_
    global bstack1l1l1lll1l_opy_
    global bstack1llll1ll_opy_
    global bstack111lll11_opy_
    global bstack1l11lllll1_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack11l1lll1_opy_ = webdriver.Remote.__init__
        bstack11lll111_opy_ = WebDriver.quit
        bstack1ll11ll1l_opy_ = WebDriver.close
        bstack1l1ll111l_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack11ll_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧឹ") in CONFIG or bstack11ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩឺ") in CONFIG) and bstack1111lll1_opy_():
        if bstack1ll11lll_opy_() < version.parse(bstack1l1ll11l1l_opy_):
            logger.error(bstack1ll11lll1_opy_.format(bstack1ll11lll_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack1l1l1lll1l_opy_ = RemoteConnection._get_proxy_url
            except Exception as e:
                logger.error(bstack1ll1llll1_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1llll1ll_opy_ = Config.getoption
        from _pytest import runner
        bstack111lll11_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack1l11lll1l_opy_)
    try:
        from pytest_bdd import reporting
        bstack1l11lllll1_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack11ll_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹࡵࠠࡳࡷࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࡹࠧុ"))
    bstack1111ll1ll_opy_ = CONFIG.get(bstack11ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫូ"), {}).get(bstack11ll_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪួ"))
    bstack1ll1l11l_opy_ = True
    bstack1l1llll1_opy_(bstack1ll11l111_opy_)
if (bstack11l111lll1_opy_()):
    bstack1lll11ll1l1_opy_()
@bstack1l111l1l1l_opy_(class_method=False)
def bstack1lll111llll_opy_(hook_name, event, bstack1lll11l1l1l_opy_=None):
    if hook_name not in [bstack11ll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪើ"), bstack11ll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧឿ"), bstack11ll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪៀ"), bstack11ll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧេ"), bstack11ll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫែ"), bstack11ll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨៃ"), bstack11ll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧោ"), bstack11ll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫៅ")]:
        return
    node = store[bstack11ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧំ")]
    if hook_name in [bstack11ll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪះ"), bstack11ll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧៈ")]:
        node = store[bstack11ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡪࡶࡨࡱࠬ៉")]
    elif hook_name in [bstack11ll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬ៊"), bstack11ll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩ់")]:
        node = store[bstack11ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡧࡱࡧࡳࡴࡡ࡬ࡸࡪࡳࠧ៌")]
    if event == bstack11ll_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪ៍"):
        hook_type = bstack1lllll1lll1_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack11llll1111_opy_ = {
            bstack11ll_opy_ (u"ࠫࡺࡻࡩࡥࠩ៎"): uuid,
            bstack11ll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ៏"): bstack1llll1llll_opy_(),
            bstack11ll_opy_ (u"࠭ࡴࡺࡲࡨࠫ័"): bstack11ll_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ៑"),
            bstack11ll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨ្ࠫ"): hook_type,
            bstack11ll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬ៓"): hook_name
        }
        store[bstack11ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ។")].append(uuid)
        bstack1lll111ll11_opy_ = node.nodeid
        if hook_type == bstack11ll_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩ៕"):
            if not _11llll1ll1_opy_.get(bstack1lll111ll11_opy_, None):
                _11llll1ll1_opy_[bstack1lll111ll11_opy_] = {bstack11ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ៖"): []}
            _11llll1ll1_opy_[bstack1lll111ll11_opy_][bstack11ll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬៗ")].append(bstack11llll1111_opy_[bstack11ll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ៘")])
        _11llll1ll1_opy_[bstack1lll111ll11_opy_ + bstack11ll_opy_ (u"ࠨ࠯ࠪ៙") + hook_name] = bstack11llll1111_opy_
        bstack1lll1l11l1l_opy_(node, bstack11llll1111_opy_, bstack11ll_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ៚"))
    elif event == bstack11ll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩ៛"):
        bstack11llllll11_opy_ = node.nodeid + bstack11ll_opy_ (u"ࠫ࠲࠭ៜ") + hook_name
        _11llll1ll1_opy_[bstack11llllll11_opy_][bstack11ll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ៝")] = bstack1llll1llll_opy_()
        bstack1lll1l1ll11_opy_(_11llll1ll1_opy_[bstack11llllll11_opy_][bstack11ll_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ៞")])
        bstack1lll1l11l1l_opy_(node, _11llll1ll1_opy_[bstack11llllll11_opy_], bstack11ll_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ៟"), bstack1lll111lll1_opy_=bstack1lll11l1l1l_opy_)
def bstack1lll11ll1ll_opy_():
    global bstack1lll11ll111_opy_
    if bstack111l1lll1_opy_():
        bstack1lll11ll111_opy_ = bstack11ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬ០")
    else:
        bstack1lll11ll111_opy_ = bstack11ll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ១")
@bstack1l1ll111l1_opy_.bstack1lll1lll11l_opy_
def bstack1lll11l1l11_opy_():
    bstack1lll11ll1ll_opy_()
    if bstack1111lll1_opy_():
        bstack1ll111l1l_opy_(bstack1llll1l11_opy_)
    try:
        bstack111l1l1ll1_opy_(bstack1lll111llll_opy_)
    except Exception as e:
        logger.debug(bstack11ll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࡳࠡࡲࡤࡸࡨ࡮࠺ࠡࡽࢀࠦ២").format(e))
bstack1lll11l1l11_opy_()