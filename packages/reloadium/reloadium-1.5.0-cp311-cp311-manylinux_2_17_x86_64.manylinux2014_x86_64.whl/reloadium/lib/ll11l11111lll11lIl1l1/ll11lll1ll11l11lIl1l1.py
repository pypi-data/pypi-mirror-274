from abc import ABC
from contextlib import contextmanager
from pathlib import Path
import sys
import types
from typing import TYPE_CHECKING, Any, ClassVar, Dict, Generator, List, Optional, Tuple, Type

from reloadium.corium.ll1ll11ll111l1llIl1l1 import lllllll1ll1l11llIl1l1, l1ll11l1l111111lIl1l1
from reloadium.corium.llll11l11ll1l11lIl1l1 import l11l1ll11ll1l1l1Il1l1, llll11l11ll1l11lIl1l1
from reloadium.corium.ll11lll1ll11111lIl1l1 import l1ll1l111l11l111Il1l1, l1ll11lll1ll111lIl1l1
from reloadium.corium.l1l11111l11111l1Il1l1 import lllll1111llll1llIl1l1, ll111l1lllll1lllIl1l1
from dataclasses import dataclass, field

if (TYPE_CHECKING):
    from reloadium.lib.ll11l11111lll11lIl1l1.l11ll1llll11ll11Il1l1 import lll1l11lllll1l11Il1l1


__RELOADIUM__ = True

llll11lll1ll11llIl1l1 = llll11l11ll1l11lIl1l1.ll11l11111l11111Il1l1(__name__)


