import asyncio
from contextlib import contextmanager
import os
from pathlib import Path
import sys
import types
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, List, Optional, Tuple, Type

from reloadium.corium.l11lll1ll11l1111Il1l1 import llll11l1l1111lllIl1l1
from reloadium.corium.lll11l1111l1l11lIl1l1 import l1lll111l11l1l1lIl1l1
from reloadium.corium.ll1l1l1ll1111lllIl1l1.l111ll1ll111llllIl1l1 import ll1lll1lll1l1l1lIl1l1
from reloadium.lib.environ import env
from reloadium.corium.lllll11ll11ll1l1Il1l1 import l1l11llll11llll1Il1l1
from reloadium.lib.ll1lll1l11l11111Il1l1.l11l1lll1l11l111Il1l1 import llll1lll11l1ll1lIl1l1, lllll111llllll11Il1l1
from reloadium.lib.ll1lll1l11l11111Il1l1.lll1ll1ll111l1llIl1l1 import lll1ll1111111ll1Il1l1
from reloadium.corium.ll111ll1l11l1ll1Il1l1 import l111111l111l1ll1Il1l1, ll1l111ll1111l1lIl1l1, l1llllllll1l1l1lIl1l1, llll1l1ll1l111llIl1l1, ll1ll1l1111ll1l1Il1l1
from reloadium.corium.l1111l11ll111lllIl1l1 import lll11lll11lll111Il1l1, l1l1ll11111ll1l1Il1l1
from reloadium.corium.lll1ll1lll1l1l1lIl1l1 import llll11ll11l1l11lIl1l1
from reloadium.corium.ll1l1l1ll1111lllIl1l1 import l1l11lll1l1l1lllIl1l1
from dataclasses import dataclass, field


if (TYPE_CHECKING):
    from django.db import transaction
    from django.db.transaction import Atomic


__RELOADIUM__ = True


@dataclass(**ll1ll1l1111ll1l1Il1l1)
class l1l1lll1ll111l11Il1l1(llll1l1ll1l111llIl1l1):
    l111lllll1111l11Il1l1 = 'Field'

    @classmethod
    def llll11111lllllllIl1l1(lll1l1ll1ll1l1l1Il1l1, llll11111l1l1lllIl1l1: llll11ll11l1l11lIl1l1.l1ll1l1l1lll1111Il1l1, ll11l11l111l111lIl1l1: Any, lll1l111111111llIl1l1: ll1l111ll1111l1lIl1l1) -> bool:
        from django.db.models.fields import Field

        if ((hasattr(ll11l11l111l111lIl1l1, 'field') and isinstance(ll11l11l111l111lIl1l1.field, Field))):
            return True

        return False

    def l1l1ll1ll1l111l1Il1l1(lll1111l111l1111Il1l1, l1l1111l11l1llllIl1l1: l1llllllll1l1l1lIl1l1) -> bool:
        return True

    @classmethod
    def l1l1l1l1l111ll11Il1l1(lll1l1ll1ll1l1l1Il1l1) -> int:
        return 200


@dataclass(repr=False)
class l1l1ll111l11l11lIl1l1(llll1lll11l1ll1lIl1l1):
    ll11l111111l1l11Il1l1: "Atomic" = field(init=False)

    lll1l11ll111ll11Il1l1: bool = field(init=False, default=False)

    def llll1l1l11l1llllIl1l1(lll1111l111l1111Il1l1) -> None:
        super().llll1l1l11l1llllIl1l1()
        from django.db import transaction

        lll1111l111l1111Il1l1.ll11l111111l1l11Il1l1 = transaction.atomic()
        lll1111l111l1111Il1l1.ll11l111111l1l11Il1l1.__enter__()

    def lll1l1lllll1l1llIl1l1(lll1111l111l1111Il1l1) -> None:
        super().lll1l1lllll1l1llIl1l1()
        if (lll1111l111l1111Il1l1.lll1l11ll111ll11Il1l1):
            return 

        lll1111l111l1111Il1l1.lll1l11ll111ll11Il1l1 = True
        from django.db import transaction

        transaction.set_rollback(True)
        lll1111l111l1111Il1l1.ll11l111111l1l11Il1l1.__exit__(None, None, None)

    def l11l1ll1l1lllll1Il1l1(lll1111l111l1111Il1l1) -> None:
        super().l11l1ll1l1lllll1Il1l1()

        if (lll1111l111l1111Il1l1.lll1l11ll111ll11Il1l1):
            return 

        lll1111l111l1111Il1l1.lll1l11ll111ll11Il1l1 = True
        lll1111l111l1111Il1l1.ll11l111111l1l11Il1l1.__exit__(None, None, None)

    def __repr__(lll1111l111l1111Il1l1) -> str:
        return 'DbMemento'


