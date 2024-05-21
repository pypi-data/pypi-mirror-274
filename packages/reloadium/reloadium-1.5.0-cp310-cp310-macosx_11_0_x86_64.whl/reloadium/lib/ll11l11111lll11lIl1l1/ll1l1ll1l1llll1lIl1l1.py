import types
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, List, Optional, Tuple, Type, Union, cast

from reloadium.corium.lll111l11l1l11llIl1l1 import ll1ll1ll1lllll11Il1l1
from reloadium.lib.ll11l11111lll11lIl1l1.ll11lll1ll11l11lIl1l1 import l11111lll11111llIl1l1
from reloadium.lib import extensions_raw
from reloadium.corium.lll1llll1l1l1lllIl1l1 import ll11l1l11111l1llIl1l1
from dataclasses import dataclass

if (TYPE_CHECKING):
    ...


__RELOADIUM__ = True


@dataclass
class l111lll11ll11111Il1l1(l11111lll11111llIl1l1):
    ll1l1l1l11l111llIl1l1 = 'Multiprocessing'

    ll1ll11l1l1ll111Il1l1 = True

    def __post_init__(lll1l11111lll1l1Il1l1) -> None:
        super().__post_init__()

    def l1lll11l111l1lllIl1l1(lll1l11111lll1l1Il1l1, l1ll111ll1ll11llIl1l1: types.ModuleType) -> None:
        if (lll1l11111lll1l1Il1l1.lll111ll1llllll1Il1l1(l1ll111ll1ll11llIl1l1, 'multiprocessing.popen_spawn_posix')):
            lll1l11111lll1l1Il1l1.l11l1l111l11ll1lIl1l1(l1ll111ll1ll11llIl1l1)

        if (lll1l11111lll1l1Il1l1.lll111ll1llllll1Il1l1(l1ll111ll1ll11llIl1l1, 'multiprocessing.popen_spawn_win32')):
            lll1l11111lll1l1Il1l1.ll1l11l1ll111ll1Il1l1(l1ll111ll1ll11llIl1l1)

    def l11l1l111l11ll1lIl1l1(lll1l11111lll1l1Il1l1, l1ll111ll1ll11llIl1l1: types.ModuleType) -> None:
        import multiprocessing.popen_spawn_posix
        multiprocessing.popen_spawn_posix.Popen._launch = extensions_raw.multiprocessing.posix_popen_launch  # type: ignore

    def ll1l11l1ll111ll1Il1l1(lll1l11111lll1l1Il1l1, l1ll111ll1ll11llIl1l1: types.ModuleType) -> None:
        import multiprocessing.popen_spawn_win32
        multiprocessing.popen_spawn_win32.Popen.__init__ = extensions_raw.multiprocessing.wind32_popen_launch  # type: ignore
