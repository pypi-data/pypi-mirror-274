import dataclasses
import types
from reloadium.lib.ll11l11111lll11lIl1l1.ll11lll1ll11l11lIl1l1 import l11111lll11111llIl1l1
from reloadium.fast.ll11l11111lll11lIl1l1.l11111l11ll11l11Il1l1 import lll11l11111l1111Il1l1

from dataclasses import dataclass

__RELOADIUM__ = True

import types


@dataclass(repr=False, frozen=False)
class l1lllllllll1l1l1Il1l1(l11111lll11111llIl1l1):
    ll1l1l1l11l111llIl1l1 = 'Pytest'

    def l1lll11l111l1lllIl1l1(lll1l11111lll1l1Il1l1, l1ll111ll1ll11llIl1l1: types.ModuleType) -> None:
        if (lll1l11111lll1l1Il1l1.lll111ll1llllll1Il1l1(l1ll111ll1ll11llIl1l1, 'pytest')):
            lll1l11111lll1l1Il1l1.ll11l1111l1ll1llIl1l1(l1ll111ll1ll11llIl1l1)

    def ll11l1111l1ll1llIl1l1(lll1l11111lll1l1Il1l1, l1ll111ll1ll11llIl1l1: types.ModuleType) -> None:
        import _pytest.assertion.rewrite
        _pytest.assertion.rewrite.AssertionRewritingHook = lll11l11111l1111Il1l1  # type: ignore

