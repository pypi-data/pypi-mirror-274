import re
from contextlib import contextmanager
import os
import sys
import types
from pathlib import Path
from textwrap import dedent
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, List, Optional, Set, Tuple, Union

from reloadium.corium.lllll11ll11ll1l1Il1l1 import l1l11llll11llll1Il1l1
from reloadium.corium.ll1l1l1ll1111lllIl1l1.l111ll1ll111llllIl1l1 import ll1lll1lll1l1l1lIl1l1
from reloadium.lib.ll1lll1l11l11111Il1l1.l11l1lll1l11l111Il1l1 import llll1l1l11llll11Il1l1, llll1lll11l1ll1lIl1l1
from reloadium.corium.l1111l11ll111lllIl1l1 import lll11lll11lll111Il1l1
from reloadium.corium.ll1l1l1ll1111lllIl1l1 import l1l11lll1l1l1lllIl1l1
from dataclasses import dataclass, field

if (TYPE_CHECKING):
    from sqlalchemy.engine.base import Engine, Transaction
    from sqlalchemy.orm.session import Session


__RELOADIUM__ = True


@dataclass(repr=False)
class l1l1ll111l11l11lIl1l1(llll1lll11l1ll1lIl1l1):
    l11l1lll1l11l111Il1l1: "ll1l111111l1l1l1Il1l1"
    ll1l11ll1ll1111lIl1l1: List["Transaction"] = field(init=False, default_factory=list)

    def llll1l1l11l1llllIl1l1(lll1111l111l1111Il1l1) -> None:
        from sqlalchemy.orm.session import _sessions

        super().llll1l1l11l1llllIl1l1()

        l1l11lll1l111111Il1l1 = list(_sessions.values())

        for l1llll11ll1ll11lIl1l1 in l1l11lll1l111111Il1l1:
            if ( not l1llll11ll1ll11lIl1l1.is_active):
                continue

            ll1llll1ll1l111lIl1l1 = l1llll11ll1ll11lIl1l1.begin_nested()
            lll1111l111l1111Il1l1.ll1l11ll1ll1111lIl1l1.append(ll1llll1ll1l111lIl1l1)

    def __repr__(lll1111l111l1111Il1l1) -> str:
        return 'DbMemento'

    def lll1l1lllll1l1llIl1l1(lll1111l111l1111Il1l1) -> None:
        super().lll1l1lllll1l1llIl1l1()

        while lll1111l111l1111Il1l1.ll1l11ll1ll1111lIl1l1:
            ll1llll1ll1l111lIl1l1 = lll1111l111l1111Il1l1.ll1l11ll1ll1111lIl1l1.pop()
            if (ll1llll1ll1l111lIl1l1.is_active):
                try:
                    ll1llll1ll1l111lIl1l1.rollback()
                except :
                    pass

    def l11l1ll1l1lllll1Il1l1(lll1111l111l1111Il1l1) -> None:
        super().l11l1ll1l1lllll1Il1l1()

        while lll1111l111l1111Il1l1.ll1l11ll1ll1111lIl1l1:
            ll1llll1ll1l111lIl1l1 = lll1111l111l1111Il1l1.ll1l11ll1ll1111lIl1l1.pop()
            if (ll1llll1ll1l111lIl1l1.is_active):
                try:
                    ll1llll1ll1l111lIl1l1.commit()
                except :
                    pass