@dataclass(repr=False)
class ll1ll11l1l111111Il1l1(lllll111llllll11Il1l1):
    ll11l111111l1l11Il1l1: "Atomic" = field(init=False)

    lll1l11ll111ll11Il1l1: bool = field(init=False, default=False)

    async def llll1l1l11l1llllIl1l1(lll1111l111l1111Il1l1) -> None:
        await super().llll1l1l11l1llllIl1l1()
        from django.db import transaction
        from asgiref.sync import sync_to_async

        lll1111l111l1111Il1l1.ll11l111111l1l11Il1l1 = transaction.atomic()


        with llll11l1l1111lllIl1l1.l1l1lll11ll11l11Il1l1.l1l111llll1lll1lIl1l1.llll1l1l11ll1111Il1l1(False):
            await sync_to_async(lll1111l111l1111Il1l1.ll11l111111l1l11Il1l1.__enter__)()

    async def lll1l1lllll1l1llIl1l1(lll1111l111l1111Il1l1) -> None:
        from asgiref.sync import sync_to_async

        await super().lll1l1lllll1l1llIl1l1()
        if (lll1111l111l1111Il1l1.lll1l11ll111ll11Il1l1):
            return 

        lll1111l111l1111Il1l1.lll1l11ll111ll11Il1l1 = True
        from django.db import transaction

        def llllll1llll1llllIl1l1() -> None:
            transaction.set_rollback(True)
            lll1111l111l1111Il1l1.ll11l111111l1l11Il1l1.__exit__(None, None, None)
        with llll11l1l1111lllIl1l1.l1l1lll11ll11l11Il1l1.l1l111llll1lll1lIl1l1.llll1l1l11ll1111Il1l1(False):
            await sync_to_async(llllll1llll1llllIl1l1)()

    async def l11l1ll1l1lllll1Il1l1(lll1111l111l1111Il1l1) -> None:
        from asgiref.sync import sync_to_async

        await super().l11l1ll1l1lllll1Il1l1()

        if (lll1111l111l1111Il1l1.lll1l11ll111ll11Il1l1):
            return 

        lll1111l111l1111Il1l1.lll1l11ll111ll11Il1l1 = True
        with llll11l1l1111lllIl1l1.l1l1lll11ll11l11Il1l1.l1l111llll1lll1lIl1l1.llll1l1l11ll1111Il1l1(False):
            await sync_to_async(lll1111l111l1111Il1l1.ll11l111111l1l11Il1l1.__exit__)(None, None, None)

    def __repr__(lll1111l111l1111Il1l1) -> str:
        return 'AsyncDbMemento'


