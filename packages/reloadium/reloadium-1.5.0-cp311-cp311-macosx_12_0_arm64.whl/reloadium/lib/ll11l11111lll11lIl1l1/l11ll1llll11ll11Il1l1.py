from contextlib import contextmanager
from pathlib import Path
import sys
import types
from threading import Timer, Thread
from typing import TYPE_CHECKING, Any, Dict, Generator, List, Tuple, Type, Set


import reloadium.lib.ll11l11111lll11lIl1l1.lll11ll111lll1l1Il1l1
from reloadium.corium import l1111l11l11111llIl1l1, l11l11lll11ll1l1Il1l1, l1lll1ll11llll1lIl1l1
from reloadium.corium.l1l1l1111l1lll11Il1l1 import l111lll11ll1l111Il1l1
from reloadium.corium.ll1ll11ll111l1llIl1l1 import lllllll1ll1l11llIl1l1, ll111ll11l111111Il1l1
from reloadium.corium.ll111ll111ll111lIl1l1 import ll11l1l1l11l1111Il1l1
from reloadium.corium.l1lll1ll11llll1lIl1l1.lll1l1llll1ll111Il1l1 import l1lll1ll1lll1lllIl1l1
from reloadium.lib.ll11l11111lll11lIl1l1.ll111111l1lllll1Il1l1 import l11l111l1ll1llllIl1l1
from reloadium.lib.ll11l11111lll11lIl1l1.ll11lll1ll11l11lIl1l1 import l11111lll11111llIl1l1
from reloadium.lib.ll11l11111lll11lIl1l1.l11l1l1l11l111llIl1l1 import l1lllll1l11l1l11Il1l1
from reloadium.lib.ll11l11111lll11lIl1l1.ll11ll11l111111lIl1l1 import lll1lll111l11ll1Il1l1
from reloadium.lib.ll11l11111lll11lIl1l1.l1l1ll11lll1llllIl1l1 import ll111l1llll1111lIl1l1
from reloadium.lib.ll11l11111lll11lIl1l1.l111l1l11ll1l11lIl1l1 import l1l1ll1ll11l111lIl1l1
from reloadium.lib.ll11l11111lll11lIl1l1.ll1111l1l11l1ll1Il1l1 import ll1llllll1l111llIl1l1
from reloadium.lib.ll11l11111lll11lIl1l1.l1l1111111lllll1Il1l1 import ll1111lll1l11l11Il1l1
from reloadium.lib.ll11l11111lll11lIl1l1.l11111l11ll11l11Il1l1 import l1lllllllll1l1l1Il1l1
from reloadium.lib.ll11l11111lll11lIl1l1.lll111l1l11111l1Il1l1 import lllll11ll1ll111lIl1l1
from reloadium.lib.ll11l11111lll11lIl1l1.ll1l1ll1l1llll1lIl1l1 import l111lll11ll11111Il1l1
from reloadium.corium.llll11l11ll1l11lIl1l1 import llll11l11ll1l11lIl1l1
from dataclasses import dataclass, field

if (TYPE_CHECKING):
    from reloadium.corium.ll11l1lll11l1l1lIl1l1 import lll11ll111ll11llIl1l1
    from reloadium.corium.ll11lll1ll11111lIl1l1 import l1ll1l111l11l111Il1l1


__RELOADIUM__ = True

llll11lll1ll11llIl1l1 = llll11l11ll1l11lIl1l1.ll11l11111l11111Il1l1(__name__)


