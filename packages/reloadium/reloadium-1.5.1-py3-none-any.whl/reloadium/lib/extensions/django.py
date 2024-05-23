import asyncio
from contextlib import contextmanager
import os
from pathlib import Path
import sys
import types
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, List, Optional, Tuple, Type

from reloadium.corium.globals import g
from reloadium.corium.license import FreeLicense
from reloadium.corium.utils.patch import monkey_patcher
from reloadium.lib.environ import env
from reloadium.corium.exceptions import reloader_code
from reloadium.lib.extensions.extension import ExtensionMemento, AsyncExtensionMemento
from reloadium.lib.extensions.server_extension import ServerExtension
from reloadium.corium.objects import Action, Container, Object, Variable, obj_dc
from reloadium.corium.state import Memento, AsyncMemento
from reloadium.corium.static_anal import symbols
from reloadium.corium.utils import misc
from dataclasses import dataclass, field


if TYPE_CHECKING:
    from django.db import transaction
    from django.db.transaction import Atomic


__RELOADIUM__ = True


@dataclass(**obj_dc)
class Field(Variable):
    TYPE_NAME = "Field"

    @classmethod
    def is_candidate(cls, sym: symbols.Symbol, py_obj: Any, potential_parent: Container) -> bool:
        from django.db.models.fields import Field

        if hasattr(py_obj, "field") and isinstance(py_obj.field, Field):
            return True

        return False

    def compare(self, against: Object) -> bool:
        return True

    @classmethod
    def get_rank(cls) -> int:
        return 200


@dataclass(repr=False)
class DbMemento(ExtensionMemento):
    transaction: "Atomic" = field(init=False)

    transaction_end: bool = field(init=False, default=False)

    def create(self) -> None:
        super().create()
        from django.db import transaction

        self.transaction = transaction.atomic()
        self.transaction.__enter__()

    def restore(self) -> None:
        super().restore()
        if self.transaction_end:
            return

        self.transaction_end = True
        from django.db import transaction

        transaction.set_rollback(True)
        self.transaction.__exit__(None, None, None)

    def cleanup(self) -> None:
        super().cleanup()

        if self.transaction_end:
            return

        self.transaction_end = True
        self.transaction.__exit__(None, None, None)

    def __repr__(self) -> str:
        return "DbMemento"


@dataclass(repr=False)
class AsyncDbMemento(AsyncExtensionMemento):
    transaction: "Atomic" = field(init=False)

    transaction_end: bool = field(init=False, default=False)

    async def create(self) -> None:
        await super().create()
        from django.db import transaction
        from asgiref.sync import sync_to_async

        self.transaction = transaction.atomic()

        # sync_to_async is interfering with tracing for some reason
        with g.core.fast_debug.trace_enabled(False):
            await sync_to_async(self.transaction.__enter__)()

    async def restore(self) -> None:
        from asgiref.sync import sync_to_async

        await super().restore()
        if self.transaction_end:
            return

        self.transaction_end = True
        from django.db import transaction

        def sync() -> None:
            transaction.set_rollback(True)
            self.transaction.__exit__(None, None, None)
        with g.core.fast_debug.trace_enabled(False):
            await sync_to_async(sync)()

    async def cleanup(self) -> None:
        from asgiref.sync import sync_to_async

        await super().cleanup()

        if self.transaction_end:
            return

        self.transaction_end = True
        with g.core.fast_debug.trace_enabled(False):
            await sync_to_async(self.transaction.__exit__)(None, None, None)

    def __repr__(self) -> str:
        return "AsyncDbMemento"