@dataclass
class ll11l111ll1ll1l1Il1l1(lll1ll1111111ll1Il1l1):
    ll11111lll1l1111Il1l1 = 'Django'

    ll1ll11111l1l1llIl1l1: Optional[int] = field(init=False)
    ll11111l1l111ll1Il1l1: Optional[Callable[..., Any]] = field(init=False, default=None)

    lll1l111ll1l1111Il1l1: Any = field(init=False, default=None)
    l1111111l11l1111Il1l1: Any = field(init=False, default=None)
    l11l111l11l1llllIl1l1: Any = field(init=False, default=None)

    llllllll11lll111Il1l1 = True

    def __post_init__(lll1111l111l1111Il1l1) -> None:
        super().__post_init__()
        lll1111l111l1111Il1l1.ll1ll11111l1l1llIl1l1 = None

    def l11ll1l1111ll1llIl1l1(lll1111l111l1111Il1l1) -> List[Type[l1llllllll1l1l1lIl1l1]]:
        return [l1l1lll1ll111l11Il1l1]

    def llllll1ll1ll1lllIl1l1(lll1111l111l1111Il1l1) -> None:
        super().llllll1ll1ll1lllIl1l1()
        if ('runserver' in sys.argv):
            sys.argv.append('--noreload')

    def l1ll11lll111ll11Il1l1(lll1111l111l1111Il1l1, l111l1l1ll1l1l1lIl1l1: types.ModuleType) -> None:
        if (lll1111l111l1111Il1l1.l1l1l1l111111lllIl1l1(l111l1l1ll1l1l1lIl1l1, 'django.core.management.commands.runserver')):
            lll1111l111l1111Il1l1.ll111lll1ll11lllIl1l1()
            if ( not lll1111l111l1111Il1l1.lll111l1lllll111Il1l1):
                lll1111l111l1111Il1l1.l1111l11l11ll1l1Il1l1()

    def l11lll1l11l1111lIl1l1(lll1111l111l1111Il1l1) -> None:
        import django.core.management.commands.runserver

        django.core.management.commands.runserver.Command.handle = lll1111l111l1111Il1l1.lll1l111ll1l1111Il1l1
        django.core.management.commands.runserver.Command.get_handler = lll1111l111l1111Il1l1.l11l111l11l1llllIl1l1
        django.core.handlers.base.BaseHandler.get_response = lll1111l111l1111Il1l1.l1111111l11l1111Il1l1

    def lll111lll11111llIl1l1(lll1111l111l1111Il1l1, ll11lll111lll1l1Il1l1: str, l11lll1l1lll11l1Il1l1: bool) -> Optional["lll11lll11lll111Il1l1"]:
        if (lll1111l111l1111Il1l1.lll111l1lllll111Il1l1):
            return None

        if ( not os.environ.get('DJANGO_SETTINGS_MODULE')):
            return None

        if (l11lll1l1lll11l1Il1l1):
            return None
        else:
            l1ll11ll11l1111lIl1l1 = l1l1ll111l11l11lIl1l1(ll11lll111lll1l1Il1l1=ll11lll111lll1l1Il1l1, l11l1lll1l11l111Il1l1=lll1111l111l1111Il1l1)
            l1ll11ll11l1111lIl1l1.llll1l1l11l1llllIl1l1()

        return l1ll11ll11l1111lIl1l1

    async def ll1ll1l1lll11111Il1l1(lll1111l111l1111Il1l1, ll11lll111lll1l1Il1l1: str) -> Optional["l1l1ll11111ll1l1Il1l1"]:
        if (lll1111l111l1111Il1l1.lll111l1lllll111Il1l1):
            return None

        if ( not os.environ.get('DJANGO_SETTINGS_MODULE')):
            return None

        l1ll11ll11l1111lIl1l1 = ll1ll11l1l111111Il1l1(ll11lll111lll1l1Il1l1=ll11lll111lll1l1Il1l1, l11l1lll1l11l111Il1l1=lll1111l111l1111Il1l1)
        await l1ll11ll11l1111lIl1l1.llll1l1l11l1llllIl1l1()
        return l1ll11ll11l1111lIl1l1

    def ll111lll1ll11lllIl1l1(lll1111l111l1111Il1l1) -> None:
        import django.core.management.commands.runserver

        lll1111l111l1111Il1l1.lll1l111ll1l1111Il1l1 = django.core.management.commands.runserver.Command.handle

        def l1l1ll1l1ll11111Il1l1(*l1l1111l11l111llIl1l1: Any, **l1l1111ll111l111Il1l1: Any) -> Any:
            with l1l11llll11llll1Il1l1():
                lll11llll1llllllIl1l1 = l1l1111ll111l111Il1l1.get('addrport')
                if ( not lll11llll1llllllIl1l1):
                    lll11llll1llllllIl1l1 = django.core.management.commands.runserver.Command.default_port

                lll11llll1llllllIl1l1 = lll11llll1llllllIl1l1.split(':')[ - 1]
                lll11llll1llllllIl1l1 = int(lll11llll1llllllIl1l1)
                lll1111l111l1111Il1l1.ll1ll11111l1l1llIl1l1 = lll11llll1llllllIl1l1

            return lll1111l111l1111Il1l1.lll1l111ll1l1111Il1l1(*l1l1111l11l111llIl1l1, **l1l1111ll111l111Il1l1)

        ll1lll1lll1l1l1lIl1l1.l111ll1ll111llllIl1l1(django.core.management.commands.runserver.Command, 'handle', l1l1ll1l1ll11111Il1l1)

    def l1111l11l11ll1l1Il1l1(lll1111l111l1111Il1l1) -> None:
        import django.core.management.commands.runserver

        lll1111l111l1111Il1l1.l11l111l11l1llllIl1l1 = django.core.management.commands.runserver.Command.get_handler

        def l1l1ll1l1ll11111Il1l1(*l1l1111l11l111llIl1l1: Any, **l1l1111ll111l111Il1l1: Any) -> Any:
            with l1l11llll11llll1Il1l1():
                assert lll1111l111l1111Il1l1.ll1ll11111l1l1llIl1l1
                lll1111l111l1111Il1l1.l11lll111lll11llIl1l1 = lll1111l111l1111Il1l1.ll11lll11l11lll1Il1l1(lll1111l111l1111Il1l1.ll1ll11111l1l1llIl1l1)
                if (env.page_reload_on_start):
                    lll1111l111l1111Il1l1.l11lll111lll11llIl1l1.ll1111l1111l11l1Il1l1(2.0)

            return lll1111l111l1111Il1l1.l11l111l11l1llllIl1l1(*l1l1111l11l111llIl1l1, **l1l1111ll111l111Il1l1)

        ll1lll1lll1l1l1lIl1l1.l111ll1ll111llllIl1l1(django.core.management.commands.runserver.Command, 'get_handler', l1l1ll1l1ll11111Il1l1)

    def llllllll1lll1l1lIl1l1(lll1111l111l1111Il1l1) -> None:
        super().llllllll1lll1l1lIl1l1()

        import django.core.handlers.base

        lll1111l111l1111Il1l1.l1111111l11l1111Il1l1 = django.core.handlers.base.BaseHandler.get_response

        def l1l1ll1l1ll11111Il1l1(l1111111ll1llll1Il1l1: Any, ll11l11l11l111llIl1l1: Any) -> Any:
            l1111ll1l11l1ll1Il1l1 = lll1111l111l1111Il1l1.l1111111l11l1111Il1l1(l1111111ll1llll1Il1l1, ll11l11l11l111llIl1l1)

            if ( not lll1111l111l1111Il1l1.l11lll111lll11llIl1l1):
                return l1111ll1l11l1ll1Il1l1

            ll1ll1l111ll111lIl1l1 = l1111ll1l11l1ll1Il1l1.get('content-type')

            if (( not ll1ll1l111ll111lIl1l1 or 'text/html' not in ll1ll1l111ll111lIl1l1)):
                return l1111ll1l11l1ll1Il1l1

            l1111111l11l1lllIl1l1 = l1111ll1l11l1ll1Il1l1.content

            if (isinstance(l1111111l11l1lllIl1l1, bytes)):
                l1111111l11l1lllIl1l1 = l1111111l11l1lllIl1l1.decode('utf-8')

            l11l1lll11l1llllIl1l1 = lll1111l111l1111Il1l1.l11lll111lll11llIl1l1.lll1l1ll11111111Il1l1(l1111111l11l1lllIl1l1)

            l1111ll1l11l1ll1Il1l1.content = l11l1lll11l1llllIl1l1.encode('utf-8')
            l1111ll1l11l1ll1Il1l1['content-length'] = str(len(l1111ll1l11l1ll1Il1l1.content)).encode('ascii')
            return l1111ll1l11l1ll1Il1l1

        django.core.handlers.base.BaseHandler.get_response = l1l1ll1l1ll11111Il1l1  # type: ignore

    def lllll1l1ll11111lIl1l1(lll1111l111l1111Il1l1, lllll11l1l1ll1llIl1l1: Path) -> None:
        super().lllll1l1ll11111lIl1l1(lllll11l1l1ll1llIl1l1)

        from django.apps.registry import Apps

        lll1111l111l1111Il1l1.ll11111l1l111ll1Il1l1 = Apps.register_model

        def l1l111ll1lll1111Il1l1(*l1l1111l11l111llIl1l1: Any, **llll11ll11l1l111Il1l1: Any) -> Any:
            pass

        Apps.register_model = l1l111ll1lll1111Il1l1

    def ll11l1lllll111l1Il1l1(lll1111l111l1111Il1l1, lllll11l1l1ll1llIl1l1: Path, ll1l1l1llll1ll11Il1l1: List[l111111l111l1ll1Il1l1]) -> None:
        super().ll11l1lllll111l1Il1l1(lllll11l1l1ll1llIl1l1, ll1l1l1llll1ll11Il1l1)

        if ( not lll1111l111l1111Il1l1.ll11111l1l111ll1Il1l1):
            return 

        from django.apps.registry import Apps

        Apps.register_model = lll1111l111l1111Il1l1.ll11111l1l111ll1Il1l1

    def ll1lll1l1l1lll11Il1l1(lll1111l111l1111Il1l1, lllll11l1l1ll1llIl1l1: Path) -> None:
        try:
            from django.template.autoreload import get_template_directories, reset_loaders

            for lll1ll11111111llIl1l1 in get_template_directories():
                if (lll1ll11111111llIl1l1 in lllll11l1l1ll1llIl1l1.parents):
                    reset_loaders()
                    break
        except Exception:
            pass

        super().ll1lll1l1l1lll11Il1l1(lllll11l1l1ll1llIl1l1)

