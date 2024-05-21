from pathlib import Path
import types
from typing import TYPE_CHECKING, Any, List

from reloadium.lib.ll11l11111lll11lIl1l1.ll11lll1ll11l11lIl1l1 import l11111lll11111llIl1l1
from reloadium.corium.ll11lll1ll11111lIl1l1 import l1ll1l111l11l111Il1l1
from reloadium.corium.l1lll1ll11llll1lIl1l1 import l1111111l1llll1lIl1l1
from dataclasses import dataclass, field


__RELOADIUM__ = True


@dataclass
class ll1111lll1l11l11Il1l1(l11111lll11111llIl1l1):
    ll1l1l1l11l111llIl1l1 = 'PyGame'

    ll1ll11l1l1ll111Il1l1 = True

    l11l11lll11ll11lIl1l1: bool = field(init=False, default=False)

    def l1lll11l111l1lllIl1l1(lll1l11111lll1l1Il1l1, l111111l11111l1lIl1l1: types.ModuleType) -> None:
        if (lll1l11111lll1l1Il1l1.lll111ll1llllll1Il1l1(l111111l11111l1lIl1l1, 'pygame.base')):
            lll1l11111lll1l1Il1l1.l11l11l11ll1ll1lIl1l1()

    def l11l11l11ll1ll1lIl1l1(lll1l11111lll1l1Il1l1) -> None:
        import pygame.display

        l1l11lll1l111l1lIl1l1 = pygame.display.update

        def l11l11llll1lll1lIl1l1(*l11111l111l11lllIl1l1: Any, **lll1l11l1l1ll111Il1l1: Any) -> None:
            if (lll1l11111lll1l1Il1l1.l11l11lll11ll11lIl1l1):
                l1111111l1llll1lIl1l1.l1llllll1l1ll111Il1l1(0.1)
                return None
            else:
                return l1l11lll1l111l1lIl1l1(*l11111l111l11lllIl1l1, **lll1l11l1l1ll111Il1l1)

        pygame.display.update = l11l11llll1lll1lIl1l1

    def ll11111lll1ll11lIl1l1(lll1l11111lll1l1Il1l1, lll11llll1111111Il1l1: Path) -> None:
        lll1l11111lll1l1Il1l1.l11l11lll11ll11lIl1l1 = True

    def lll11111lllll1llIl1l1(lll1l11111lll1l1Il1l1, lll11llll1111111Il1l1: Path, l111lll111111l1lIl1l1: List[l1ll1l111l11l111Il1l1]) -> None:
        lll1l11111lll1l1Il1l1.l11l11lll11ll11lIl1l1 = False

    def l11111l1l1l111llIl1l1(lll1l11111lll1l1Il1l1, ll1ll1ll11l1l1l1Il1l1: Exception) -> None:
        lll1l11111lll1l1Il1l1.l11l11lll11ll11lIl1l1 = False
