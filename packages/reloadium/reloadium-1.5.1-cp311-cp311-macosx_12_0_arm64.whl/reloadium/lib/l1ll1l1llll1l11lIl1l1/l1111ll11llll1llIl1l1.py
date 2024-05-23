from pathlib import Path
import sys
import threading
from types import CodeType, FrameType, ModuleType
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set, cast

from reloadium.corium import ll11ll111lll11llIl1l1, lllll11ll11ll1l1Il1l1, public, lllllll1lllll1l1Il1l1, ll1l1l1ll1111lllIl1l1
from reloadium.corium.l111llll11l1lll1Il1l1 import lll1ll111ll11111Il1l1, l1l1ll11llll111lIl1l1
from reloadium.corium.lllll11ll11ll1l1Il1l1 import llll1lll11l111llIl1l1, l1l11llll11llll1Il1l1, lllll11l1l1l111lIl1l1
from reloadium.corium.l11lll1ll11l1111Il1l1 import llll11l1l1111lllIl1l1
from reloadium.corium.ll1lll11l11ll11lIl1l1 import ll1lll11l11ll11lIl1l1
from reloadium.corium.ll11l1ll1l1ll111Il1l1 import l1l11lll1l1111l1Il1l1
from reloadium.corium.l1111l11ll111lllIl1l1 import lll11lll11lll111Il1l1, l1l1ll11111ll1l1Il1l1
from dataclasses import dataclass, field


__RELOADIUM__ = True

__all__ = ['l1lllll1111111l1Il1l1', 'l1l1llll1l11l111Il1l1', 'lllllll1lll1111lIl1l1']


ll1ll11l111ll1llIl1l1 = ll1lll11l11ll11lIl1l1.l1l1l1l1l1111l1lIl1l1(__name__)


class l1lllll1111111l1Il1l1:
    @classmethod
    def ll11l11l1l111111Il1l1(lll1111l111l1111Il1l1) -> Optional[FrameType]:
        l1111l1l11l1l1l1Il1l1: FrameType = sys._getframe(2)
        l1ll11ll11l1111lIl1l1 = next(ll1l1l1ll1111lllIl1l1.l1111l1l11l1l1l1Il1l1.lll11ll11lll11l1Il1l1(l1111l1l11l1l1l1Il1l1))
        return l1ll11ll11l1111lIl1l1


class l1l1llll1l11l111Il1l1(l1lllll1111111l1Il1l1):
    @classmethod
    def ll1lll111lll11llIl1l1(lll1l1ll1ll1l1l1Il1l1, l1l1111l11l111llIl1l1: List[Any], llll11ll11l1l111Il1l1: Dict[str, Any], l11l111lll1ll111Il1l1: List[lll11lll11lll111Il1l1]) -> Any:  # type: ignore
        with l1l11llll11llll1Il1l1():
            assert llll11l1l1111lllIl1l1.l1l1lll11ll11l11Il1l1.l1ll1l1llll1l11lIl1l1
            l1111l1l11l1l1l1Il1l1 = llll11l1l1111lllIl1l1.l1l1lll11ll11l11Il1l1.l1ll1l1llll1l11lIl1l1.l1111l1l1l1llll1Il1l1.l1ll11ll11l1ll11Il1l1()

            l1l1111lll11lll1Il1l1 = l1111l1l11l1l1l1Il1l1.l1ll111l1ll1lll1Il1l1.l1l1l11l1lll11llIl1l1.l11lll1l1l1ll1l1Il1l1(l1111l1l11l1l1l1Il1l1.ll1l1l11ll11ll11Il1l1, l1111l1l11l1l1l1Il1l1.l1ll111l1ll1lll1Il1l1.l1l111ll11lll11lIl1l1())
            assert l1l1111lll11lll1Il1l1
            ll1ll1l111111111Il1l1 = lll1l1ll1ll1l1l1Il1l1.ll11l11l1l111111Il1l1()

            for l1ll1l11111l1111Il1l1 in l11l111lll1ll111Il1l1:
                l1ll1l11111l1111Il1l1.lll1l1lllll1l1llIl1l1()

            for l1ll1l11111l1111Il1l1 in l11l111lll1ll111Il1l1:
                l1ll1l11111l1111Il1l1.l11l1ll1l1lllll1Il1l1()

            l1111l1l11l1l1l1Il1l1.l11l1ll111111111Il1l1()


        l1ll11ll11l1111lIl1l1 = l1l1111lll11lll1Il1l1(*l1l1111l11l111llIl1l1, **llll11ll11l1l111Il1l1);        l1111l1l11l1l1l1Il1l1.lll1l1ll1l1l1ll1Il1l1.additional_info.pydev_step_stop = ll1ll1l111111111Il1l1  # type: ignore

        return l1ll11ll11l1111lIl1l1

    @classmethod
    async def l111l1lll1llllllIl1l1(lll1l1ll1ll1l1l1Il1l1, l1l1111l11l111llIl1l1: List[Any], llll11ll11l1l111Il1l1: Dict[str, Any], l11l111lll1ll111Il1l1: List[l1l1ll11111ll1l1Il1l1]) -> Any:  # type: ignore
        with l1l11llll11llll1Il1l1():
            assert llll11l1l1111lllIl1l1.l1l1lll11ll11l11Il1l1.l1ll1l1llll1l11lIl1l1
            l1111l1l11l1l1l1Il1l1 = llll11l1l1111lllIl1l1.l1l1lll11ll11l11Il1l1.l1ll1l1llll1l11lIl1l1.l1111l1l1l1llll1Il1l1.l1ll11ll11l1ll11Il1l1()

            l1l1111lll11lll1Il1l1 = l1111l1l11l1l1l1Il1l1.l1ll111l1ll1lll1Il1l1.l1l1l11l1lll11llIl1l1.l11lll1l1l1ll1l1Il1l1(l1111l1l11l1l1l1Il1l1.ll1l1l11ll11ll11Il1l1, l1111l1l11l1l1l1Il1l1.l1ll111l1ll1lll1Il1l1.l1l111ll11lll11lIl1l1())
            assert l1l1111lll11lll1Il1l1
            ll1ll1l111111111Il1l1 = lll1l1ll1ll1l1l1Il1l1.ll11l11l1l111111Il1l1()

            for l1ll1l11111l1111Il1l1 in l11l111lll1ll111Il1l1:
                await l1ll1l11111l1111Il1l1.lll1l1lllll1l1llIl1l1()

            for l1ll1l11111l1111Il1l1 in l11l111lll1ll111Il1l1:
                await l1ll1l11111l1111Il1l1.l11l1ll1l1lllll1Il1l1()

            l1111l1l11l1l1l1Il1l1.l11l1ll111111111Il1l1()


        l1ll11ll11l1111lIl1l1 = await l1l1111lll11lll1Il1l1(*l1l1111l11l111llIl1l1, **llll11ll11l1l111Il1l1);        l1111l1l11l1l1l1Il1l1.lll1l1ll1l1l1ll1Il1l1.additional_info.pydev_step_stop = ll1ll1l111111111Il1l1  # type: ignore

        return l1ll11ll11l1111lIl1l1


