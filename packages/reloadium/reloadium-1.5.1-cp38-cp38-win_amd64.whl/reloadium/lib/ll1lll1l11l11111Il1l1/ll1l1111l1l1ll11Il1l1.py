import types
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, List, Optional, Tuple, Type, Union, cast

from reloadium.corium.lllll1111111l1l1Il1l1 import l11l1l11111l111lIl1l1
from reloadium.lib.ll1lll1l11l11111Il1l1.l11l1lll1l11l111Il1l1 import llll1l1l11llll11Il1l1
from reloadium.lib import extensions_raw
from reloadium.corium.l11lll1ll11l1111Il1l1 import llll11l1l1111lllIl1l1
from dataclasses import dataclass

if (TYPE_CHECKING):
    ...


__RELOADIUM__ = True


@dataclass
class l11l1l111lll1lllIl1l1(llll1l1l11llll11Il1l1):
    ll11111lll1l1111Il1l1 = 'Multiprocessing'

    llllllll11lll111Il1l1 = True

    def __post_init__(lll1111l111l1111Il1l1) -> None:
        super().__post_init__()

    def l1ll11lll111ll11Il1l1(lll1111l111l1111Il1l1, l111l1l1ll1l1l1lIl1l1: types.ModuleType) -> None:
        if (lll1111l111l1111Il1l1.l1l1l1l111111lllIl1l1(l111l1l1ll1l1l1lIl1l1, 'multiprocessing.popen_spawn_posix')):
            lll1111l111l1111Il1l1.l111l1ll1llllll1Il1l1(l111l1l1ll1l1l1lIl1l1)

        if (lll1111l111l1111Il1l1.l1l1l1l111111lllIl1l1(l111l1l1ll1l1l1lIl1l1, 'multiprocessing.popen_spawn_win32')):
            lll1111l111l1111Il1l1.ll11111llll1l111Il1l1(l111l1l1ll1l1l1lIl1l1)

    def l111l1ll1llllll1Il1l1(lll1111l111l1111Il1l1, l111l1l1ll1l1l1lIl1l1: types.ModuleType) -> None:
        import multiprocessing.popen_spawn_posix
        multiprocessing.popen_spawn_posix.Popen._launch = extensions_raw.multiprocessing.posix_popen_launch  # type: ignore

    def ll11111llll1l111Il1l1(lll1111l111l1111Il1l1, l111l1l1ll1l1l1lIl1l1: types.ModuleType) -> None:
        import multiprocessing.popen_spawn_win32
        multiprocessing.popen_spawn_win32.Popen.__init__ = extensions_raw.multiprocessing.wind32_popen_launch  # type: ignore
