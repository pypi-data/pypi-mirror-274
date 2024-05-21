import asyncio
from contextlib import contextmanager
import os
from pathlib import Path
import sys
import types
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, List, Optional, Tuple, Type

from reloadium.corium.lll1llll1l1l1lllIl1l1 import ll11l1l11111l1llIl1l1
from reloadium.corium.ll1ll11ll111l1llIl1l1 import l1ll11l1l111111lIl1l1
from reloadium.corium.l1lll1ll11llll1lIl1l1.ll11ll1lll1llll1Il1l1 import llll1llllll1ll11Il1l1
from reloadium.lib.environ import env
from reloadium.corium.l1l111l1l11lll1lIl1l1 import l1l1111ll1llllllIl1l1
from reloadium.lib.ll11l11111lll11lIl1l1.ll11lll1ll11l11lIl1l1 import l1111l1lllll11llIl1l1, l1l11ll1l11ll1l1Il1l1
from reloadium.lib.ll11l11111lll11lIl1l1.lll11ll11ll11111Il1l1 import l1l11lll1l1l11llIl1l1
from reloadium.corium.ll11lll1ll11111lIl1l1 import l1ll1l111l11l111Il1l1, lll11l11lll1111lIl1l1, l1ll11lll1ll111lIl1l1, lll11ll1ll111111Il1l1, ll111llll11l1l11Il1l1
from reloadium.corium.l1l11111l11111l1Il1l1 import lllll1111llll1llIl1l1, ll111l1lllll1lllIl1l1
from reloadium.corium.l111l1l11ll1l1l1Il1l1 import llll1l11lllll1l1Il1l1
from reloadium.corium.l1lll1ll11llll1lIl1l1 import l1111111l1llll1lIl1l1
from dataclasses import dataclass, field


if (TYPE_CHECKING):
    from django.db import transaction
    from django.db.transaction import Atomic


__RELOADIUM__ = True


@dataclass(**ll111llll11l1l11Il1l1)
class l11l1l1l1111lll1Il1l1(lll11ll1ll111111Il1l1):
    l1111l111ll1ll1lIl1l1 = 'Field'

    @classmethod
    def l1l11ll1ll1lll11Il1l1(l11lllll1l111ll1Il1l1, ll1l11111l11ll11Il1l1: llll1l11lllll1l1Il1l1.l11llll11ll1lll1Il1l1, ll1lll1l11l1lll1Il1l1: Any, lll11ll11lll111lIl1l1: lll11l11lll1111lIl1l1) -> bool:
        from django.db.models.fields import Field

        if ((hasattr(ll1lll1l11l1lll1Il1l1, 'field') and isinstance(ll1lll1l11l1lll1Il1l1.field, Field))):
            return True

        return False

    def lllllll1l11ll111Il1l1(lll1l11111lll1l1Il1l1, l11llllll111l1llIl1l1: l1ll11lll1ll111lIl1l1) -> bool:
        return True

    @classmethod
    def llllllll11111ll1Il1l1(l11lllll1l111ll1Il1l1) -> int:
        return 200


@dataclass(repr=False)
class l1l1l1111l111lllIl1l1(l1111l1lllll11llIl1l1):
    l111ll1l1l1llll1Il1l1: "Atomic" = field(init=False)

    l11llll11llll11lIl1l1: bool = field(init=False, default=False)

    def ll1ll11l1l1l1lllIl1l1(lll1l11111lll1l1Il1l1) -> None:
        super().ll1ll11l1l1l1lllIl1l1()
        from django.db import transaction

        lll1l11111lll1l1Il1l1.l111ll1l1l1llll1Il1l1 = transaction.atomic()
        lll1l11111lll1l1Il1l1.l111ll1l1l1llll1Il1l1.__enter__()

    def l1ll11l11llll111Il1l1(lll1l11111lll1l1Il1l1) -> None:
        super().l1ll11l11llll111Il1l1()
        if (lll1l11111lll1l1Il1l1.l11llll11llll11lIl1l1):
            return 

        lll1l11111lll1l1Il1l1.l11llll11llll11lIl1l1 = True
        from django.db import transaction

        transaction.set_rollback(True)
        lll1l11111lll1l1Il1l1.l111ll1l1l1llll1Il1l1.__exit__(None, None, None)

    def ll1ll11lll1ll1l1Il1l1(lll1l11111lll1l1Il1l1) -> None:
        super().ll1ll11lll1ll1l1Il1l1()

        if (lll1l11111lll1l1Il1l1.l11llll11llll11lIl1l1):
            return 

        lll1l11111lll1l1Il1l1.l11llll11llll11lIl1l1 = True
        lll1l11111lll1l1Il1l1.l111ll1l1l1llll1Il1l1.__exit__(None, None, None)

    def __repr__(lll1l11111lll1l1Il1l1) -> str:
        return 'DbMemento'


