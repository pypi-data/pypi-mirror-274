from dataclasses import dataclass, field
from types import CodeType, ModuleType
from typing import TYPE_CHECKING, Any, Callable, Optional
import inspect

from reloadium.lib.ll1lll1l11l11111Il1l1.lll1ll1ll111l1llIl1l1 import lll1ll1111111ll1Il1l1

if (TYPE_CHECKING):
    pass


__RELOADIUM__ = True


@dataclass
class lll111ll1lll11llIl1l1(lll1ll1111111ll1Il1l1):
    ll11111lll1l1111Il1l1 = 'Numba'

    llllllll11lll111Il1l1 = True

    def __post_init__(lll1111l111l1111Il1l1) -> None:
        super().__post_init__()

    def l1ll11lll111ll11Il1l1(lll1111l111l1111Il1l1, l111l1l1ll1l1l1lIl1l1: ModuleType) -> None:
        if (lll1111l111l1111Il1l1.l1l1l1l111111lllIl1l1(l111l1l1ll1l1l1lIl1l1, 'numba.core.bytecode')):
            lll1111l111l1111Il1l1.l1l1ll1l1ll111l1Il1l1()

    def l1l1ll1l1ll111l1Il1l1(lll1111l111l1111Il1l1) -> None:
        import numba.core.bytecode

        def l111l1ll11l1lll1Il1l1(llll11l11lll1111Il1l1) -> CodeType:  # type: ignore
            import ast
            l1ll11ll11l1111lIl1l1 = getattr(llll11l11lll1111Il1l1, '__code__', getattr(llll11l11lll1111Il1l1, 'func_code', None))  # type: ignore

            if ('__rw_mode__' in l1ll11ll11l1111lIl1l1.co_consts):  # type: ignore
                l1111l1111lll1l1Il1l1 = ast.parse(inspect.getsource(llll11l11lll1111Il1l1))
                ll11l1ll11lll1llIl1l1 = l1111l1111lll1l1Il1l1.body[0]
                ll11l1ll11lll1llIl1l1.decorator_list = []  # type: ignore

                ll1l1l11ll11ll11Il1l1 = compile(l1111l1111lll1l1Il1l1, filename=l1ll11ll11l1111lIl1l1.co_filename, mode='exec')  # type: ignore
                l1ll11ll11l1111lIl1l1 = ll1l1l11ll11ll11Il1l1.co_consts[0]

            return l1ll11ll11l1111lIl1l1  # type: ignore

        numba.core.bytecode.get_code_object.__code__ = l111l1ll11l1lll1Il1l1.__code__
