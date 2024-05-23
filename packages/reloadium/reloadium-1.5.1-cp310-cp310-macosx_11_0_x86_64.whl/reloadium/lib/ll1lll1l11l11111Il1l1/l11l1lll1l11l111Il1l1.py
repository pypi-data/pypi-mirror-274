from abc import ABC
from contextlib import contextmanager
from pathlib import Path
import sys
import types
from typing import TYPE_CHECKING, Any, ClassVar, Dict, Generator, List, Optional, Tuple, Type

from reloadium.corium.lll11l1111l1l11lIl1l1 import l111ll11l1ll1l11Il1l1, l1lll111l11l1l1lIl1l1
from reloadium.corium.ll1lll11l11ll11lIl1l1 import l111l1l1llllll1lIl1l1, ll1lll11l11ll11lIl1l1
from reloadium.corium.ll111ll1l11l1ll1Il1l1 import l111111l111l1ll1Il1l1, l1llllllll1l1l1lIl1l1
from reloadium.corium.l1111l11ll111lllIl1l1 import lll11lll11lll111Il1l1, l1l1ll11111ll1l1Il1l1
from dataclasses import dataclass, field

if (TYPE_CHECKING):
    from reloadium.lib.ll1lll1l11l11111Il1l1.l111llllll111l1lIl1l1 import l11l11ll1l1l1lllIl1l1


__RELOADIUM__ = True

ll1ll11l111ll1llIl1l1 = ll1lll11l11ll11lIl1l1.l1l1l1l1l1111l1lIl1l1(__name__)