@dataclass(repr=False)
class ll111111111ll1llIl1l1(l1l11ll1l11ll1l1Il1l1):
    l111ll1l1l1llll1Il1l1: "Atomic" = field(init=False)

    l11llll11llll11lIl1l1: bool = field(init=False, default=False)

    async def ll1ll11l1l1l1lllIl1l1(lll1l11111lll1l1Il1l1) -> None:
        await super().ll1ll11l1l1l1lllIl1l1()
        from django.db import transaction
        from asgiref.sync import sync_to_async

        lll1l11111lll1l1Il1l1.l111ll1l1l1llll1Il1l1 = transaction.atomic()


        with ll11l1l11111l1llIl1l1.ll11l1lll11l1l1lIl1l1.lll1l1111l1111l1Il1l1.l111l11l1ll11l11Il1l1(False):
            await sync_to_async(lll1l11111lll1l1Il1l1.l111ll1l1l1llll1Il1l1.__enter__)()

    async def l1ll11l11llll111Il1l1(lll1l11111lll1l1Il1l1) -> None:
        from asgiref.sync import sync_to_async

        await super().l1ll11l11llll111Il1l1()
        if (lll1l11111lll1l1Il1l1.l11llll11llll11lIl1l1):
            return 

        lll1l11111lll1l1Il1l1.l11llll11llll11lIl1l1 = True
        from django.db import transaction

        def l1lllll1l1l11lllIl1l1() -> None:
            transaction.set_rollback(True)
            lll1l11111lll1l1Il1l1.l111ll1l1l1llll1Il1l1.__exit__(None, None, None)
        with ll11l1l11111l1llIl1l1.ll11l1lll11l1l1lIl1l1.lll1l1111l1111l1Il1l1.l111l11l1ll11l11Il1l1(False):
            await sync_to_async(l1lllll1l1l11lllIl1l1)()

    async def ll1ll11lll1ll1l1Il1l1(lll1l11111lll1l1Il1l1) -> None:
        from asgiref.sync import sync_to_async

        await super().ll1ll11lll1ll1l1Il1l1()

        if (lll1l11111lll1l1Il1l1.l11llll11llll11lIl1l1):
            return 

        lll1l11111lll1l1Il1l1.l11llll11llll11lIl1l1 = True
        with ll11l1l11111l1llIl1l1.ll11l1lll11l1l1lIl1l1.lll1l1111l1111l1Il1l1.l111l11l1ll11l11Il1l1(False):
            await sync_to_async(lll1l11111lll1l1Il1l1.l111ll1l1l1llll1Il1l1.__exit__)(None, None, None)

    def __repr__(lll1l11111lll1l1Il1l1) -> str:
        return 'AsyncDbMemento'