@dataclass
class lll1l11lllll1l11Il1l1:
    ll11l1lll11l1l1lIl1l1: "lll11ll111ll11llIl1l1"

    ll11l11111lll11lIl1l1: List[l11111lll11111llIl1l1] = field(init=False, default_factory=list)

    ll1l111ll11111l1Il1l1: List[types.ModuleType] = field(init=False, default_factory=list)

    l1lll11l111llll1Il1l1: List[Type[l11111lll11111llIl1l1]] = field(init=False, default_factory=lambda :[lll1lll111l11ll1Il1l1, ll1llllll1l111llIl1l1, l11l111l1ll1llllIl1l1, lllll11ll1ll111lIl1l1, ll1111lll1l11l11Il1l1, ll111l1llll1111lIl1l1, l1lllllllll1l1l1Il1l1, l111lll11ll11111Il1l1, l1lllll1l11l1l11Il1l1, l1l1ll1ll11l111lIl1l1])




    llll1l1l1l1lll11Il1l1: List[Type[l11111lll11111llIl1l1]] = field(init=False, default_factory=list)
    l1l1llll11l111l1Il1l1 = (1 if l111lll11ll1l111Il1l1().l1ll11l1lll1lll1Il1l1 in [ll11l1l1l11l1111Il1l1.l11ll11ll1lll111Il1l1, ll11l1l1l11l1111Il1l1.l1l11ll1l11ll111Il1l1] else 5)

    def __post_init__(lll1l11111lll1l1Il1l1) -> None:
        if (l111lll11ll1l111Il1l1().l1l1l1l1ll111l11Il1l1.lll1lll11ll11lllIl1l1):
            lll1l11111lll1l1Il1l1.l1lll11l111llll1Il1l1.remove(l1lllllllll1l1l1Il1l1)

        l1lll1ll1lll1lllIl1l1(l1111ll1ll1llll1Il1l1=lll1l11111lll1l1Il1l1.l11lll1lll1ll1llIl1l1, l1l111lll1lll111Il1l1='show-forbidden-dialog').start()

    def l11lll1lll1ll1llIl1l1(lll1l11111lll1l1Il1l1) -> None:
        l1lll1ll11llll1lIl1l1.l1111111l1llll1lIl1l1.l1llllll1l1ll111Il1l1(lll1l11111lll1l1Il1l1.l1l1llll11l111l1Il1l1)

        lll1l11111lll1l1Il1l1.ll11l1lll11l1l1lIl1l1.ll11l1ll11l1lll1Il1l1.l1l1ll111l1lllllIl1l1()

        if ( not lll1l11111lll1l1Il1l1.llll1l1l1l1lll11Il1l1):
            return 

        ll11l11111lll11lIl1l1 = [ll1lll1lll11l111Il1l1.ll1l1l1l11l111llIl1l1 for ll1lll1lll11l111Il1l1 in lll1l11111lll1l1Il1l1.llll1l1l1l1lll11Il1l1]
        lll1l11111lll1l1Il1l1.ll11l1lll11l1l1lIl1l1.l11111l1ll1l1l11Il1l1.l111111lll11llllIl1l1(ll111ll11l111111Il1l1.lllllllll11l1111Il1l1, l11l11lll11ll1l1Il1l1.l1llll11lll111l1Il1l1.l1llllllllllll11Il1l1(ll11l11111lll11lIl1l1), 
lll11l1l1l1llll1Il1l1='')

    def l1llll1l1lllll11Il1l1(lll1l11111lll1l1Il1l1, ll111l11ll111ll1Il1l1: types.ModuleType) -> None:
        for l1l1l111111ll111Il1l1 in lll1l11111lll1l1Il1l1.l1lll11l111llll1Il1l1.copy():
            if (l1l1l111111ll111Il1l1.l11llllllll1l11lIl1l1(ll111l11ll111ll1Il1l1)):
                if (( not l1l1l111111ll111Il1l1.ll1ll11l1l1ll111Il1l1 and lll1l11111lll1l1Il1l1.ll11l1lll11l1l1lIl1l1.l11111l1ll1l1l11Il1l1.ll1ll11ll111l1llIl1l1.ll1l11lllllll111Il1l1([l1l1l111111ll111Il1l1.ll1l1l1l11l111llIl1l1]) is False)):
                    lll1l11111lll1l1Il1l1.llll1l1l1l1lll11Il1l1.append(l1l1l111111ll111Il1l1)
                    lll1l11111lll1l1Il1l1.l1lll11l111llll1Il1l1.remove(l1l1l111111ll111Il1l1)
                    continue
                lll1l11111lll1l1Il1l1.l1111llllll1lll1Il1l1(l1l1l111111ll111Il1l1)

        if (ll111l11ll111ll1Il1l1 in lll1l11111lll1l1Il1l1.ll1l111ll11111l1Il1l1):
            return 

        for l11l1l1l11ll1l11Il1l1 in lll1l11111lll1l1Il1l1.ll11l11111lll11lIl1l1.copy():
            l11l1l1l11ll1l11Il1l1.l1lll11l111l1lllIl1l1(ll111l11ll111ll1Il1l1)

        lll1l11111lll1l1Il1l1.ll1l111ll11111l1Il1l1.append(ll111l11ll111ll1Il1l1)

    def l1111llllll1lll1Il1l1(lll1l11111lll1l1Il1l1, l1l1l111111ll111Il1l1: Type[l11111lll11111llIl1l1]) -> None:
        ll1111l1lllllll1Il1l1 = l1l1l111111ll111Il1l1(lll1l11111lll1l1Il1l1, lll1l11111lll1l1Il1l1.ll11l1lll11l1l1lIl1l1.l11111l1ll1l1l11Il1l1.ll1ll11ll111l1llIl1l1)

        lll1l11111lll1l1Il1l1.ll11l1lll11l1l1lIl1l1.l11lll1l1111l1llIl1l1.l1111l1l1lll1111Il1l1.l1lll1l11ll111l1Il1l1(l1111l11l11111llIl1l1.ll1l1l1lll1l11llIl1l1(ll1111l1lllllll1Il1l1))
        ll1111l1lllllll1Il1l1.l11lll1111l1lll1Il1l1()
        lll1l11111lll1l1Il1l1.ll11l11111lll11lIl1l1.append(ll1111l1lllllll1Il1l1)

        if (l1l1l111111ll111Il1l1 in lll1l11111lll1l1Il1l1.l1lll11l111llll1Il1l1):
            lll1l11111lll1l1Il1l1.l1lll11l111llll1Il1l1.remove(l1l1l111111ll111Il1l1)

    @contextmanager
    def l111l1ll1l1l111lIl1l1(lll1l11111lll1l1Il1l1) -> Generator[None, None, None]:
        ll1lll1llll1l1l1Il1l1 = [l11l1l1l11ll1l11Il1l1.l111l1ll1l1l111lIl1l1() for l11l1l1l11ll1l11Il1l1 in lll1l11111lll1l1Il1l1.ll11l11111lll11lIl1l1.copy()]

        for l11ll1l1ll1l1l1lIl1l1 in ll1lll1llll1l1l1Il1l1:
            l11ll1l1ll1l1l1lIl1l1.__enter__()

        yield 

        for l11ll1l1ll1l1l1lIl1l1 in ll1lll1llll1l1l1Il1l1:
            l11ll1l1ll1l1l1lIl1l1.__exit__(*sys.exc_info())

    def ll11111lll1ll11lIl1l1(lll1l11111lll1l1Il1l1, lll11llll1111111Il1l1: Path) -> None:
        for l11l1l1l11ll1l11Il1l1 in lll1l11111lll1l1Il1l1.ll11l11111lll11lIl1l1.copy():
            l11l1l1l11ll1l11Il1l1.ll11111lll1ll11lIl1l1(lll11llll1111111Il1l1)

    def lll111llllll11l1Il1l1(lll1l11111lll1l1Il1l1, lll11llll1111111Il1l1: Path) -> None:
        for l11l1l1l11ll1l11Il1l1 in lll1l11111lll1l1Il1l1.ll11l11111lll11lIl1l1.copy():
            l11l1l1l11ll1l11Il1l1.lll111llllll11l1Il1l1(lll11llll1111111Il1l1)

    def l11111l1l1l111llIl1l1(lll1l11111lll1l1Il1l1, ll1ll1ll11l1l1l1Il1l1: Exception) -> None:
        for l11l1l1l11ll1l11Il1l1 in lll1l11111lll1l1Il1l1.ll11l11111lll11lIl1l1.copy():
            l11l1l1l11ll1l11Il1l1.l11111l1l1l111llIl1l1(ll1ll1ll11l1l1l1Il1l1)

    def lll11111lllll1llIl1l1(lll1l11111lll1l1Il1l1, lll11llll1111111Il1l1: Path, l111lll111111l1lIl1l1: List["l1ll1l111l11l111Il1l1"]) -> None:
        for l11l1l1l11ll1l11Il1l1 in lll1l11111lll1l1Il1l1.ll11l11111lll11lIl1l1.copy():
            l11l1l1l11ll1l11Il1l1.lll11111lllll1llIl1l1(lll11llll1111111Il1l1, l111lll111111l1lIl1l1)

    def lll1ll1l1l111lllIl1l1(lll1l11111lll1l1Il1l1) -> None:
        lll1l11111lll1l1Il1l1.ll11l11111lll11lIl1l1.clear()