class lllllll1lll1111lIl1l1(l1lllll1111111l1Il1l1):
    @classmethod
    def ll1lll111lll11llIl1l1(lll1l1ll1ll1l1l1Il1l1) -> Optional[ModuleType]:  # type: ignore
        with l1l11llll11llll1Il1l1():
            assert llll11l1l1111lllIl1l1.l1l1lll11ll11l11Il1l1.l1ll1l1llll1l11lIl1l1
            l1111l1l11l1l1l1Il1l1 = llll11l1l1111lllIl1l1.l1l1lll11ll11l11Il1l1.l1ll1l1llll1l11lIl1l1.l1111l1l1l1llll1Il1l1.l1ll11ll11l1ll11Il1l1()

            llllll1ll1l1lll1Il1l1 = Path(l1111l1l11l1l1l1Il1l1.ll11l11l111l111lIl1l1.f_globals['__spec__'].origin).absolute()
            l1lll111l1l111l1Il1l1 = l1111l1l11l1l1l1Il1l1.ll11l11l111l111lIl1l1.f_globals['__name__']
            lllll11l11l1l1llIl1l1 = llll11l1l1111lllIl1l1.l1l1lll11ll11l11Il1l1.l1l111llll11ll11Il1l1.l1lllll1111l1ll1Il1l1(llllll1ll1l1lll1Il1l1)

            if ( not lllll11l11l1l1llIl1l1):
                ll1ll11l111ll1llIl1l1.ll1111l11l1l11llIl1l1('Could not retrieve src.', l1lllll1l111lll1Il1l1={'file': l1l11lll1l1111l1Il1l1.lllll11l1l1ll1llIl1l1(llllll1ll1l1lll1Il1l1), 
'fullname': l1l11lll1l1111l1Il1l1.l1lll111l1l111l1Il1l1(l1lll111l1l111l1Il1l1)})

            assert lllll11l11l1l1llIl1l1

        try:
            lllll11l11l1l1llIl1l1.l1111ll1l11l11llIl1l1()
            lllll11l11l1l1llIl1l1.ll1lllllll1l1ll1Il1l1(l1llll11l1l11111Il1l1=False)
            lllll11l11l1l1llIl1l1.llll1lll1l111ll1Il1l1(l1llll11l1l11111Il1l1=False)
        except llll1lll11l111llIl1l1 as lll111ll1l1l1ll1Il1l1:
            l1111l1l11l1l1l1Il1l1.l1l1ll1ll111111lIl1l1(lll111ll1l1l1ll1Il1l1)
            return None

        import importlib.util

        l11lll111lll111lIl1l1 = l1111l1l11l1l1l1Il1l1.ll11l11l111l111lIl1l1.f_locals['__spec__']
        l111l1l1ll1l1l1lIl1l1 = importlib.util.module_from_spec(l11lll111lll111lIl1l1)

        with l1l11llll11llll1Il1l1():
            l1111l1l11l1l1l1Il1l1.l11l1ll111111111Il1l1()

        lllll11l11l1l1llIl1l1.ll11l1lllllll111Il1l1(l111l1l1ll1l1l1lIl1l1)
        return l111l1l1ll1l1l1lIl1l1


l1l1ll11llll111lIl1l1.lll111l11111ll1lIl1l1(lll1ll111ll11111Il1l1.l11llll1l11ll11lIl1l1, l1l1llll1l11l111Il1l1.ll1lll111lll11llIl1l1)
l1l1ll11llll111lIl1l1.lll111l11111ll1lIl1l1(lll1ll111ll11111Il1l1.l1lllll1l1l1111lIl1l1, l1l1llll1l11l111Il1l1.l111l1lll1llllllIl1l1)
l1l1ll11llll111lIl1l1.lll111l11111ll1lIl1l1(lll1ll111ll11111Il1l1.ll1l111ll1lll11lIl1l1, lllllll1lll1111lIl1l1.ll1lll111lll11llIl1l1)
