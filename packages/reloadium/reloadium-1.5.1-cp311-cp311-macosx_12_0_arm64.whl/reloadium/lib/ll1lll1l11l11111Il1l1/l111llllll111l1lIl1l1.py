from contextlib import contextmanager
from pathlib import Path
import sys
import types
from threading import Timer, Thread
from typing import TYPE_CHECKING, Any, Dict, Generator, List, Tuple, Type, Set


import reloadium.lib.ll1lll1l11l11111Il1l1.ll1l11l1111l11l1Il1l1
from reloadium.corium import ll1l11lll1lll111Il1l1, ll11ll111lll11llIl1l1, ll1l1l1ll1111lllIl1l1
from reloadium.corium.l1ll1l1lll11l111Il1l1 import ll11lllll1lll11lIl1l1
from reloadium.corium.lll11l1111l1l11lIl1l1 import l111ll11l1ll1l11Il1l1, l1l11lll11ll1lllIl1l1
from reloadium.corium.lllllll1lllll1l1Il1l1 import ll1l11l1lll1ll1lIl1l1
from reloadium.corium.ll1l1l1ll1111lllIl1l1.lll1l1ll1l1l1ll1Il1l1 import l1111l11l1111111Il1l1
from reloadium.lib.ll1lll1l11l11111Il1l1.lll1l111l1lll1llIl1l1 import ll11l111ll1ll1l1Il1l1
from reloadium.lib.ll1lll1l11l11111Il1l1.l11l1lll1l11l111Il1l1 import llll1l1l11llll11Il1l1
from reloadium.lib.ll1lll1l11l11111Il1l1.llll11llll1l11l1Il1l1 import l1111llll11l1ll1Il1l1
from reloadium.lib.ll1lll1l11l11111Il1l1.ll1lll11l11llll1Il1l1 import l11l11ll1l11ll1lIl1l1
from reloadium.lib.ll1lll1l11l11111Il1l1.l11lllll111ll1l1Il1l1 import ll11llll1ll11lllIl1l1
from reloadium.lib.ll1lll1l11l11111Il1l1.l1111l11lll11ll1Il1l1 import lll111ll1lll11llIl1l1
from reloadium.lib.ll1lll1l11l11111Il1l1.llll1l111lllll11Il1l1 import l1l1l111111111llIl1l1
from reloadium.lib.ll1lll1l11l11111Il1l1.l1lllll1l111111lIl1l1 import l111111l11111l11Il1l1
from reloadium.lib.ll1lll1l11l11111Il1l1.ll1l1ll111l1ll1lIl1l1 import lll111lllll1l111Il1l1
from reloadium.lib.ll1lll1l11l11111Il1l1.ll1l1lll1l11ll11Il1l1 import ll1l111111l1l1l1Il1l1
from reloadium.lib.ll1lll1l11l11111Il1l1.ll1l1111l1l1ll11Il1l1 import l11l1l111lll1lllIl1l1
from reloadium.corium.ll1lll11l11ll11lIl1l1 import ll1lll11l11ll11lIl1l1
from dataclasses import dataclass, field

if (TYPE_CHECKING):
    from reloadium.corium.l1l1lll11ll11l11Il1l1 import llllll11llllllllIl1l1
    from reloadium.corium.ll111ll1l11l1ll1Il1l1 import l111111l111l1ll1Il1l1


__RELOADIUM__ = True

ll1ll11l111ll1llIl1l1 = ll1lll11l11ll11lIl1l1.l1l1l1l1l1111l1lIl1l1(__name__)


@dataclass
class l11l11ll1l1l1lllIl1l1:
    l1l1lll11ll11l11Il1l1: "llllll11llllllllIl1l1"

    ll1lll1l11l11111Il1l1: List[llll1l1l11llll11Il1l1] = field(init=False, default_factory=list)

    ll1111l1ll11llllIl1l1: List[types.ModuleType] = field(init=False, default_factory=list)

    lll1l1lll1ll11llIl1l1: List[Type[llll1l1l11llll11Il1l1]] = field(init=False, default_factory=lambda :[l11l11ll1l11ll1lIl1l1, l1l1l111111111llIl1l1, ll11l111ll1ll1l1Il1l1, ll1l111111l1l1l1Il1l1, l111111l11111l11Il1l1, ll11llll1ll11lllIl1l1, lll111lllll1l111Il1l1, l11l1l111lll1lllIl1l1, l1111llll11l1ll1Il1l1, lll111ll1lll11llIl1l1])




    l1llll1l1l1l1l1lIl1l1: List[Type[llll1l1l11llll11Il1l1]] = field(init=False, default_factory=list)
    llll1ll1l111ll11Il1l1 = (1 if ll11lllll1lll11lIl1l1().ll111ll111111111Il1l1 in [ll1l11l1lll1ll1lIl1l1.ll1l11ll11111lllIl1l1, ll1l11l1lll1ll1lIl1l1.ll1l1ll11l1111l1Il1l1] else 5)

    def __post_init__(lll1111l111l1111Il1l1) -> None:
        if (ll11lllll1lll11lIl1l1().ll1111l111l1ll1lIl1l1.ll1l111ll11111l1Il1l1):
            lll1111l111l1111Il1l1.lll1l1lll1ll11llIl1l1.remove(lll111lllll1l111Il1l1)

        l1111l11l1111111Il1l1(lll1l1l1l11l1l1lIl1l1=lll1111l111l1111Il1l1.ll11lll111l111l1Il1l1, ll11lll111lll1l1Il1l1='show-forbidden-dialog').start()

    def ll11lll111l111l1Il1l1(lll1111l111l1111Il1l1) -> None:
        ll1l1l1ll1111lllIl1l1.l1l11lll1l1l1lllIl1l1.ll1111l1llll11llIl1l1(lll1111l111l1111Il1l1.llll1ll1l111ll11Il1l1)

        lll1111l111l1111Il1l1.l1l1lll11ll11l11Il1l1.lllll111l1lll1l1Il1l1.l111ll11l1111l11Il1l1()

        if ( not lll1111l111l1111Il1l1.l1llll1l1l1l1l1lIl1l1):
            return 

        ll1lll1l11l11111Il1l1 = [lll111ll1l1l1ll1Il1l1.ll11111lll1l1111Il1l1 for lll111ll1l1l1ll1Il1l1 in lll1111l111l1111Il1l1.l1llll1l1l1l1l1lIl1l1]
        lll1111l111l1111Il1l1.l1l1lll11ll11l11Il1l1.l1ll1l1llll11l1lIl1l1.lll1ll1ll11l11llIl1l1(l1l11lll11ll1lllIl1l1.l11llll1l11l1lllIl1l1, ll11ll111lll11llIl1l1.l11l1lll11lll1llIl1l1.l1l111lll11llll1Il1l1(ll1lll1l11l11111Il1l1), 
llllll1l11llllllIl1l1='')

    def l1l1l1111lll111lIl1l1(lll1111l111l1111Il1l1, llll1ll1l11ll11lIl1l1: types.ModuleType) -> None:
        for l1lll11l1l11llllIl1l1 in lll1111l111l1111Il1l1.lll1l1lll1ll11llIl1l1.copy():
            if (l1lll11l1l11llllIl1l1.ll11111ll1lllll1Il1l1(llll1ll1l11ll11lIl1l1)):
                if (( not l1lll11l1l11llllIl1l1.llllllll11lll111Il1l1 and lll1111l111l1111Il1l1.l1l1lll11ll11l11Il1l1.l1ll1l1llll11l1lIl1l1.lll11l1111l1l11lIl1l1.llll11l11l1l11l1Il1l1([l1lll11l1l11llllIl1l1.ll11111lll1l1111Il1l1]) is False)):
                    lll1111l111l1111Il1l1.l1llll1l1l1l1l1lIl1l1.append(l1lll11l1l11llllIl1l1)
                    lll1111l111l1111Il1l1.lll1l1lll1ll11llIl1l1.remove(l1lll11l1l11llllIl1l1)
                    continue
                lll1111l111l1111Il1l1.l1ll1l1ll11111llIl1l1(l1lll11l1l11llllIl1l1)

        if (llll1ll1l11ll11lIl1l1 in lll1111l111l1111Il1l1.ll1111l1ll11llllIl1l1):
            return 

        for l111lll1l1ll1ll1Il1l1 in lll1111l111l1111Il1l1.ll1lll1l11l11111Il1l1.copy():
            l111lll1l1ll1ll1Il1l1.l1ll11lll111ll11Il1l1(llll1ll1l11ll11lIl1l1)

        lll1111l111l1111Il1l1.ll1111l1ll11llllIl1l1.append(llll1ll1l11ll11lIl1l1)

    def l1ll1l1ll11111llIl1l1(lll1111l111l1111Il1l1, l1lll11l1l11llllIl1l1: Type[llll1l1l11llll11Il1l1]) -> None:
        l11l1l1l1ll1111lIl1l1 = l1lll11l1l11llllIl1l1(lll1111l111l1111Il1l1, lll1111l111l1111Il1l1.l1l1lll11ll11l11Il1l1.l1ll1l1llll11l1lIl1l1.lll11l1111l1l11lIl1l1)

        lll1111l111l1111Il1l1.l1l1lll11ll11l11Il1l1.l11llll111l11111Il1l1.ll1lll1llll1l111Il1l1.l1l111111ll111l1Il1l1(ll1l11lll1lll111Il1l1.lll11ll1lll11l1lIl1l1(l11l1l1l1ll1111lIl1l1))
        l11l1l1l1ll1111lIl1l1.llllll1ll1ll1lllIl1l1()
        lll1111l111l1111Il1l1.ll1lll1l11l11111Il1l1.append(l11l1l1l1ll1111lIl1l1)

        if (l1lll11l1l11llllIl1l1 in lll1111l111l1111Il1l1.lll1l1lll1ll11llIl1l1):
            lll1111l111l1111Il1l1.lll1l1lll1ll11llIl1l1.remove(l1lll11l1l11llllIl1l1)

    @contextmanager
    def l1llll111ll1llllIl1l1(lll1111l111l1111Il1l1) -> Generator[None, None, None]:
        lllll1llll11l1l1Il1l1 = [l111lll1l1ll1ll1Il1l1.l1llll111ll1llllIl1l1() for l111lll1l1ll1ll1Il1l1 in lll1111l111l1111Il1l1.ll1lll1l11l11111Il1l1.copy()]

        for lll1lllll11111l1Il1l1 in lllll1llll11l1l1Il1l1:
            lll1lllll11111l1Il1l1.__enter__()

        yield 

        for lll1lllll11111l1Il1l1 in lllll1llll11l1l1Il1l1:
            lll1lllll11111l1Il1l1.__exit__(*sys.exc_info())

    def lllll1l1ll11111lIl1l1(lll1111l111l1111Il1l1, lllll11l1l1ll1llIl1l1: Path) -> None:
        for l111lll1l1ll1ll1Il1l1 in lll1111l111l1111Il1l1.ll1lll1l11l11111Il1l1.copy():
            l111lll1l1ll1ll1Il1l1.lllll1l1ll11111lIl1l1(lllll11l1l1ll1llIl1l1)

    def ll1lll1l1l1lll11Il1l1(lll1111l111l1111Il1l1, lllll11l1l1ll1llIl1l1: Path) -> None:
        for l111lll1l1ll1ll1Il1l1 in lll1111l111l1111Il1l1.ll1lll1l11l11111Il1l1.copy():
            l111lll1l1ll1ll1Il1l1.ll1lll1l1l1lll11Il1l1(lllll11l1l1ll1llIl1l1)

    def ll1l1ll1llll11l1Il1l1(lll1111l111l1111Il1l1, ll1l1ll111l1l111Il1l1: Exception) -> None:
        for l111lll1l1ll1ll1Il1l1 in lll1111l111l1111Il1l1.ll1lll1l11l11111Il1l1.copy():
            l111lll1l1ll1ll1Il1l1.ll1l1ll1llll11l1Il1l1(ll1l1ll111l1l111Il1l1)

    def ll11l1lllll111l1Il1l1(lll1111l111l1111Il1l1, lllll11l1l1ll1llIl1l1: Path, ll1l1l1llll1ll11Il1l1: List["l111111l111l1ll1Il1l1"]) -> None:
        for l111lll1l1ll1ll1Il1l1 in lll1111l111l1111Il1l1.ll1lll1l11l11111Il1l1.copy():
            l111lll1l1ll1ll1Il1l1.ll11l1lllll111l1Il1l1(lllll11l1l1ll1llIl1l1, ll1l1l1llll1ll11Il1l1)

    def ll11ll1ll1111l11Il1l1(lll1111l111l1111Il1l1) -> None:
        lll1111l111l1111Il1l1.ll1lll1l11l11111Il1l1.clear()