@dataclass
class Django(ServerExtension):
    NAME = "Django"

    app_port: Optional[int] = field(init=False)
    orig_register_model: Optional[Callable[..., Any]] = field(init=False, default=None)

    handle_command_original: Any = field(init=False, default=None)
    get_response_original: Any = field(init=False, default=None)
    get_handler_original: Any = field(init=False, default=None)

    ALLOWED_IN_FREE = True

    def __post_init__(self) -> None:
        super().__post_init__()
        self.app_port = None

    def get_objects(self) -> List[Type[Object]]:
        return [Field]

    def on_start(self) -> None:
        super().on_start()
        if "runserver" in sys.argv:
            sys.argv.append("--noreload")

    def enable(self, module: types.ModuleType) -> None:
        if self.is_import(module, "django.core.management.commands.runserver"):
            self._watch_runserver()
            if not self.free:
                self._watch_server_starting()

    def disable(self) -> None:
        import django.core.management.commands.runserver

        django.core.management.commands.runserver.Command.handle = self.handle_command_original
        django.core.management.commands.runserver.Command.get_handler = self.get_handler_original
        django.core.handlers.base.BaseHandler.get_response = self.get_response_original

    def create_function_memento(self, name: str, is_async: bool) -> Optional["Memento"]:
        if self.free:
            return None

        if not os.environ.get("DJANGO_SETTINGS_MODULE"):
            return None

        if is_async:
            return None
        else:
            ret = DbMemento(name=name, extension=self)
            ret.create()

        return ret

    async def create_function_memento_async(self, name: str) -> Optional["AsyncMemento"]:
        if self.free:
            return None

        if not os.environ.get("DJANGO_SETTINGS_MODULE"):
            return None

        ret = AsyncDbMemento(name=name, extension=self)
        await ret.create()
        return ret

    def _watch_runserver(self) -> None:
        import django.core.management.commands.runserver

        self.handle_command_original = django.core.management.commands.runserver.Command.handle

        def patched(*args: Any, **options: Any) -> Any:
            with reloader_code():
                port = options.get("addrport")
                if not port:
                    port = django.core.management.commands.runserver.Command.default_port

                port = port.split(":")[-1]
                port = int(port)
                self.app_port = port

            return self.handle_command_original(*args, **options)

        monkey_patcher.patch(django.core.management.commands.runserver.Command, "handle", patched)

    def _watch_server_starting(self) -> None:
        import django.core.management.commands.runserver

        self.get_handler_original = django.core.management.commands.runserver.Command.get_handler

        def patched(*args: Any, **options: Any) -> Any:
            with reloader_code():
                assert self.app_port
                self.page_reloader = self._page_reloader_factory(self.app_port)
                if env.page_reload_on_start:
                    self.page_reloader.reload_with_delay(2.0)

            return self.get_handler_original(*args, **options)

        monkey_patcher.patch(django.core.management.commands.runserver.Command, "get_handler", patched)

    def _inject_reloader(self) -> None:
        super()._inject_reloader()

        import django.core.handlers.base

        self.get_response_original = django.core.handlers.base.BaseHandler.get_response

        def patched(d_self: Any, request: Any) -> Any:
            response = self.get_response_original(d_self, request)

            if not self.page_reloader:
                return response

            content_type = response.get("content-type")

            if not content_type or "text/html" not in content_type:
                return response

            content = response.content

            if isinstance(content, bytes):
                content = content.decode("utf-8")

            injected_content = self.page_reloader.inject_script(content)

            response.content = injected_content.encode("utf-8")
            response["content-length"] = str(len(response.content)).encode("ascii")
            return response

        django.core.handlers.base.BaseHandler.get_response = patched  # type: ignore

    def before_reload(self, path: Path) -> None:
        super().before_reload(path)

        from django.apps.registry import Apps

        self.orig_register_model = Apps.register_model

        def mock(*args: Any, **kwargs: Any) -> Any:
            pass

        Apps.register_model = mock

    def after_reload(self, path: Path, actions: List[Action]) -> None:
        super().after_reload(path, actions)

        if not self.orig_register_model:
            return

        from django.apps.registry import Apps

        Apps.register_model = self.orig_register_model

    def on_other_modify(self, path: Path) -> None:
        try:
            from django.template.autoreload import get_template_directories, reset_loaders

            for template_dir in get_template_directories():
                if template_dir in path.parents:
                    reset_loaders()
                    break
        except Exception:
            pass

        super().on_other_modify(path)