@dataclass
class llll1l1l11llll11Il1l1:
    l111llllll111l1lIl1l1: "l11l11ll1l1l1lllIl1l1"
    lll11l1111l1l11lIl1l1: l111ll11l1ll1l11Il1l1

    ll11111lll1l1111Il1l1: ClassVar[str] = NotImplemented
    l111l1lll111ll11Il1l1: bool = field(init=False, default=False)

    ll11111l1l11l1llIl1l1: l111l1l1llllll1lIl1l1 = field(init=False)

    lll111l1lllll111Il1l1: bool = field(init=False, default=False)

    llllllll11lll111Il1l1 = False

    def __post_init__(lll1111l111l1111Il1l1) -> None:
        lll1111l111l1111Il1l1.ll11111l1l11l1llIl1l1 = ll1lll11l11ll11lIl1l1.l1l1l1l1l1111l1lIl1l1(lll1111l111l1111Il1l1.ll11111lll1l1111Il1l1)
        lll1111l111l1111Il1l1.ll11111l1l11l1llIl1l1.l11l11111llll1llIl1l1('Creating extension')
        lll1111l111l1111Il1l1.l111llllll111l1lIl1l1.l1l1lll11ll11l11Il1l1.l1llllll11ll1111Il1l1.l1ll111lll1l1l11Il1l1(lll1111l111l1111Il1l1.ll11l1ll11ll1ll1Il1l1())
        lll1111l111l1111Il1l1.lll111l1lllll111Il1l1 = isinstance(lll1111l111l1111Il1l1.lll11l1111l1l11lIl1l1, l1lll111l11l1l1lIl1l1)

    def ll11l1ll11ll1ll1Il1l1(lll1111l111l1111Il1l1) -> List[Type[l1llllllll1l1l1lIl1l1]]:
        l1ll11ll11l1111lIl1l1 = []
        ll111ll1l11l1ll1Il1l1 = lll1111l111l1111Il1l1.l11ll1l1111ll1llIl1l1()
        for l11l11ll1l1lll1lIl1l1 in ll111ll1l11l1ll1Il1l1:
            l11l11ll1l1lll1lIl1l1.ll1llll1ll1ll1l1Il1l1 = lll1111l111l1111Il1l1.ll11111lll1l1111Il1l1

        l1ll11ll11l1111lIl1l1.extend(ll111ll1l11l1ll1Il1l1)
        return l1ll11ll11l1111lIl1l1

    def lll111l11lll1l11Il1l1(lll1111l111l1111Il1l1) -> None:
        lll1111l111l1111Il1l1.l111l1lll111ll11Il1l1 = True

    def l1ll11lll111ll11Il1l1(lll1111l111l1111Il1l1, l111l1l1ll1l1l1lIl1l1: types.ModuleType) -> None:
        pass

    @classmethod
    def ll11111ll1lllll1Il1l1(lll1l1ll1ll1l1l1Il1l1, l111l1l1ll1l1l1lIl1l1: types.ModuleType) -> bool:
        if ( not hasattr(l111l1l1ll1l1l1lIl1l1, '__name__')):
            return False

        l1ll11ll11l1111lIl1l1 = l111l1l1ll1l1l1lIl1l1.__name__.split('.')[0].lower() == lll1l1ll1ll1l1l1Il1l1.ll11111lll1l1111Il1l1.lower()
        return l1ll11ll11l1111lIl1l1

    def l11lll1l11l1111lIl1l1(lll1111l111l1111Il1l1) -> None:
        ll1ll11l111ll1llIl1l1.l11l11111llll1llIl1l1(''.join(['Disabling extension ', '{:{}}'.format(lll1111l111l1111Il1l1.ll11111lll1l1111Il1l1, '')]))

    @contextmanager
    def l1llll111ll1llllIl1l1(lll1111l111l1111Il1l1) -> Generator[None, None, None]:
        yield 

    def llllll1ll1ll1lllIl1l1(lll1111l111l1111Il1l1) -> None:
        pass

    def ll1l1ll1llll11l1Il1l1(lll1111l111l1111Il1l1, ll1l1ll111l1l111Il1l1: Exception) -> None:
        pass

    def lll111lll11111llIl1l1(lll1111l111l1111Il1l1, ll11lll111lll1l1Il1l1: str, l11lll1l1lll11l1Il1l1: bool) -> Optional[lll11lll11lll111Il1l1]:
        return None

    async def ll1ll1l1lll11111Il1l1(lll1111l111l1111Il1l1, ll11lll111lll1l1Il1l1: str) -> Optional[l1l1ll11111ll1l1Il1l1]:
        return None

    def llll1lllll1l11llIl1l1(lll1111l111l1111Il1l1, ll11lll111lll1l1Il1l1: str) -> Optional[lll11lll11lll111Il1l1]:
        return None

    async def l111l11l1l111ll1Il1l1(lll1111l111l1111Il1l1, ll11lll111lll1l1Il1l1: str) -> Optional[l1l1ll11111ll1l1Il1l1]:
        return None

    def ll1lll1l1l1lll11Il1l1(lll1111l111l1111Il1l1, lllll11l1l1ll1llIl1l1: Path) -> None:
        pass

    def lllll1l1ll11111lIl1l1(lll1111l111l1111Il1l1, lllll11l1l1ll1llIl1l1: Path) -> None:
        pass

    def ll11l1lllll111l1Il1l1(lll1111l111l1111Il1l1, lllll11l1l1ll1llIl1l1: Path, ll1l1l1llll1ll11Il1l1: List[l111111l111l1ll1Il1l1]) -> None:
        pass

    def __eq__(lll1111l111l1111Il1l1, ll1l1lll1l11l1llIl1l1: Any) -> bool:
        return id(ll1l1lll1l11l1llIl1l1) == id(lll1111l111l1111Il1l1)

    def l11ll1l1111ll1llIl1l1(lll1111l111l1111Il1l1) -> List[Type[l1llllllll1l1l1lIl1l1]]:
        return []

    def l1l1l1l111111lllIl1l1(lll1111l111l1111Il1l1, l111l1l1ll1l1l1lIl1l1: types.ModuleType, ll11lll111lll1l1Il1l1: str) -> bool:
        l1ll11ll11l1111lIl1l1 = (hasattr(l111l1l1ll1l1l1lIl1l1, '__name__') and l111l1l1ll1l1l1lIl1l1.__name__ == ll11lll111lll1l1Il1l1)
        return l1ll11ll11l1111lIl1l1


@dataclass(repr=False)
class llll1lll11l1ll1lIl1l1(lll11lll11lll111Il1l1):
    l11l1lll1l11l111Il1l1: llll1l1l11llll11Il1l1

    def __repr__(lll1111l111l1111Il1l1) -> str:
        return 'ExtensionMemento'


@dataclass(repr=False)
class lllll111llllll11Il1l1(l1l1ll11111ll1l1Il1l1):
    l11l1lll1l11l111Il1l1: llll1l1l11llll11Il1l1

    def __repr__(lll1111l111l1111Il1l1) -> str:
        return 'AsyncExtensionMemento'
