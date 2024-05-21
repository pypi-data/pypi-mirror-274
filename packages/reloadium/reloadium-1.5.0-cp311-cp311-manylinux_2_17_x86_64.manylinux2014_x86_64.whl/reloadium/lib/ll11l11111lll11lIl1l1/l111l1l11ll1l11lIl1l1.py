from dataclasses import dataclass, field
from types import CodeType, ModuleType
from typing import TYPE_CHECKING, Any, Callable, Optional
import inspect

from reloadium.lib.ll11l11111lll11lIl1l1.lll11ll11ll11111Il1l1 import l1l11lll1l1l11llIl1l1

if (TYPE_CHECKING):
    pass


__RELOADIUM__ = True


@dataclass
class l1l1ll1ll11l111lIl1l1(l1l11lll1l1l11llIl1l1):
    ll1l1l1l11l111llIl1l1 = 'Numba'

    ll1ll11l1l1ll111Il1l1 = True

    def __post_init__(lll1l11111lll1l1Il1l1) -> None:
        super().__post_init__()

    def l1lll11l111l1lllIl1l1(lll1l11111lll1l1Il1l1, l1ll111ll1ll11llIl1l1: ModuleType) -> None:
        if (lll1l11111lll1l1Il1l1.lll111ll1llllll1Il1l1(l1ll111ll1ll11llIl1l1, 'numba.core.bytecode')):
            lll1l11111lll1l1Il1l1.l1111111l1ll1l1lIl1l1()

    def l1111111l1ll1l1lIl1l1(lll1l11111lll1l1Il1l1) -> None:
        import numba.core.bytecode

        def l1l11l1ll11l1111Il1l1(lllllllll1111ll1Il1l1) -> CodeType:  # type: ignore
            import ast
            lllll1l111111111Il1l1 = getattr(lllllllll1111ll1Il1l1, '__code__', getattr(lllllllll1111ll1Il1l1, 'func_code', None))  # type: ignore

            if ('__rw_mode__' in lllll1l111111111Il1l1.co_consts):  # type: ignore
                l1lll11ll11llll1Il1l1 = ast.parse(inspect.getsource(lllllllll1111ll1Il1l1))
                l1ll11l111l1111lIl1l1 = l1lll11ll11llll1Il1l1.body[0]
                l1ll11l111l1111lIl1l1.decorator_list = []  # type: ignore

                l111lll11l1l111lIl1l1 = compile(l1lll11ll11llll1Il1l1, filename=lllll1l111111111Il1l1.co_filename, mode='exec')  # type: ignore
                lllll1l111111111Il1l1 = l111lll11l1l111lIl1l1.co_consts[0]

            return lllll1l111111111Il1l1  # type: ignore

        numba.core.bytecode.get_code_object.__code__ = l1l11l1ll11l1111Il1l1.__code__
