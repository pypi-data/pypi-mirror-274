from pathlib import Path
import sys
import threading
from types import CodeType, FrameType, ModuleType
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set, cast

from reloadium.corium import l11l11lll11ll1l1Il1l1, l1l111l1l11lll1lIl1l1, public, ll111ll111ll111lIl1l1, l1lll1ll11llll1lIl1l1
from reloadium.corium.lll11l1l1ll1l111Il1l1 import ll1l1111ll111lllIl1l1, ll1llll11l11l1l1Il1l1
from reloadium.corium.l1l111l1l11lll1lIl1l1 import l1111ll11111lll1Il1l1, l1l1111ll1llllllIl1l1, l111l11111ll111lIl1l1
from reloadium.corium.lll1llll1l1l1lllIl1l1 import ll11l1l11111l1llIl1l1
from reloadium.corium.llll11l11ll1l11lIl1l1 import llll11l11ll1l11lIl1l1
from reloadium.corium.lll111l1lllll11lIl1l1 import l1l11l1l1ll1ll1lIl1l1
from reloadium.corium.l1l11111l11111l1Il1l1 import lllll1111llll1llIl1l1, ll111l1lllll1lllIl1l1
from dataclasses import dataclass, field


__RELOADIUM__ = True

__all__ = ['ll1lll1l1111ll1lIl1l1', 'l11l1l1l1l1ll1llIl1l1', 'l11111llll1l1l1lIl1l1']


llll11lll1ll11llIl1l1 = llll11l11ll1l11lIl1l1.ll11l11111l11111Il1l1(__name__)


class ll1lll1l1111ll1lIl1l1:
    @classmethod
    def ll11l1lll1ll11l1Il1l1(lll1l11111lll1l1Il1l1) -> Optional[FrameType]:
        l11ll111ll1ll1llIl1l1: FrameType = sys._getframe(2)
        lllll1l111111111Il1l1 = next(l1lll1ll11llll1lIl1l1.l11ll111ll1ll1llIl1l1.l1l1l1ll111llll1Il1l1(l11ll111ll1ll1llIl1l1))
        return lllll1l111111111Il1l1


class l11l1l1l1l1ll1llIl1l1(ll1lll1l1111ll1lIl1l1):
    @classmethod
    def llll1l11ll11l1l1Il1l1(l11lllll1l111ll1Il1l1, l11111l111l11lllIl1l1: List[Any], lll1l11l1l1ll111Il1l1: Dict[str, Any], ll11111ll1l111llIl1l1: List[lllll1111llll1llIl1l1]) -> Any:  # type: ignore
        with l1l1111ll1llllllIl1l1():
            assert ll11l1l11111l1llIl1l1.ll11l1lll11l1l1lIl1l1.l11l111lll1l1111Il1l1
            l11ll111ll1ll1llIl1l1 = ll11l1l11111l1llIl1l1.ll11l1lll11l1l1lIl1l1.l11l111lll1l1111Il1l1.ll1l11lll1lll1llIl1l1.ll1111l1l11llll1Il1l1()

            l1l11111l1llllllIl1l1 = l11ll111ll1ll1llIl1l1.l1l1l1ll1l1lllllIl1l1.llll111ll111l1l1Il1l1.l11l11lll1l11lllIl1l1(l11ll111ll1ll1llIl1l1.l111lll11l1l111lIl1l1, l11ll111ll1ll1llIl1l1.l1l1l1ll1l1lllllIl1l1.l11llll1ll1l1l11Il1l1())
            assert l1l11111l1llllllIl1l1
            l1111l11111l111lIl1l1 = l11lllll1l111ll1Il1l1.ll11l1lll1ll11l1Il1l1()

            for lllll1llll1l11l1Il1l1 in ll11111ll1l111llIl1l1:
                lllll1llll1l11l1Il1l1.l1ll11l11llll111Il1l1()

            for lllll1llll1l11l1Il1l1 in ll11111ll1l111llIl1l1:
                lllll1llll1l11l1Il1l1.ll1ll11lll1ll1l1Il1l1()

            l11ll111ll1ll1llIl1l1.l1l11ll1lll11l11Il1l1()


        lllll1l111111111Il1l1 = l1l11111l1llllllIl1l1(*l11111l111l11lllIl1l1, **lll1l11l1l1ll111Il1l1);        l11ll111ll1ll1llIl1l1.lll1l1llll1ll111Il1l1.additional_info.pydev_step_stop = l1111l11111l111lIl1l1  # type: ignore

        return lllll1l111111111Il1l1

    @classmethod
    async def ll1111l1ll1l111lIl1l1(l11lllll1l111ll1Il1l1, l11111l111l11lllIl1l1: List[Any], lll1l11l1l1ll111Il1l1: Dict[str, Any], ll11111ll1l111llIl1l1: List[ll111l1lllll1lllIl1l1]) -> Any:  # type: ignore
        with l1l1111ll1llllllIl1l1():
            assert ll11l1l11111l1llIl1l1.ll11l1lll11l1l1lIl1l1.l11l111lll1l1111Il1l1
            l11ll111ll1ll1llIl1l1 = ll11l1l11111l1llIl1l1.ll11l1lll11l1l1lIl1l1.l11l111lll1l1111Il1l1.ll1l11lll1lll1llIl1l1.ll1111l1l11llll1Il1l1()

            l1l11111l1llllllIl1l1 = l11ll111ll1ll1llIl1l1.l1l1l1ll1l1lllllIl1l1.llll111ll111l1l1Il1l1.l11l11lll1l11lllIl1l1(l11ll111ll1ll1llIl1l1.l111lll11l1l111lIl1l1, l11ll111ll1ll1llIl1l1.l1l1l1ll1l1lllllIl1l1.l11llll1ll1l1l11Il1l1())
            assert l1l11111l1llllllIl1l1
            l1111l11111l111lIl1l1 = l11lllll1l111ll1Il1l1.ll11l1lll1ll11l1Il1l1()

            for lllll1llll1l11l1Il1l1 in ll11111ll1l111llIl1l1:
                await lllll1llll1l11l1Il1l1.l1ll11l11llll111Il1l1()

            for lllll1llll1l11l1Il1l1 in ll11111ll1l111llIl1l1:
                await lllll1llll1l11l1Il1l1.ll1ll11lll1ll1l1Il1l1()

            l11ll111ll1ll1llIl1l1.l1l11ll1lll11l11Il1l1()


        lllll1l111111111Il1l1 = await l1l11111l1llllllIl1l1(*l11111l111l11lllIl1l1, **lll1l11l1l1ll111Il1l1);        l11ll111ll1ll1llIl1l1.lll1l1llll1ll111Il1l1.additional_info.pydev_step_stop = l1111l11111l111lIl1l1  # type: ignore

        return lllll1l111111111Il1l1


