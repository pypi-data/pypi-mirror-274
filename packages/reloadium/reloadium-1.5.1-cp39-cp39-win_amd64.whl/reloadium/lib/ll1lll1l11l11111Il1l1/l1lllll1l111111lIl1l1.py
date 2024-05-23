from pathlib import Path
import types
from typing import TYPE_CHECKING, Any, List

from reloadium.lib.ll1lll1l11l11111Il1l1.l11l1lll1l11l111Il1l1 import llll1l1l11llll11Il1l1
from reloadium.corium.ll111ll1l11l1ll1Il1l1 import l111111l111l1ll1Il1l1
from reloadium.corium.ll1l1l1ll1111lllIl1l1 import l1l11lll1l1l1lllIl1l1
from dataclasses import dataclass, field


__RELOADIUM__ = True


@dataclass
class l111111l11111l11Il1l1(llll1l1l11llll11Il1l1):
    ll11111lll1l1111Il1l1 = 'PyGame'

    llllllll11lll111Il1l1 = True

    l11111l1l1llllllIl1l1: bool = field(init=False, default=False)

    def l1ll11lll111ll11Il1l1(lll1111l111l1111Il1l1, l11l1l1l1llll1llIl1l1: types.ModuleType) -> None:
        if (lll1111l111l1111Il1l1.l1l1l1l111111lllIl1l1(l11l1l1l1llll1llIl1l1, 'pygame.base')):
            lll1111l111l1111Il1l1.l1ll111llllll1llIl1l1()

    def l1ll111llllll1llIl1l1(lll1111l111l1111Il1l1) -> None:
        import pygame.display

        l11l1lll1l11ll11Il1l1 = pygame.display.update

        def l1l11lll111lllllIl1l1(*l1l1111l11l111llIl1l1: Any, **llll11ll11l1l111Il1l1: Any) -> None:
            if (lll1111l111l1111Il1l1.l11111l1l1llllllIl1l1):
                l1l11lll1l1l1lllIl1l1.ll1111l1llll11llIl1l1(0.1)
                return None
            else:
                return l11l1lll1l11ll11Il1l1(*l1l1111l11l111llIl1l1, **llll11ll11l1l111Il1l1)

        pygame.display.update = l1l11lll111lllllIl1l1

    def lllll1l1ll11111lIl1l1(lll1111l111l1111Il1l1, lllll11l1l1ll1llIl1l1: Path) -> None:
        lll1111l111l1111Il1l1.l11111l1l1llllllIl1l1 = True

    def ll11l1lllll111l1Il1l1(lll1111l111l1111Il1l1, lllll11l1l1ll1llIl1l1: Path, ll1l1l1llll1ll11Il1l1: List[l111111l111l1ll1Il1l1]) -> None:
        lll1111l111l1111Il1l1.l11111l1l1llllllIl1l1 = False

    def ll1l1ll1llll11l1Il1l1(lll1111l111l1111Il1l1, ll1l1ll111l1l111Il1l1: Exception) -> None:
        lll1111l111l1111Il1l1.l11111l1l1llllllIl1l1 = False
