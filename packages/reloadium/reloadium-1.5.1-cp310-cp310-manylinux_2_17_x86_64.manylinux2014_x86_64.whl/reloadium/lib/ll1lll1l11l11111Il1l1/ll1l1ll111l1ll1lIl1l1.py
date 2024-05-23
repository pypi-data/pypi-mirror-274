import dataclasses
import types
from reloadium.lib.ll1lll1l11l11111Il1l1.l11l1lll1l11l111Il1l1 import llll1l1l11llll11Il1l1
from reloadium.fast.ll1lll1l11l11111Il1l1.ll1l1ll111l1ll1lIl1l1 import ll1l1llll1l11lllIl1l1

from dataclasses import dataclass

__RELOADIUM__ = True

import types


@dataclass(repr=False, frozen=False)
class lll111lllll1l111Il1l1(llll1l1l11llll11Il1l1):
    ll11111lll1l1111Il1l1 = 'Pytest'

    def l1ll11lll111ll11Il1l1(lll1111l111l1111Il1l1, l111l1l1ll1l1l1lIl1l1: types.ModuleType) -> None:
        if (lll1111l111l1111Il1l1.l1l1l1l111111lllIl1l1(l111l1l1ll1l1l1lIl1l1, 'pytest')):
            lll1111l111l1111Il1l1.lll1111ll11l1l1lIl1l1(l111l1l1ll1l1l1lIl1l1)

    def lll1111ll11l1l1lIl1l1(lll1111l111l1111Il1l1, l111l1l1ll1l1l1lIl1l1: types.ModuleType) -> None:
        import _pytest.assertion.rewrite
        _pytest.assertion.rewrite.AssertionRewritingHook = ll1l1llll1l11lllIl1l1  # type: ignore