@dataclass
class l11l111l1ll1llllIl1l1(l1l11lll1l1l11llIl1l1):
    ll1l1l1l11l111llIl1l1 = 'Django'

    l1l1l1111ll111llIl1l1: Optional[int] = field(init=False)
    l1ll111111lll11lIl1l1: Optional[Callable[..., Any]] = field(init=False, default=None)

    ll111l1lll1ll11lIl1l1: Any = field(init=False, default=None)
    lll11llllll111llIl1l1: Any = field(init=False, default=None)
    l111l111lll1l1l1Il1l1: Any = field(init=False, default=None)

    ll1ll11l1l1ll111Il1l1 = True

    def __post_init__(lll1l11111lll1l1Il1l1) -> None:
        super().__post_init__()
        lll1l11111lll1l1Il1l1.l1l1l1111ll111llIl1l1 = None

    def ll11l1l1llllll11Il1l1(lll1l11111lll1l1Il1l1) -> List[Type[l1ll11lll1ll111lIl1l1]]:
        return [l11l1l1l1111lll1Il1l1]

    def l11lll1111l1lll1Il1l1(lll1l11111lll1l1Il1l1) -> None:
        super().l11lll1111l1lll1Il1l1()
        if ('runserver' in sys.argv):
            sys.argv.append('--noreload')

    def l1lll11l111l1lllIl1l1(lll1l11111lll1l1Il1l1, l1ll111ll1ll11llIl1l1: types.ModuleType) -> None:
        if (lll1l11111lll1l1Il1l1.lll111ll1llllll1Il1l1(l1ll111ll1ll11llIl1l1, 'django.core.management.commands.runserver')):
            lll1l11111lll1l1Il1l1.ll111l1l1lllll1lIl1l1()
            if ( not lll1l11111lll1l1Il1l1.l111111111l1ll11Il1l1):
                lll1l11111lll1l1Il1l1.l111111111lllll1Il1l1()

    def llllll11l1l1ll1lIl1l1(lll1l11111lll1l1Il1l1) -> None:
        import django.core.management.commands.runserver

        django.core.management.commands.runserver.Command.handle = lll1l11111lll1l1Il1l1.ll111l1lll1ll11lIl1l1
        django.core.management.commands.runserver.Command.get_handler = lll1l11111lll1l1Il1l1.l111l111lll1l1l1Il1l1
        django.core.handlers.base.BaseHandler.get_response = lll1l11111lll1l1Il1l1.lll11llllll111llIl1l1

    def lll111111l11111lIl1l1(lll1l11111lll1l1Il1l1, l1l111lll1lll111Il1l1: str, l1111ll11l1l1111Il1l1: bool) -> Optional["lllll1111llll1llIl1l1"]:
        if (lll1l11111lll1l1Il1l1.l111111111l1ll11Il1l1):
            return None

        if ( not os.environ.get('DJANGO_SETTINGS_MODULE')):
            return None

        if (l1111ll11l1l1111Il1l1):
            return None
        else:
            lllll1l111111111Il1l1 = l1l1l1111l111lllIl1l1(l1l111lll1lll111Il1l1=l1l111lll1lll111Il1l1, ll11lll1ll11l11lIl1l1=lll1l11111lll1l1Il1l1)
            lllll1l111111111Il1l1.ll1ll11l1l1l1lllIl1l1()

        return lllll1l111111111Il1l1

    async def lllll11111111lllIl1l1(lll1l11111lll1l1Il1l1, l1l111lll1lll111Il1l1: str) -> Optional["ll111l1lllll1lllIl1l1"]:
        if (lll1l11111lll1l1Il1l1.l111111111l1ll11Il1l1):
            return None

        if ( not os.environ.get('DJANGO_SETTINGS_MODULE')):
            return None

        lllll1l111111111Il1l1 = ll111111111ll1llIl1l1(l1l111lll1lll111Il1l1=l1l111lll1lll111Il1l1, ll11lll1ll11l11lIl1l1=lll1l11111lll1l1Il1l1)
        await lllll1l111111111Il1l1.ll1ll11l1l1l1lllIl1l1()
        return lllll1l111111111Il1l1

    def ll111l1l1lllll1lIl1l1(lll1l11111lll1l1Il1l1) -> None:
        import django.core.management.commands.runserver

        lll1l11111lll1l1Il1l1.ll111l1lll1ll11lIl1l1 = django.core.management.commands.runserver.Command.handle

        def lll11ll1l11l1111Il1l1(*l11111l111l11lllIl1l1: Any, **l11l111111llll1lIl1l1: Any) -> Any:
            with l1l1111ll1llllllIl1l1():
                l11ll1l1111111llIl1l1 = l11l111111llll1lIl1l1.get('addrport')
                if ( not l11ll1l1111111llIl1l1):
                    l11ll1l1111111llIl1l1 = django.core.management.commands.runserver.Command.default_port

                l11ll1l1111111llIl1l1 = l11ll1l1111111llIl1l1.split(':')[ - 1]
                l11ll1l1111111llIl1l1 = int(l11ll1l1111111llIl1l1)
                lll1l11111lll1l1Il1l1.l1l1l1111ll111llIl1l1 = l11ll1l1111111llIl1l1

            return lll1l11111lll1l1Il1l1.ll111l1lll1ll11lIl1l1(*l11111l111l11lllIl1l1, **l11l111111llll1lIl1l1)

        llll1llllll1ll11Il1l1.ll11ll1lll1llll1Il1l1(django.core.management.commands.runserver.Command, 'handle', lll11ll1l11l1111Il1l1)

    def l111111111lllll1Il1l1(lll1l11111lll1l1Il1l1) -> None:
        import django.core.management.commands.runserver

        lll1l11111lll1l1Il1l1.l111l111lll1l1l1Il1l1 = django.core.management.commands.runserver.Command.get_handler

        def lll11ll1l11l1111Il1l1(*l11111l111l11lllIl1l1: Any, **l11l111111llll1lIl1l1: Any) -> Any:
            with l1l1111ll1llllllIl1l1():
                assert lll1l11111lll1l1Il1l1.l1l1l1111ll111llIl1l1
                lll1l11111lll1l1Il1l1.l1ll1111ll1l1111Il1l1 = lll1l11111lll1l1Il1l1.l1l1ll11ll111111Il1l1(lll1l11111lll1l1Il1l1.l1l1l1111ll111llIl1l1)
                if (env.page_reload_on_start):
                    lll1l11111lll1l1Il1l1.l1ll1111ll1l1111Il1l1.l11l11ll11111111Il1l1(2.0)

            return lll1l11111lll1l1Il1l1.l111l111lll1l1l1Il1l1(*l11111l111l11lllIl1l1, **l11l111111llll1lIl1l1)

        llll1llllll1ll11Il1l1.ll11ll1lll1llll1Il1l1(django.core.management.commands.runserver.Command, 'get_handler', lll11ll1l11l1111Il1l1)

    def ll1l1l11llll1111Il1l1(lll1l11111lll1l1Il1l1) -> None:
        super().ll1l1l11llll1111Il1l1()

        import django.core.handlers.base

        lll1l11111lll1l1Il1l1.lll11llllll111llIl1l1 = django.core.handlers.base.BaseHandler.get_response

        def lll11ll1l11l1111Il1l1(l11lll1ll11lll11Il1l1: Any, lllll1ll1ll1l1l1Il1l1: Any) -> Any:
            l11l1l1lll1lll1lIl1l1 = lll1l11111lll1l1Il1l1.lll11llllll111llIl1l1(l11lll1ll11lll11Il1l1, lllll1ll1ll1l1l1Il1l1)

            if ( not lll1l11111lll1l1Il1l1.l1ll1111ll1l1111Il1l1):
                return l11l1l1lll1lll1lIl1l1

            l11111111ll111l1Il1l1 = l11l1l1lll1lll1lIl1l1.get('content-type')

            if (( not l11111111ll111l1Il1l1 or 'text/html' not in l11111111ll111l1Il1l1)):
                return l11l1l1lll1lll1lIl1l1

            l111lllll11l1l11Il1l1 = l11l1l1lll1lll1lIl1l1.content

            if (isinstance(l111lllll11l1l11Il1l1, bytes)):
                l111lllll11l1l11Il1l1 = l111lllll11l1l11Il1l1.decode('utf-8')

            lll11l1lll1l1l11Il1l1 = lll1l11111lll1l1Il1l1.l1ll1111ll1l1111Il1l1.l111llll1111ll11Il1l1(l111lllll11l1l11Il1l1)

            l11l1l1lll1lll1lIl1l1.content = lll11l1lll1l1l11Il1l1.encode('utf-8')
            l11l1l1lll1lll1lIl1l1['content-length'] = str(len(l11l1l1lll1lll1lIl1l1.content)).encode('ascii')
            return l11l1l1lll1lll1lIl1l1

        django.core.handlers.base.BaseHandler.get_response = lll11ll1l11l1111Il1l1  # type: ignore

    def ll11111lll1ll11lIl1l1(lll1l11111lll1l1Il1l1, lll11llll1111111Il1l1: Path) -> None:
        super().ll11111lll1ll11lIl1l1(lll11llll1111111Il1l1)

        from django.apps.registry import Apps

        lll1l11111lll1l1Il1l1.l1ll111111lll11lIl1l1 = Apps.register_model

        def lll1l11l1l11ll11Il1l1(*l11111l111l11lllIl1l1: Any, **lll1l11l1l1ll111Il1l1: Any) -> Any:
            pass

        Apps.register_model = lll1l11l1l11ll11Il1l1

    def lll11111lllll1llIl1l1(lll1l11111lll1l1Il1l1, lll11llll1111111Il1l1: Path, l111lll111111l1lIl1l1: List[l1ll1l111l11l111Il1l1]) -> None:
        super().lll11111lllll1llIl1l1(lll11llll1111111Il1l1, l111lll111111l1lIl1l1)

        if ( not lll1l11111lll1l1Il1l1.l1ll111111lll11lIl1l1):
            return 

        from django.apps.registry import Apps

        Apps.register_model = lll1l11111lll1l1Il1l1.l1ll111111lll11lIl1l1

    def lll111llllll11l1Il1l1(lll1l11111lll1l1Il1l1, lll11llll1111111Il1l1: Path) -> None:
        try:
            from django.template.autoreload import get_template_directories, reset_loaders

            for l11lll1ll1l1ll11Il1l1 in get_template_directories():
                if (l11lll1ll1l1ll11Il1l1 in lll11llll1111111Il1l1.parents):
                    reset_loaders()
                    break
        except Exception:
            pass

        super().lll111llllll11l1Il1l1(lll11llll1111111Il1l1)

