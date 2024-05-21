import re
from contextlib import contextmanager
import os
import sys
import types
from pathlib import Path
from textwrap import dedent
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, List, Optional, Set, Tuple, Union

from reloadium.corium.l1l111l1l11lll1lIl1l1 import l1l1111ll1llllllIl1l1
from reloadium.corium.l1lll1ll11llll1lIl1l1.ll11ll1lll1llll1Il1l1 import llll1llllll1ll11Il1l1
from reloadium.lib.ll11l11111lll11lIl1l1.ll11lll1ll11l11lIl1l1 import l11111lll11111llIl1l1, l1111l1lllll11llIl1l1
from reloadium.corium.l1l11111l11111l1Il1l1 import lllll1111llll1llIl1l1
from reloadium.corium.l1lll1ll11llll1lIl1l1 import l1111111l1llll1lIl1l1
from dataclasses import dataclass, field

if (TYPE_CHECKING):
    from sqlalchemy.engine.base import Engine, Transaction
    from sqlalchemy.orm.session import Session


__RELOADIUM__ = True


@dataclass(repr=False)
class l1l1l1111l111lllIl1l1(l1111l1lllll11llIl1l1):
    ll11lll1ll11l11lIl1l1: "lllll11ll1ll111lIl1l1"
    l1l11ll111l1l111Il1l1: List["Transaction"] = field(init=False, default_factory=list)

    def ll1ll11l1l1l1lllIl1l1(lll1l11111lll1l1Il1l1) -> None:
        from sqlalchemy.orm.session import _sessions

        super().ll1ll11l1l1l1lllIl1l1()

        ll1llll1l111l1l1Il1l1 = list(_sessions.values())

        for l111l11l11l1111lIl1l1 in ll1llll1l111l1l1Il1l1:
            if ( not l111l11l11l1111lIl1l1.is_active):
                continue

            l11l111l11llllllIl1l1 = l111l11l11l1111lIl1l1.begin_nested()
            lll1l11111lll1l1Il1l1.l1l11ll111l1l111Il1l1.append(l11l111l11llllllIl1l1)

    def __repr__(lll1l11111lll1l1Il1l1) -> str:
        return 'DbMemento'

    def l1ll11l11llll111Il1l1(lll1l11111lll1l1Il1l1) -> None:
        super().l1ll11l11llll111Il1l1()

        while lll1l11111lll1l1Il1l1.l1l11ll111l1l111Il1l1:
            l11l111l11llllllIl1l1 = lll1l11111lll1l1Il1l1.l1l11ll111l1l111Il1l1.pop()
            if (l11l111l11llllllIl1l1.is_active):
                try:
                    l11l111l11llllllIl1l1.rollback()
                except :
                    pass

    def ll1ll11lll1ll1l1Il1l1(lll1l11111lll1l1Il1l1) -> None:
        super().ll1ll11lll1ll1l1Il1l1()

        while lll1l11111lll1l1Il1l1.l1l11ll111l1l111Il1l1:
            l11l111l11llllllIl1l1 = lll1l11111lll1l1Il1l1.l1l11ll111l1l111Il1l1.pop()
            if (l11l111l11llllllIl1l1.is_active):
                try:
                    l11l111l11llllllIl1l1.commit()
                except :
                    pass


