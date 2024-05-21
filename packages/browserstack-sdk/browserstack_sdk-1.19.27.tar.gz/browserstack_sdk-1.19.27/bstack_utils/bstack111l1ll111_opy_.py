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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack11l11l1111_opy_
from browserstack_sdk.bstack1llll1111l_opy_ import bstack11l1l1ll_opy_
def _111l1lll11_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack111l1l1ll1_opy_:
    def __init__(self, handler):
        self._111l1llll1_opy_ = {}
        self._111l1ll1ll_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack11l1l1ll_opy_.version()
        if bstack11l11l1111_opy_(pytest_version, bstack11ll_opy_ (u"ࠦ࠽࠴࠱࠯࠳ࠥጡ")) >= 0:
            self._111l1llll1_opy_[bstack11ll_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨጢ")] = Module._register_setup_function_fixture
            self._111l1llll1_opy_[bstack11ll_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧጣ")] = Module._register_setup_module_fixture
            self._111l1llll1_opy_[bstack11ll_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧጤ")] = Class._register_setup_class_fixture
            self._111l1llll1_opy_[bstack11ll_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩጥ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack111ll1111l_opy_(bstack11ll_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬጦ"))
            Module._register_setup_module_fixture = self.bstack111ll1111l_opy_(bstack11ll_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫጧ"))
            Class._register_setup_class_fixture = self.bstack111ll1111l_opy_(bstack11ll_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫጨ"))
            Class._register_setup_method_fixture = self.bstack111ll1111l_opy_(bstack11ll_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ጩ"))
        else:
            self._111l1llll1_opy_[bstack11ll_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩጪ")] = Module._inject_setup_function_fixture
            self._111l1llll1_opy_[bstack11ll_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨጫ")] = Module._inject_setup_module_fixture
            self._111l1llll1_opy_[bstack11ll_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨጬ")] = Class._inject_setup_class_fixture
            self._111l1llll1_opy_[bstack11ll_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪጭ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack111ll1111l_opy_(bstack11ll_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ጮ"))
            Module._inject_setup_module_fixture = self.bstack111ll1111l_opy_(bstack11ll_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬጯ"))
            Class._inject_setup_class_fixture = self.bstack111ll1111l_opy_(bstack11ll_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠬጰ"))
            Class._inject_setup_method_fixture = self.bstack111ll1111l_opy_(bstack11ll_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠧጱ"))
    def bstack111l1l1l1l_opy_(self, bstack111l1ll11l_opy_, hook_type):
        meth = getattr(bstack111l1ll11l_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._111l1ll1ll_opy_[hook_type] = meth
            setattr(bstack111l1ll11l_opy_, hook_type, self.bstack111l1ll1l1_opy_(hook_type))
    def bstack111ll11111_opy_(self, instance, bstack111l1lll1l_opy_):
        if bstack111l1lll1l_opy_ == bstack11ll_opy_ (u"ࠢࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠥጲ"):
            self.bstack111l1l1l1l_opy_(instance.obj, bstack11ll_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠤጳ"))
            self.bstack111l1l1l1l_opy_(instance.obj, bstack11ll_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠨጴ"))
        if bstack111l1lll1l_opy_ == bstack11ll_opy_ (u"ࠥࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠦጵ"):
            self.bstack111l1l1l1l_opy_(instance.obj, bstack11ll_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠥጶ"))
            self.bstack111l1l1l1l_opy_(instance.obj, bstack11ll_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠢጷ"))
        if bstack111l1lll1l_opy_ == bstack11ll_opy_ (u"ࠨࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪࠨጸ"):
            self.bstack111l1l1l1l_opy_(instance.obj, bstack11ll_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠧጹ"))
            self.bstack111l1l1l1l_opy_(instance.obj, bstack11ll_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠤጺ"))
        if bstack111l1lll1l_opy_ == bstack11ll_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠥጻ"):
            self.bstack111l1l1l1l_opy_(instance.obj, bstack11ll_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠤጼ"))
            self.bstack111l1l1l1l_opy_(instance.obj, bstack11ll_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩࠨጽ"))
    @staticmethod
    def bstack111l1l1lll_opy_(hook_type, func, args):
        if hook_type in [bstack11ll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫጾ"), bstack11ll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨጿ")]:
            _111l1lll11_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack111l1ll1l1_opy_(self, hook_type):
        def bstack111ll111l1_opy_(arg=None):
            self.handler(hook_type, bstack11ll_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧፀ"))
            result = None
            exception = None
            try:
                self.bstack111l1l1lll_opy_(hook_type, self._111l1ll1ll_opy_[hook_type], (arg,))
                result = Result(result=bstack11ll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨፁ"))
            except Exception as e:
                result = Result(result=bstack11ll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩፂ"), exception=e)
                self.handler(hook_type, bstack11ll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩፃ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11ll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪፄ"), result)
        def bstack111ll111ll_opy_(this, arg=None):
            self.handler(hook_type, bstack11ll_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬፅ"))
            result = None
            exception = None
            try:
                self.bstack111l1l1lll_opy_(hook_type, self._111l1ll1ll_opy_[hook_type], (this, arg))
                result = Result(result=bstack11ll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ፆ"))
            except Exception as e:
                result = Result(result=bstack11ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧፇ"), exception=e)
                self.handler(hook_type, bstack11ll_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧፈ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11ll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨፉ"), result)
        if hook_type in [bstack11ll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩፊ"), bstack11ll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ፋ")]:
            return bstack111ll111ll_opy_
        return bstack111ll111l1_opy_
    def bstack111ll1111l_opy_(self, bstack111l1lll1l_opy_):
        def bstack111l1lllll_opy_(this, *args, **kwargs):
            self.bstack111ll11111_opy_(this, bstack111l1lll1l_opy_)
            self._111l1llll1_opy_[bstack111l1lll1l_opy_](this, *args, **kwargs)
        return bstack111l1lllll_opy_