class l11111llll1l1l1lIl1l1(ll1lll1l1111ll1lIl1l1):
    @classmethod
    def llll1l11ll11l1l1Il1l1(l11lllll1l111ll1Il1l1) -> Optional[ModuleType]:  # type: ignore
        with l1l1111ll1llllllIl1l1():
            assert ll11l1l11111l1llIl1l1.ll11l1lll11l1l1lIl1l1.l11l111lll1l1111Il1l1
            l11ll111ll1ll1llIl1l1 = ll11l1l11111l1llIl1l1.ll11l1lll11l1l1lIl1l1.l11l111lll1l1111Il1l1.ll1l11lll1lll1llIl1l1.ll1111l1l11llll1Il1l1()

            ll1l1l1l111ll1llIl1l1 = Path(l11ll111ll1ll1llIl1l1.ll1lll1l11l1lll1Il1l1.f_globals['__spec__'].origin).absolute()
            l11111lll1ll111lIl1l1 = l11ll111ll1ll1llIl1l1.ll1lll1l11l1lll1Il1l1.f_globals['__name__']
            l11ll1lll111ll11Il1l1 = ll11l1l11111l1llIl1l1.ll11l1lll11l1l1lIl1l1.l1l1ll1l1l111l11Il1l1.l1111l11llllll11Il1l1(ll1l1l1l111ll1llIl1l1)

            if ( not l11ll1lll111ll11Il1l1):
                llll11lll1ll11llIl1l1.l111lll1l11l1111Il1l1('Could not retrieve src.', ll1111ll11l1llllIl1l1={'file': l1l11l1l1ll1ll1lIl1l1.lll11llll1111111Il1l1(ll1l1l1l111ll1llIl1l1), 
'fullname': l1l11l1l1ll1ll1lIl1l1.l11111lll1ll111lIl1l1(l11111lll1ll111lIl1l1)})

            assert l11ll1lll111ll11Il1l1

        try:
            l11ll1lll111ll11Il1l1.l11l1111l1l1lll1Il1l1()
            l11ll1lll111ll11Il1l1.l11ll11ll1ll1lllIl1l1(ll1l111ll1ll1lllIl1l1=False)
            l11ll1lll111ll11Il1l1.ll1ll1lll1llll11Il1l1(ll1l111ll1ll1lllIl1l1=False)
        except l1111ll11111lll1Il1l1 as ll1lll1lll11l111Il1l1:
            l11ll111ll1ll1llIl1l1.l1111lllll11l11lIl1l1(ll1lll1lll11l111Il1l1)
            return None

        import importlib.util

        l111ll1111l1l1l1Il1l1 = l11ll111ll1ll1llIl1l1.ll1lll1l11l1lll1Il1l1.f_locals['__spec__']
        l1ll111ll1ll11llIl1l1 = importlib.util.module_from_spec(l111ll1111l1l1l1Il1l1)

        with l1l1111ll1llllllIl1l1():
            l11ll111ll1ll1llIl1l1.l1l11ll1lll11l11Il1l1()

        l11ll1lll111ll11Il1l1.ll11lll11l1ll111Il1l1(l1ll111ll1ll11llIl1l1)
        return l1ll111ll1ll11llIl1l1


ll1llll11l11l1l1Il1l1.ll1111111l11llllIl1l1(ll1l1111ll111lllIl1l1.l1lllll111l11lllIl1l1, l11l1l1l1l1ll1llIl1l1.llll1l11ll11l1l1Il1l1)
ll1llll11l11l1l1Il1l1.ll1111111l11llllIl1l1(ll1l1111ll111lllIl1l1.lllll11ll1llllllIl1l1, l11l1l1l1l1ll1llIl1l1.ll1111l1ll1l111lIl1l1)
ll1llll11l11l1l1Il1l1.ll1111111l11llllIl1l1(ll1l1111ll111lllIl1l1.ll11l11l1lll1l1lIl1l1, l11111llll1l1l1lIl1l1.llll1l11ll11l1l1Il1l1)
