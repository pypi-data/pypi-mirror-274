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
import datetime
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack11llll111l_opy_ import RobotHandler
from bstack_utils.capture import bstack1l1111l11l_opy_
from bstack_utils.bstack11lll1l1ll_opy_ import bstack1l11111ll1_opy_, bstack1l111111l1_opy_, bstack1l1111ll1l_opy_
from bstack_utils.bstack11ll11111_opy_ import bstack1l1ll111l1_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1ll1l111ll_opy_, bstack1llll1llll_opy_, Result, \
    bstack1l111l1l1l_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack11ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭൅"): [],
        bstack11ll_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩെ"): [],
        bstack11ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨേ"): []
    }
    bstack11lllll111_opy_ = []
    bstack1l111l1111_opy_ = []
    @staticmethod
    def bstack1l11l111ll_opy_(log):
        if not (log[bstack11ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ൈ")] and log[bstack11ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ൉")].strip()):
            return
        active = bstack1l1ll111l1_opy_.bstack11llllllll_opy_()
        log = {
            bstack11ll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ൊ"): log[bstack11ll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧോ")],
            bstack11ll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬൌ"): datetime.datetime.utcnow().isoformat() + bstack11ll_opy_ (u"ࠪ࡞്ࠬ"),
            bstack11ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬൎ"): log[bstack11ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭൏")],
        }
        if active:
            if active[bstack11ll_opy_ (u"࠭ࡴࡺࡲࡨࠫ൐")] == bstack11ll_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ൑"):
                log[bstack11ll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ൒")] = active[bstack11ll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ൓")]
            elif active[bstack11ll_opy_ (u"ࠪࡸࡾࡶࡥࠨൔ")] == bstack11ll_opy_ (u"ࠫࡹ࡫ࡳࡵࠩൕ"):
                log[bstack11ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬൖ")] = active[bstack11ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ൗ")]
        bstack1l1ll111l1_opy_.bstack1l1ll11l_opy_([log])
    def __init__(self):
        self.messages = Messages()
        self._11lll11ll1_opy_ = None
        self._1l111llll1_opy_ = None
        self._11llll1ll1_opy_ = OrderedDict()
        self.bstack11lllll11l_opy_ = bstack1l1111l11l_opy_(self.bstack1l11l111ll_opy_)
    @bstack1l111l1l1l_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack11lll1lll1_opy_()
        if not self._11llll1ll1_opy_.get(attrs.get(bstack11ll_opy_ (u"ࠧࡪࡦࠪ൘")), None):
            self._11llll1ll1_opy_[attrs.get(bstack11ll_opy_ (u"ࠨ࡫ࡧࠫ൙"))] = {}
        bstack1l1111l111_opy_ = bstack1l1111ll1l_opy_(
                bstack11lll1llll_opy_=attrs.get(bstack11ll_opy_ (u"ࠩ࡬ࡨࠬ൚")),
                name=name,
                bstack1l111ll11l_opy_=bstack1llll1llll_opy_(),
                file_path=os.path.relpath(attrs[bstack11ll_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ൛")], start=os.getcwd()) if attrs.get(bstack11ll_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ൜")) != bstack11ll_opy_ (u"ࠬ࠭൝") else bstack11ll_opy_ (u"࠭ࠧ൞"),
                framework=bstack11ll_opy_ (u"ࠧࡓࡱࡥࡳࡹ࠭ൟ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack11ll_opy_ (u"ࠨ࡫ࡧࠫൠ"), None)
        self._11llll1ll1_opy_[attrs.get(bstack11ll_opy_ (u"ࠩ࡬ࡨࠬൡ"))][bstack11ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ൢ")] = bstack1l1111l111_opy_
    @bstack1l111l1l1l_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack1l11111111_opy_()
        self._11lllllll1_opy_(messages)
        for bstack1l111l1l11_opy_ in self.bstack11lllll111_opy_:
            bstack1l111l1l11_opy_[bstack11ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭ൣ")][bstack11ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ൤")].extend(self.store[bstack11ll_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬ൥")])
            bstack1l1ll111l1_opy_.bstack1l1111l1l1_opy_(bstack1l111l1l11_opy_)
        self.bstack11lllll111_opy_ = []
        self.store[bstack11ll_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭൦")] = []
    @bstack1l111l1l1l_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack11lllll11l_opy_.start()
        if not self._11llll1ll1_opy_.get(attrs.get(bstack11ll_opy_ (u"ࠨ࡫ࡧࠫ൧")), None):
            self._11llll1ll1_opy_[attrs.get(bstack11ll_opy_ (u"ࠩ࡬ࡨࠬ൨"))] = {}
        driver = bstack1ll1l111ll_opy_(threading.current_thread(), bstack11ll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ൩"), None)
        bstack11lll1l1ll_opy_ = bstack1l1111ll1l_opy_(
            bstack11lll1llll_opy_=attrs.get(bstack11ll_opy_ (u"ࠫ࡮ࡪࠧ൪")),
            name=name,
            bstack1l111ll11l_opy_=bstack1llll1llll_opy_(),
            file_path=os.path.relpath(attrs[bstack11ll_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ൫")], start=os.getcwd()),
            scope=RobotHandler.bstack11lll1l111_opy_(attrs.get(bstack11ll_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭൬"), None)),
            framework=bstack11ll_opy_ (u"ࠧࡓࡱࡥࡳࡹ࠭൭"),
            tags=attrs[bstack11ll_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭൮")],
            hooks=self.store[bstack11ll_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨ൯")],
            bstack11lllll1l1_opy_=bstack1l1ll111l1_opy_.bstack11lll11l1l_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack11ll_opy_ (u"ࠥࡿࢂࠦ࡜࡯ࠢࡾࢁࠧ൰").format(bstack11ll_opy_ (u"ࠦࠥࠨ൱").join(attrs[bstack11ll_opy_ (u"ࠬࡺࡡࡨࡵࠪ൲")]), name) if attrs[bstack11ll_opy_ (u"࠭ࡴࡢࡩࡶࠫ൳")] else name
        )
        self._11llll1ll1_opy_[attrs.get(bstack11ll_opy_ (u"ࠧࡪࡦࠪ൴"))][bstack11ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ൵")] = bstack11lll1l1ll_opy_
        threading.current_thread().current_test_uuid = bstack11lll1l1ll_opy_.bstack11lll11lll_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack11ll_opy_ (u"ࠩ࡬ࡨࠬ൶"), None)
        self.bstack1l111lllll_opy_(bstack11ll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ൷"), bstack11lll1l1ll_opy_)
    @bstack1l111l1l1l_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack11lllll11l_opy_.reset()
        bstack1l111l111l_opy_ = bstack11lll1ll11_opy_.get(attrs.get(bstack11ll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ൸")), bstack11ll_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭൹"))
        self._11llll1ll1_opy_[attrs.get(bstack11ll_opy_ (u"࠭ࡩࡥࠩൺ"))][bstack11ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪൻ")].stop(time=bstack1llll1llll_opy_(), duration=int(attrs.get(bstack11ll_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭ർ"), bstack11ll_opy_ (u"ࠩ࠳ࠫൽ"))), result=Result(result=bstack1l111l111l_opy_, exception=attrs.get(bstack11ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫൾ")), bstack1l11111l1l_opy_=[attrs.get(bstack11ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬൿ"))]))
        self.bstack1l111lllll_opy_(bstack11ll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ඀"), self._11llll1ll1_opy_[attrs.get(bstack11ll_opy_ (u"࠭ࡩࡥࠩඁ"))][bstack11ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪං")], True)
        self.store[bstack11ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬඃ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack1l111l1l1l_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack11lll1lll1_opy_()
        current_test_id = bstack1ll1l111ll_opy_(threading.current_thread(), bstack11ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫ඄"), None)
        bstack1l111l11l1_opy_ = current_test_id if bstack1ll1l111ll_opy_(threading.current_thread(), bstack11ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡨࠬඅ"), None) else bstack1ll1l111ll_opy_(threading.current_thread(), bstack11ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡹࡵࡪࡶࡨࡣ࡮ࡪࠧආ"), None)
        if attrs.get(bstack11ll_opy_ (u"ࠬࡺࡹࡱࡧࠪඇ"), bstack11ll_opy_ (u"࠭ࠧඈ")).lower() in [bstack11ll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ඉ"), bstack11ll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪඊ")]:
            hook_type = bstack1l1111llll_opy_(attrs.get(bstack11ll_opy_ (u"ࠩࡷࡽࡵ࡫ࠧඋ")), bstack1ll1l111ll_opy_(threading.current_thread(), bstack11ll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧඌ"), None))
            hook_name = bstack11ll_opy_ (u"ࠫࢀࢃࠧඍ").format(attrs.get(bstack11ll_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬඎ"), bstack11ll_opy_ (u"࠭ࠧඏ")))
            if hook_type in [bstack11ll_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫඐ"), bstack11ll_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫඑ")]:
                hook_name = bstack11ll_opy_ (u"ࠩ࡞ࡿࢂࡣࠠࡼࡿࠪඒ").format(bstack11llll11l1_opy_.get(hook_type), attrs.get(bstack11ll_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪඓ"), bstack11ll_opy_ (u"ࠫࠬඔ")))
            bstack11llll1111_opy_ = bstack1l111111l1_opy_(
                bstack11lll1llll_opy_=bstack1l111l11l1_opy_ + bstack11ll_opy_ (u"ࠬ࠳ࠧඕ") + attrs.get(bstack11ll_opy_ (u"࠭ࡴࡺࡲࡨࠫඖ"), bstack11ll_opy_ (u"ࠧࠨ඗")).lower(),
                name=hook_name,
                bstack1l111ll11l_opy_=bstack1llll1llll_opy_(),
                file_path=os.path.relpath(attrs.get(bstack11ll_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ඘")), start=os.getcwd()),
                framework=bstack11ll_opy_ (u"ࠩࡕࡳࡧࡵࡴࠨ඙"),
                tags=attrs[bstack11ll_opy_ (u"ࠪࡸࡦ࡭ࡳࠨක")],
                scope=RobotHandler.bstack11lll1l111_opy_(attrs.get(bstack11ll_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫඛ"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack11llll1111_opy_.bstack11lll11lll_opy_()
            threading.current_thread().current_hook_id = bstack1l111l11l1_opy_ + bstack11ll_opy_ (u"ࠬ࠳ࠧග") + attrs.get(bstack11ll_opy_ (u"࠭ࡴࡺࡲࡨࠫඝ"), bstack11ll_opy_ (u"ࠧࠨඞ")).lower()
            self.store[bstack11ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬඟ")] = [bstack11llll1111_opy_.bstack11lll11lll_opy_()]
            if bstack1ll1l111ll_opy_(threading.current_thread(), bstack11ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ච"), None):
                self.store[bstack11ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧඡ")].append(bstack11llll1111_opy_.bstack11lll11lll_opy_())
            else:
                self.store[bstack11ll_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪජ")].append(bstack11llll1111_opy_.bstack11lll11lll_opy_())
            if bstack1l111l11l1_opy_:
                self._11llll1ll1_opy_[bstack1l111l11l1_opy_ + bstack11ll_opy_ (u"ࠬ࠳ࠧඣ") + attrs.get(bstack11ll_opy_ (u"࠭ࡴࡺࡲࡨࠫඤ"), bstack11ll_opy_ (u"ࠧࠨඥ")).lower()] = { bstack11ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫඦ"): bstack11llll1111_opy_ }
            bstack1l1ll111l1_opy_.bstack1l111lllll_opy_(bstack11ll_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪට"), bstack11llll1111_opy_)
        else:
            bstack1l111ll1ll_opy_ = {
                bstack11ll_opy_ (u"ࠪ࡭ࡩ࠭ඨ"): uuid4().__str__(),
                bstack11ll_opy_ (u"ࠫࡹ࡫ࡸࡵࠩඩ"): bstack11ll_opy_ (u"ࠬࢁࡽࠡࡽࢀࠫඪ").format(attrs.get(bstack11ll_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭ණ")), attrs.get(bstack11ll_opy_ (u"ࠧࡢࡴࡪࡷࠬඬ"), bstack11ll_opy_ (u"ࠨࠩත"))) if attrs.get(bstack11ll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧථ"), []) else attrs.get(bstack11ll_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪද")),
                bstack11ll_opy_ (u"ࠫࡸࡺࡥࡱࡡࡤࡶ࡬ࡻ࡭ࡦࡰࡷࠫධ"): attrs.get(bstack11ll_opy_ (u"ࠬࡧࡲࡨࡵࠪන"), []),
                bstack11ll_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ඲"): bstack1llll1llll_opy_(),
                bstack11ll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧඳ"): bstack11ll_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩප"),
                bstack11ll_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧඵ"): attrs.get(bstack11ll_opy_ (u"ࠪࡨࡴࡩࠧබ"), bstack11ll_opy_ (u"ࠫࠬභ"))
            }
            if attrs.get(bstack11ll_opy_ (u"ࠬࡲࡩࡣࡰࡤࡱࡪ࠭ම"), bstack11ll_opy_ (u"࠭ࠧඹ")) != bstack11ll_opy_ (u"ࠧࠨය"):
                bstack1l111ll1ll_opy_[bstack11ll_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩර")] = attrs.get(bstack11ll_opy_ (u"ࠩ࡯࡭ࡧࡴࡡ࡮ࡧࠪ඼"))
            if not self.bstack1l111l1111_opy_:
                self._11llll1ll1_opy_[self._1l111lll11_opy_()][bstack11ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ල")].add_step(bstack1l111ll1ll_opy_)
                threading.current_thread().current_step_uuid = bstack1l111ll1ll_opy_[bstack11ll_opy_ (u"ࠫ࡮ࡪࠧ඾")]
            self.bstack1l111l1111_opy_.append(bstack1l111ll1ll_opy_)
    @bstack1l111l1l1l_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack1l11111111_opy_()
        self._11lllllll1_opy_(messages)
        current_test_id = bstack1ll1l111ll_opy_(threading.current_thread(), bstack11ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪࠧ඿"), None)
        bstack1l111l11l1_opy_ = current_test_id if current_test_id else bstack1ll1l111ll_opy_(threading.current_thread(), bstack11ll_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡷ࡬ࡸࡪࡥࡩࡥࠩව"), None)
        bstack1l111l1lll_opy_ = bstack11lll1ll11_opy_.get(attrs.get(bstack11ll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧශ")), bstack11ll_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩෂ"))
        bstack1l11l111l1_opy_ = attrs.get(bstack11ll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪස"))
        if bstack1l111l1lll_opy_ != bstack11ll_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫහ") and not attrs.get(bstack11ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬළ")) and self._11lll11ll1_opy_:
            bstack1l11l111l1_opy_ = self._11lll11ll1_opy_
        bstack1l11111l11_opy_ = Result(result=bstack1l111l1lll_opy_, exception=bstack1l11l111l1_opy_, bstack1l11111l1l_opy_=[bstack1l11l111l1_opy_])
        if attrs.get(bstack11ll_opy_ (u"ࠬࡺࡹࡱࡧࠪෆ"), bstack11ll_opy_ (u"࠭ࠧ෇")).lower() in [bstack11ll_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭෈"), bstack11ll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ෉")]:
            bstack1l111l11l1_opy_ = current_test_id if current_test_id else bstack1ll1l111ll_opy_(threading.current_thread(), bstack11ll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡷࡺ࡯ࡴࡦࡡ࡬ࡨ්ࠬ"), None)
            if bstack1l111l11l1_opy_:
                bstack11llllll11_opy_ = bstack1l111l11l1_opy_ + bstack11ll_opy_ (u"ࠥ࠱ࠧ෋") + attrs.get(bstack11ll_opy_ (u"ࠫࡹࡿࡰࡦࠩ෌"), bstack11ll_opy_ (u"ࠬ࠭෍")).lower()
                self._11llll1ll1_opy_[bstack11llllll11_opy_][bstack11ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ෎")].stop(time=bstack1llll1llll_opy_(), duration=int(attrs.get(bstack11ll_opy_ (u"ࠧࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩࠬා"), bstack11ll_opy_ (u"ࠨ࠲ࠪැ"))), result=bstack1l11111l11_opy_)
                bstack1l1ll111l1_opy_.bstack1l111lllll_opy_(bstack11ll_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫෑ"), self._11llll1ll1_opy_[bstack11llllll11_opy_][bstack11ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ි")])
        else:
            bstack1l111l11l1_opy_ = current_test_id if current_test_id else bstack1ll1l111ll_opy_(threading.current_thread(), bstack11ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢ࡭ࡩ࠭ී"), None)
            if bstack1l111l11l1_opy_ and len(self.bstack1l111l1111_opy_) == 1:
                current_step_uuid = bstack1ll1l111ll_opy_(threading.current_thread(), bstack11ll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡵࡧࡳࡣࡺࡻࡩࡥࠩු"), None)
                self._11llll1ll1_opy_[bstack1l111l11l1_opy_][bstack11ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ෕")].bstack11lll1l1l1_opy_(current_step_uuid, duration=int(attrs.get(bstack11ll_opy_ (u"ࠧࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩࠬූ"), bstack11ll_opy_ (u"ࠨ࠲ࠪ෗"))), result=bstack1l11111l11_opy_)
            else:
                self.bstack1l111ll1l1_opy_(attrs)
            self.bstack1l111l1111_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack11ll_opy_ (u"ࠩ࡫ࡸࡲࡲࠧෘ"), bstack11ll_opy_ (u"ࠪࡲࡴ࠭ෙ")) == bstack11ll_opy_ (u"ࠫࡾ࡫ࡳࠨේ"):
                return
            self.messages.push(message)
            bstack1l111l11ll_opy_ = []
            if bstack1l1ll111l1_opy_.bstack11llllllll_opy_():
                bstack1l111l11ll_opy_.append({
                    bstack11ll_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨෛ"): bstack1llll1llll_opy_(),
                    bstack11ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧො"): message.get(bstack11ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨෝ")),
                    bstack11ll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧෞ"): message.get(bstack11ll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨෟ")),
                    **bstack1l1ll111l1_opy_.bstack11llllllll_opy_()
                })
                if len(bstack1l111l11ll_opy_) > 0:
                    bstack1l1ll111l1_opy_.bstack1l1ll11l_opy_(bstack1l111l11ll_opy_)
        except Exception as err:
            pass
    def close(self):
        bstack1l1ll111l1_opy_.bstack11lll1l11l_opy_()
    def bstack1l111ll1l1_opy_(self, bstack1l11l1111l_opy_):
        if not bstack1l1ll111l1_opy_.bstack11llllllll_opy_():
            return
        kwname = bstack11ll_opy_ (u"ࠪࡿࢂࠦࡻࡾࠩ෠").format(bstack1l11l1111l_opy_.get(bstack11ll_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫ෡")), bstack1l11l1111l_opy_.get(bstack11ll_opy_ (u"ࠬࡧࡲࡨࡵࠪ෢"), bstack11ll_opy_ (u"࠭ࠧ෣"))) if bstack1l11l1111l_opy_.get(bstack11ll_opy_ (u"ࠧࡢࡴࡪࡷࠬ෤"), []) else bstack1l11l1111l_opy_.get(bstack11ll_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨ෥"))
        error_message = bstack11ll_opy_ (u"ࠤ࡮ࡻࡳࡧ࡭ࡦ࠼ࠣࡠࠧࢁ࠰ࡾ࡞ࠥࠤࢁࠦࡳࡵࡣࡷࡹࡸࡀࠠ࡝ࠤࡾ࠵ࢂࡢࠢࠡࡾࠣࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠ࡝ࠤࡾ࠶ࢂࡢࠢࠣ෦").format(kwname, bstack1l11l1111l_opy_.get(bstack11ll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ෧")), str(bstack1l11l1111l_opy_.get(bstack11ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ෨"))))
        bstack11llllll1l_opy_ = bstack11ll_opy_ (u"ࠧࡱࡷ࡯ࡣࡰࡩ࠿ࠦ࡜ࠣࡽ࠳ࢁࡡࠨࠠࡽࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡠࠧࢁ࠱ࡾ࡞ࠥࠦ෩").format(kwname, bstack1l11l1111l_opy_.get(bstack11ll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭෪")))
        bstack1l1111l1ll_opy_ = error_message if bstack1l11l1111l_opy_.get(bstack11ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ෫")) else bstack11llllll1l_opy_
        bstack11llll1l1l_opy_ = {
            bstack11ll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ෬"): self.bstack1l111l1111_opy_[-1].get(bstack11ll_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭෭"), bstack1llll1llll_opy_()),
            bstack11ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ෮"): bstack1l1111l1ll_opy_,
            bstack11ll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ෯"): bstack11ll_opy_ (u"ࠬࡋࡒࡓࡑࡕࠫ෰") if bstack1l11l1111l_opy_.get(bstack11ll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭෱")) == bstack11ll_opy_ (u"ࠧࡇࡃࡌࡐࠬෲ") else bstack11ll_opy_ (u"ࠨࡋࡑࡊࡔ࠭ෳ"),
            **bstack1l1ll111l1_opy_.bstack11llllllll_opy_()
        }
        bstack1l1ll111l1_opy_.bstack1l1ll11l_opy_([bstack11llll1l1l_opy_])
    def _1l111lll11_opy_(self):
        for bstack11lll1llll_opy_ in reversed(self._11llll1ll1_opy_):
            bstack1l111111ll_opy_ = bstack11lll1llll_opy_
            data = self._11llll1ll1_opy_[bstack11lll1llll_opy_][bstack11ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ෴")]
            if isinstance(data, bstack1l111111l1_opy_):
                if not bstack11ll_opy_ (u"ࠪࡉࡆࡉࡈࠨ෵") in data.bstack11llll11ll_opy_():
                    return bstack1l111111ll_opy_
            else:
                return bstack1l111111ll_opy_
    def _11lllllll1_opy_(self, messages):
        try:
            bstack1l1111ll11_opy_ = BuiltIn().get_variable_value(bstack11ll_opy_ (u"ࠦࠩࢁࡌࡐࡉࠣࡐࡊ࡜ࡅࡍࡿࠥ෶")) in (bstack11llll1lll_opy_.DEBUG, bstack11llll1lll_opy_.TRACE)
            for message, bstack11llll1l11_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack11ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭෷"))
                level = message.get(bstack11ll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ෸"))
                if level == bstack11llll1lll_opy_.FAIL:
                    self._11lll11ll1_opy_ = name or self._11lll11ll1_opy_
                    self._1l111llll1_opy_ = bstack11llll1l11_opy_.get(bstack11ll_opy_ (u"ࠢ࡮ࡧࡶࡷࡦ࡭ࡥࠣ෹")) if bstack1l1111ll11_opy_ and bstack11llll1l11_opy_ else self._1l111llll1_opy_
        except:
            pass
    @classmethod
    def bstack1l111lllll_opy_(self, event: str, bstack1l111ll111_opy_: bstack1l11111ll1_opy_, bstack1l11l11l11_opy_=False):
        if event == bstack11ll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ෺"):
            bstack1l111ll111_opy_.set(hooks=self.store[bstack11ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭෻")])
        if event == bstack11ll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫ෼"):
            event = bstack11ll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭෽")
        if bstack1l11l11l11_opy_:
            bstack11lll1ll1l_opy_ = {
                bstack11ll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ෾"): event,
                bstack1l111ll111_opy_.bstack1l11111lll_opy_(): bstack1l111ll111_opy_.bstack1l111lll1l_opy_(event)
            }
            self.bstack11lllll111_opy_.append(bstack11lll1ll1l_opy_)
        else:
            bstack1l1ll111l1_opy_.bstack1l111lllll_opy_(event, bstack1l111ll111_opy_)
class Messages:
    def __init__(self):
        self._1l1111111l_opy_ = []
    def bstack11lll1lll1_opy_(self):
        self._1l1111111l_opy_.append([])
    def bstack1l11111111_opy_(self):
        return self._1l1111111l_opy_.pop() if self._1l1111111l_opy_ else list()
    def push(self, message):
        self._1l1111111l_opy_[-1].append(message) if self._1l1111111l_opy_ else self._1l1111111l_opy_.append([message])
class bstack11llll1lll_opy_:
    FAIL = bstack11ll_opy_ (u"࠭ࡆࡂࡋࡏࠫ෿")
    ERROR = bstack11ll_opy_ (u"ࠧࡆࡔࡕࡓࡗ࠭฀")
    WARNING = bstack11ll_opy_ (u"ࠨ࡙ࡄࡖࡓ࠭ก")
    bstack1l11l11111_opy_ = bstack11ll_opy_ (u"ࠩࡌࡒࡋࡕࠧข")
    DEBUG = bstack11ll_opy_ (u"ࠪࡈࡊࡈࡕࡈࠩฃ")
    TRACE = bstack11ll_opy_ (u"࡙ࠫࡘࡁࡄࡇࠪค")
    bstack1l111l1ll1_opy_ = [FAIL, ERROR]
def bstack11lllll1ll_opy_(bstack1l1111lll1_opy_):
    if not bstack1l1111lll1_opy_:
        return None
    if bstack1l1111lll1_opy_.get(bstack11ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨฅ"), None):
        return getattr(bstack1l1111lll1_opy_[bstack11ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩฆ")], bstack11ll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬง"), None)
    return bstack1l1111lll1_opy_.get(bstack11ll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭จ"), None)
def bstack1l1111llll_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack11ll_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨฉ"), bstack11ll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬช")]:
        return
    if hook_type.lower() == bstack11ll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪซ"):
        if current_test_uuid is None:
            return bstack11ll_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩฌ")
        else:
            return bstack11ll_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫญ")
    elif hook_type.lower() == bstack11ll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩฎ"):
        if current_test_uuid is None:
            return bstack11ll_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫฏ")
        else:
            return bstack11ll_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭ฐ")