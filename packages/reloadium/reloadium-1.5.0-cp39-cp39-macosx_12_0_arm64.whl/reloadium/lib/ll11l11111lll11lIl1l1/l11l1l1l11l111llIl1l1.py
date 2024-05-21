import sys
from contextlib import contextmanager
from pathlib import Path
import types
from typing import TYPE_CHECKING, Any, Dict, Generator, List, Tuple, Type

from reloadium.corium.l1lll1ll11llll1lIl1l1 import l1111111l1llll1lIl1l1
from reloadium.lib.environ import env
from reloadium.corium.l1l111l1l11lll1lIl1l1 import l1l1111ll1llllllIl1l1
from reloadium.lib.ll11l11111lll11lIl1l1.lll11ll11ll11111Il1l1 import l1l11lll1l1l11llIl1l1
from reloadium.corium.ll11lll1ll11111lIl1l1 import lll11l11lll1111lIl1l1, l1ll11lll1ll111lIl1l1, lll11ll1ll111111Il1l1, ll111llll11l1l11Il1l1
from dataclasses import dataclass, field


__RELOADIUM__ = True


@dataclass
class l1lllll1l11l1l11Il1l1(l1l11lll1l1l11llIl1l1):
    ll1l1l1l11l111llIl1l1 = 'FastApi'

    llll1l1111l1lll1Il1l1 = 'uvicorn'

    @contextmanager
    def l111l1ll1l1l111lIl1l1(lll1l11111lll1l1Il1l1) -> Generator[None, None, None]:
        yield 

    def ll11l1l1llllll11Il1l1(lll1l11111lll1l1Il1l1) -> List[Type[l1ll11lll1ll111lIl1l1]]:
        return []

    def l1lll11l111l1lllIl1l1(lll1l11111lll1l1Il1l1, l111111l11111l1lIl1l1: types.ModuleType) -> None:
        if (lll1l11111lll1l1Il1l1.lll111ll1llllll1Il1l1(l111111l11111l1lIl1l1, lll1l11111lll1l1Il1l1.llll1l1111l1lll1Il1l1)):
            lll1l11111lll1l1Il1l1.l11l11l111llll11Il1l1()

    @classmethod
    def l11llllllll1l11lIl1l1(l11lllll1l111ll1Il1l1, l1ll111ll1ll11llIl1l1: types.ModuleType) -> bool:
        lllll1l111111111Il1l1 = super().l11llllllll1l11lIl1l1(l1ll111ll1ll11llIl1l1)
        lllll1l111111111Il1l1 |= l1ll111ll1ll11llIl1l1.__name__ == l11lllll1l111ll1Il1l1.llll1l1111l1lll1Il1l1
        return lllll1l111111111Il1l1

    def l11l11l111llll11Il1l1(lll1l11111lll1l1Il1l1) -> None:
        l1l1111l1llll111Il1l1 = '--reload'
        if (l1l1111l1llll111Il1l1 in sys.argv):
            sys.argv.remove('--reload')