@dataclass
class ll1l111111l1l1l1Il1l1(llll1l1l11llll11Il1l1):
    ll11111lll1l1111Il1l1 = 'Sqlalchemy'

    l1111l1lll1l1l11Il1l1: List["Engine"] = field(init=False, default_factory=list)
    l1l11lll1l111111Il1l1: Set["Session"] = field(init=False, default_factory=set)
    l1l1ll1111111l11Il1l1: Tuple[int, ...] = field(init=False)

    def l1ll11lll111ll11Il1l1(lll1111l111l1111Il1l1, l111l1l1ll1l1l1lIl1l1: types.ModuleType) -> None:
        if (lll1111l111l1111Il1l1.l1l1l1l111111lllIl1l1(l111l1l1ll1l1l1lIl1l1, 'sqlalchemy')):
            lll1111l111l1111Il1l1.lll1ll1l11l1ll1lIl1l1(l111l1l1ll1l1l1lIl1l1)

        if (lll1111l111l1111Il1l1.l1l1l1l111111lllIl1l1(l111l1l1ll1l1l1lIl1l1, 'sqlalchemy.engine.base')):
            lll1111l111l1111Il1l1.l1lll1lll1l11ll1Il1l1(l111l1l1ll1l1l1lIl1l1)

    def lll1ll1l11l1ll1lIl1l1(lll1111l111l1111Il1l1, l111l1l1ll1l1l1lIl1l1: Any) -> None:
        l1111111l11l1lllIl1l1 = Path(l111l1l1ll1l1l1lIl1l1.__file__).read_text(encoding='utf-8')
        __version__ = re.findall('__version__\\s*?=\\s*?"(.*?)"', l1111111l11l1lllIl1l1)[0]

        l11l1l111l1111l1Il1l1 = [int(l1llllllll11llllIl1l1) for l1llllllll11llllIl1l1 in __version__.split('.')]
        lll1111l111l1111Il1l1.l1l1ll1111111l11Il1l1 = tuple(l11l1l111l1111l1Il1l1)

    def lll111lll11111llIl1l1(lll1111l111l1111Il1l1, ll11lll111lll1l1Il1l1: str, l11lll1l1lll11l1Il1l1: bool) -> Optional["lll11lll11lll111Il1l1"]:
        l1ll11ll11l1111lIl1l1 = l1l1ll111l11l11lIl1l1(ll11lll111lll1l1Il1l1=ll11lll111lll1l1Il1l1, l11l1lll1l11l111Il1l1=lll1111l111l1111Il1l1)
        l1ll11ll11l1111lIl1l1.llll1l1l11l1llllIl1l1()
        return l1ll11ll11l1111lIl1l1

    def l1lll1lll1l11ll1Il1l1(lll1111l111l1111Il1l1, l111l1l1ll1l1l1lIl1l1: Any) -> None:
        l11ll11llll1ll1lIl1l1 = locals().copy()

        l11ll11llll1ll1lIl1l1.update({'original': l111l1l1ll1l1l1lIl1l1.Engine.__init__, 'reloader_code': l1l11llll11llll1Il1l1, 'engines': lll1111l111l1111Il1l1.l1111l1lll1l1l11Il1l1})





        l1l1l111lllll11lIl1l1 = dedent('\n            def patched(\n                    self2: Any,\n                    pool: Any,\n                    dialect: Any,\n                    url: Any,\n                    logging_name: Any = None,\n                    echo: Any = None,\n                    proxy: Any = None,\n                    execution_options: Any = None,\n                    hide_parameters: Any = None,\n            ) -> Any:\n                original(self2,\n                         pool,\n                         dialect,\n                         url,\n                         logging_name,\n                         echo,\n                         proxy,\n                         execution_options,\n                         hide_parameters\n                         )\n                with reloader_code():\n                    engines.append(self2)')
























        lll11l1l1lllll11Il1l1 = dedent('\n            def patched(\n                    self2: Any,\n                    pool: Any,\n                    dialect: Any,\n                    url: Any,\n                    logging_name: Any = None,\n                    echo: Any = None,\n                    query_cache_size: Any = 500,\n                    execution_options: Any = None,\n                    hide_parameters: Any = False,\n            ) -> Any:\n                original(self2,\n                         pool,\n                         dialect,\n                         url,\n                         logging_name,\n                         echo,\n                         query_cache_size,\n                         execution_options,\n                         hide_parameters)\n                with reloader_code():\n                    engines.append(self2)\n        ')
























        if (lll1111l111l1111Il1l1.l1l1ll1111111l11Il1l1 <= (1, 3, 24, )):
            exec(l1l1l111lllll11lIl1l1, {**globals(), **l11ll11llll1ll1lIl1l1}, l11ll11llll1ll1lIl1l1)
        else:
            exec(lll11l1l1lllll11Il1l1, {**globals(), **l11ll11llll1ll1lIl1l1}, l11ll11llll1ll1lIl1l1)

        ll1lll1lll1l1l1lIl1l1.l111ll1ll111llllIl1l1(l111l1l1ll1l1l1lIl1l1.Engine, '__init__', l11ll11llll1ll1lIl1l1['patched'])