@dataclass
class l11111lll11111llIl1l1:
    l11ll1llll11ll11Il1l1: "lll1l11lllll1l11Il1l1"
    ll1ll11ll111l1llIl1l1: lllllll1ll1l11llIl1l1

    ll1l1l1l11l111llIl1l1: ClassVar[str] = NotImplemented
    l1lllll1l1llllllIl1l1: bool = field(init=False, default=False)

    l1l1111111lll11lIl1l1: l11l1ll11ll1l1l1Il1l1 = field(init=False)

    l111111111l1ll11Il1l1: bool = field(init=False, default=False)

    ll1ll11l1l1ll111Il1l1 = False

    def __post_init__(lll1l11111lll1l1Il1l1) -> None:
        lll1l11111lll1l1Il1l1.l1l1111111lll11lIl1l1 = llll11l11ll1l11lIl1l1.ll11l11111l11111Il1l1(lll1l11111lll1l1Il1l1.ll1l1l1l11l111llIl1l1)
        lll1l11111lll1l1Il1l1.l1l1111111lll11lIl1l1.lll1ll1lll1l1l1lIl1l1('Creating extension')
        lll1l11111lll1l1Il1l1.l11ll1llll11ll11Il1l1.ll11l1lll11l1l1lIl1l1.l1ll11ll1ll1l111Il1l1.l1l11l111l1l11llIl1l1(lll1l11111lll1l1Il1l1.lllll1ll111l1l1lIl1l1())
        lll1l11111lll1l1Il1l1.l111111111l1ll11Il1l1 = isinstance(lll1l11111lll1l1Il1l1.ll1ll11ll111l1llIl1l1, l1ll11l1l111111lIl1l1)

    def lllll1ll111l1l1lIl1l1(lll1l11111lll1l1Il1l1) -> List[Type[l1ll11lll1ll111lIl1l1]]:
        lllll1l111111111Il1l1 = []
        ll11lll1ll11111lIl1l1 = lll1l11111lll1l1Il1l1.ll11l1l1llllll11Il1l1()
        for llllll11l1ll111lIl1l1 in ll11lll1ll11111lIl1l1:
            llllll11l1ll111lIl1l1.l1111111llll1ll1Il1l1 = lll1l11111lll1l1Il1l1.ll1l1l1l11l111llIl1l1

        lllll1l111111111Il1l1.extend(ll11lll1ll11111lIl1l1)
        return lllll1l111111111Il1l1

    def lll11l1lll11l1llIl1l1(lll1l11111lll1l1Il1l1) -> None:
        lll1l11111lll1l1Il1l1.l1lllll1l1llllllIl1l1 = True

    def l1lll11l111l1lllIl1l1(lll1l11111lll1l1Il1l1, l1ll111ll1ll11llIl1l1: types.ModuleType) -> None:
        pass

    @classmethod
    def l11llllllll1l11lIl1l1(l11lllll1l111ll1Il1l1, l1ll111ll1ll11llIl1l1: types.ModuleType) -> bool:
        if ( not hasattr(l1ll111ll1ll11llIl1l1, '__name__')):
            return False

        lllll1l111111111Il1l1 = l1ll111ll1ll11llIl1l1.__name__.split('.')[0].lower() == l11lllll1l111ll1Il1l1.ll1l1l1l11l111llIl1l1.lower()
        return lllll1l111111111Il1l1

    def llllll11l1l1ll1lIl1l1(lll1l11111lll1l1Il1l1) -> None:
        llll11lll1ll11llIl1l1.lll1ll1lll1l1l1lIl1l1(''.join(['Disabling extension ', '{:{}}'.format(lll1l11111lll1l1Il1l1.ll1l1l1l11l111llIl1l1, '')]))

    @contextmanager
    def l111l1ll1l1l111lIl1l1(lll1l11111lll1l1Il1l1) -> Generator[None, None, None]:
        yield 

    def l11lll1111l1lll1Il1l1(lll1l11111lll1l1Il1l1) -> None:
        pass

    def l11111l1l1l111llIl1l1(lll1l11111lll1l1Il1l1, ll1ll1ll11l1l1l1Il1l1: Exception) -> None:
        pass

    def lll111111l11111lIl1l1(lll1l11111lll1l1Il1l1, l1l111lll1lll111Il1l1: str, l1111ll11l1l1111Il1l1: bool) -> Optional[lllll1111llll1llIl1l1]:
        return None

    async def lllll11111111lllIl1l1(lll1l11111lll1l1Il1l1, l1l111lll1lll111Il1l1: str) -> Optional[ll111l1lllll1lllIl1l1]:
        return None

    def llll11111l11l111Il1l1(lll1l11111lll1l1Il1l1, l1l111lll1lll111Il1l1: str) -> Optional[lllll1111llll1llIl1l1]:
        return None

    async def l11l11llllll1ll1Il1l1(lll1l11111lll1l1Il1l1, l1l111lll1lll111Il1l1: str) -> Optional[ll111l1lllll1lllIl1l1]:
        return None

    def lll111llllll11l1Il1l1(lll1l11111lll1l1Il1l1, lll11llll1111111Il1l1: Path) -> None:
        pass

    def ll11111lll1ll11lIl1l1(lll1l11111lll1l1Il1l1, lll11llll1111111Il1l1: Path) -> None:
        pass

    def lll11111lllll1llIl1l1(lll1l11111lll1l1Il1l1, lll11llll1111111Il1l1: Path, l111lll111111l1lIl1l1: List[l1ll1l111l11l111Il1l1]) -> None:
        pass

    def __eq__(lll1l11111lll1l1Il1l1, l1lllllll11llll1Il1l1: Any) -> bool:
        return id(l1lllllll11llll1Il1l1) == id(lll1l11111lll1l1Il1l1)

    def ll11l1l1llllll11Il1l1(lll1l11111lll1l1Il1l1) -> List[Type[l1ll11lll1ll111lIl1l1]]:
        return []

    def lll111ll1llllll1Il1l1(lll1l11111lll1l1Il1l1, l1ll111ll1ll11llIl1l1: types.ModuleType, l1l111lll1lll111Il1l1: str) -> bool:
        lllll1l111111111Il1l1 = (hasattr(l1ll111ll1ll11llIl1l1, '__name__') and l1ll111ll1ll11llIl1l1.__name__ == l1l111lll1lll111Il1l1)
        return lllll1l111111111Il1l1


@dataclass(repr=False)
class l1111l1lllll11llIl1l1(lllll1111llll1llIl1l1):
    ll11lll1ll11l11lIl1l1: l11111lll11111llIl1l1

    def __repr__(lll1l11111lll1l1Il1l1) -> str:
        return 'ExtensionMemento'


@dataclass(repr=False)
class l1l11ll1l11ll1l1Il1l1(ll111l1lllll1lllIl1l1):
    ll11lll1ll11l11lIl1l1: l11111lll11111llIl1l1

    def __repr__(lll1l11111lll1l1Il1l1) -> str:
        return 'AsyncExtensionMemento'