@dataclass
class lllll11ll1ll111lIl1l1(l11111lll11111llIl1l1):
    ll1l1l1l11l111llIl1l1 = 'Sqlalchemy'

    ll1lllll11l1lll1Il1l1: List["Engine"] = field(init=False, default_factory=list)
    ll1llll1l111l1l1Il1l1: Set["Session"] = field(init=False, default_factory=set)
    l1l11llllll111llIl1l1: Tuple[int, ...] = field(init=False)

    def l1lll11l111l1lllIl1l1(lll1l11111lll1l1Il1l1, l1ll111ll1ll11llIl1l1: types.ModuleType) -> None:
        if (lll1l11111lll1l1Il1l1.lll111ll1llllll1Il1l1(l1ll111ll1ll11llIl1l1, 'sqlalchemy')):
            lll1l11111lll1l1Il1l1.llll111ll111lll1Il1l1(l1ll111ll1ll11llIl1l1)

        if (lll1l11111lll1l1Il1l1.lll111ll1llllll1Il1l1(l1ll111ll1ll11llIl1l1, 'sqlalchemy.engine.base')):
            lll1l11111lll1l1Il1l1.l1l1111lllll11llIl1l1(l1ll111ll1ll11llIl1l1)

    def llll111ll111lll1Il1l1(lll1l11111lll1l1Il1l1, l1ll111ll1ll11llIl1l1: Any) -> None:
        l111lllll11l1l11Il1l1 = Path(l1ll111ll1ll11llIl1l1.__file__).read_text(encoding='utf-8')
        __version__ = re.findall('__version__\\s*?=\\s*?"(.*?)"', l111lllll11l1l11Il1l1)[0]

        lll11llll1l1111lIl1l1 = [int(llll1l1l1l1l11llIl1l1) for llll1l1l1l1l11llIl1l1 in __version__.split('.')]
        lll1l11111lll1l1Il1l1.l1l11llllll111llIl1l1 = tuple(lll11llll1l1111lIl1l1)

    def lll111111l11111lIl1l1(lll1l11111lll1l1Il1l1, l1l111lll1lll111Il1l1: str, l1111ll11l1l1111Il1l1: bool) -> Optional["lllll1111llll1llIl1l1"]:
        lllll1l111111111Il1l1 = l1l1l1111l111lllIl1l1(l1l111lll1lll111Il1l1=l1l111lll1lll111Il1l1, ll11lll1ll11l11lIl1l1=lll1l11111lll1l1Il1l1)
        lllll1l111111111Il1l1.ll1ll11l1l1l1lllIl1l1()
        return lllll1l111111111Il1l1

    def l1l1111lllll11llIl1l1(lll1l11111lll1l1Il1l1, l1ll111ll1ll11llIl1l1: Any) -> None:
        lll11ll1ll111ll1Il1l1 = locals().copy()

        lll11ll1ll111ll1Il1l1.update({'original': l1ll111ll1ll11llIl1l1.Engine.__init__, 'reloader_code': l1l1111ll1llllllIl1l1, 'engines': lll1l11111lll1l1Il1l1.ll1lllll11l1lll1Il1l1})





        ll1111lllll111llIl1l1 = dedent('\n            def patched(\n                    self2: Any,\n                    pool: Any,\n                    dialect: Any,\n                    url: Any,\n                    logging_name: Any = None,\n                    echo: Any = None,\n                    proxy: Any = None,\n                    execution_options: Any = None,\n                    hide_parameters: Any = None,\n            ) -> Any:\n                original(self2,\n                         pool,\n                         dialect,\n                         url,\n                         logging_name,\n                         echo,\n                         proxy,\n                         execution_options,\n                         hide_parameters\n                         )\n                with reloader_code():\n                    engines.append(self2)')
























        l11ll1l1ll11l11lIl1l1 = dedent('\n            def patched(\n                    self2: Any,\n                    pool: Any,\n                    dialect: Any,\n                    url: Any,\n                    logging_name: Any = None,\n                    echo: Any = None,\n                    query_cache_size: Any = 500,\n                    execution_options: Any = None,\n                    hide_parameters: Any = False,\n            ) -> Any:\n                original(self2,\n                         pool,\n                         dialect,\n                         url,\n                         logging_name,\n                         echo,\n                         query_cache_size,\n                         execution_options,\n                         hide_parameters)\n                with reloader_code():\n                    engines.append(self2)\n        ')
























        if (lll1l11111lll1l1Il1l1.l1l11llllll111llIl1l1 <= (1, 3, 24, )):
            exec(ll1111lllll111llIl1l1, {**globals(), **lll11ll1ll111ll1Il1l1}, lll11ll1ll111ll1Il1l1)
        else:
            exec(l11ll1l1ll11l11lIl1l1, {**globals(), **lll11ll1ll111ll1Il1l1}, lll11ll1ll111ll1Il1l1)

        llll1llllll1ll11Il1l1.ll11ll1lll1llll1Il1l1(l1ll111ll1ll11llIl1l1.Engine, '__init__', lll11ll1ll111ll1Il1l1['patched'])
