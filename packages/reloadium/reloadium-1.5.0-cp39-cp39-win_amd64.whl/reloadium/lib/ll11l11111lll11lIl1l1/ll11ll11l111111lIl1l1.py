from contextlib import contextmanager
from pathlib import Path
import types
from typing import TYPE_CHECKING, Any, Dict, Generator, List, Tuple, Type, cast
import types

from reloadium.corium.llll11l11ll1l11lIl1l1 import llll11l11ll1l11lIl1l1
from reloadium.corium.l1lll1ll11llll1lIl1l1.ll11ll1lll1llll1Il1l1 import llll1llllll1ll11Il1l1
from reloadium.lib.environ import env
from reloadium.corium.l1l111l1l11lll1lIl1l1 import l1l1111ll1llllllIl1l1
from reloadium.lib.ll11l11111lll11lIl1l1.lll11ll11ll11111Il1l1 import l1l11lll1l1l11llIl1l1
from reloadium.corium.ll11lll1ll11111lIl1l1 import lll11l11lll1111lIl1l1, l1ll11lll1ll111lIl1l1, lll11ll1ll111111Il1l1, ll111llll11l1l11Il1l1
from reloadium.corium.l111l1l11ll1l1l1Il1l1 import llll1l11lllll1l1Il1l1
from dataclasses import dataclass, field

__RELOADIUM__ = True

llll11lll1ll11llIl1l1 = llll11l11ll1l11lIl1l1.ll11l11111l11111Il1l1(__name__)


@dataclass(**ll111llll11l1l11Il1l1)
class lllll11lll1l111lIl1l1(lll11ll1ll111111Il1l1):
    l1111l111ll1ll1lIl1l1 = 'FlaskApp'

    @classmethod
    def l1l11ll1ll1lll11Il1l1(l11lllll1l111ll1Il1l1, ll1l11111l11ll11Il1l1: llll1l11lllll1l1Il1l1.l11llll11ll1lll1Il1l1, ll1lll1l11l1lll1Il1l1: Any, lll11ll11lll111lIl1l1: lll11l11lll1111lIl1l1) -> bool:
        import flask

        if (isinstance(ll1lll1l11l1lll1Il1l1, flask.Flask)):
            return True

        return False

    def ll1l111ll111l11lIl1l1(lll1l11111lll1l1Il1l1) -> bool:
        return True

    @classmethod
    def llllllll11111ll1Il1l1(l11lllll1l111ll1Il1l1) -> int:
        return (super().llllllll11111ll1Il1l1() + 10)


@dataclass(**ll111llll11l1l11Il1l1)
class l11l11l1ll1l1111Il1l1(lll11ll1ll111111Il1l1):
    l1111l111ll1ll1lIl1l1 = 'Request'

    @classmethod
    def l1l11ll1ll1lll11Il1l1(l11lllll1l111ll1Il1l1, ll1l11111l11ll11Il1l1: llll1l11lllll1l1Il1l1.l11llll11ll1lll1Il1l1, ll1lll1l11l1lll1Il1l1: Any, lll11ll11lll111lIl1l1: lll11l11lll1111lIl1l1) -> bool:
        if (repr(ll1lll1l11l1lll1Il1l1) == '<LocalProxy unbound>'):
            return True

        return False

    def ll1l111ll111l11lIl1l1(lll1l11111lll1l1Il1l1) -> bool:
        return True

    @classmethod
    def llllllll11111ll1Il1l1(l11lllll1l111ll1Il1l1) -> int:

        return int(10000000000.0)


@dataclass
class lll1lll111l11ll1Il1l1(l1l11lll1l1l11llIl1l1):
    ll1l1l1l11l111llIl1l1 = 'Flask'

    @contextmanager
    def l111l1ll1l1l111lIl1l1(lll1l11111lll1l1Il1l1) -> Generator[None, None, None]:




        from flask import Flask as FlaskLib 

        def lllll1ll1l111l1lIl1l1(*l11111l111l11lllIl1l1: Any, **lll1l11l1l1ll111Il1l1: Any) -> Any:
            def l11l1ll1ll11111lIl1l1(lll11111lll111llIl1l1: Any) -> Any:
                return lll11111lll111llIl1l1

            return l11l1ll1ll11111lIl1l1

        l1l11l11llllllllIl1l1 = FlaskLib.route
        FlaskLib.route = lllll1ll1l111l1lIl1l1  # type: ignore

        try:
            yield 
        finally:
            FlaskLib.route = l1l11l11llllllllIl1l1  # type: ignore

    def ll11l1l1llllll11Il1l1(lll1l11111lll1l1Il1l1) -> List[Type[l1ll11lll1ll111lIl1l1]]:
        return [lllll11lll1l111lIl1l1, l11l11l1ll1l1111Il1l1]

    def l1lll11l111l1lllIl1l1(lll1l11111lll1l1Il1l1, l111111l11111l1lIl1l1: types.ModuleType) -> None:
        if (lll1l11111lll1l1Il1l1.lll111ll1llllll1Il1l1(l111111l11111l1lIl1l1, 'flask.app')):
            lll1l11111lll1l1Il1l1.l11ll1111ll1ll1lIl1l1()
            lll1l11111lll1l1Il1l1.l11ll11l11lllll1Il1l1()
            lll1l11111lll1l1Il1l1.ll1ll11l1lll1l11Il1l1()

        if (lll1l11111lll1l1Il1l1.lll111ll1llllll1Il1l1(l111111l11111l1lIl1l1, 'flask.cli')):
            lll1l11111lll1l1Il1l1.ll1l111l1ll11l1lIl1l1()


    def ll1ll1ll1lll11llIl1l1(hostname: Any, port: Any, application: Any, use_reloader: Any = False, use_debugger: Any = False, use_evalex: Any = True, extra_files: Any = None, exclude_patterns: Any = None, reloader_interval: Any = 1, reloader_type: Any = 'auto', threaded: Any = False, processes: Any = 1, request_handler: Any = None, static_files: Any = None, passthrough_errors: Any = False, ssl_context: Any = None) -> Any:
        from typing import cast
        __rw_plugin__ = cast('Flask', globals().get('__rw_plugin__'))

        __rw_plugin__.l1ll1111ll1l1111Il1l1 = __rw_plugin__.l1l1ll11ll111111Il1l1(port)  # type: ignore
        if (__rw_globals__['env'].page_reload_on_start):  # type: ignore
            __rw_plugin__.l1ll1111ll1l1111Il1l1.l11l11ll11111111Il1l1(1.0)  # type: ignore
        __rw_orig__(hostname, port, application, use_reloader, use_debugger, use_evalex, extra_files, exclude_patterns, reloader_interval, reloader_type, threaded, processes, request_handler, static_files, passthrough_errors, ssl_context)  # type: ignore













    def l11ll1111ll1ll1lIl1l1(lll1l11111lll1l1Il1l1) -> None:
        try:
            import werkzeug.serving
            import flask.cli
        except ImportError:
            return 

        llll1llllll1ll11Il1l1.l111l1l11l1111l1Il1l1(werkzeug.serving.run_simple, lll1l11111lll1l1Il1l1.ll1ll1ll1lll11llIl1l1, lll1lll1l11111llIl1l1={'__rw_plugin__': lll1l11111lll1l1Il1l1})


    def ll1ll11l1lll1l11Il1l1(lll1l11111lll1l1Il1l1) -> None:
        try:
            import flask
        except ImportError:
            return 

        lll11l1ll1111ll1Il1l1 = flask.app.Flask.__init__

        def lll11ll1l11l1111Il1l1(ll1ll11111l11111Il1l1: Any, *l11111l111l11lllIl1l1: Any, **lll1l11l1l1ll111Il1l1: Any) -> Any:
            lll11l1ll1111ll1Il1l1(ll1ll11111l11111Il1l1, *l11111l111l11lllIl1l1, **lll1l11l1l1ll111Il1l1)
            with l1l1111ll1llllllIl1l1():
                ll1ll11111l11111Il1l1.config['TEMPLATES_AUTO_RELOAD'] = True

        llll1llllll1ll11Il1l1.ll11ll1lll1llll1Il1l1(flask.app.Flask, '__init__', lll11ll1l11l1111Il1l1)

    def l11ll11l11lllll1Il1l1(lll1l11111lll1l1Il1l1) -> None:
        try:
            import waitress  # type: ignore
        except ImportError:
            return 

        lll11l1ll1111ll1Il1l1 = waitress.serve



        def lll11ll1l11l1111Il1l1(*l11111l111l11lllIl1l1: Any, **lll1l11l1l1ll111Il1l1: Any) -> Any:
            with l1l1111ll1llllllIl1l1():
                l11ll1l1111111llIl1l1 = lll1l11l1l1ll111Il1l1.get('port')
                if ( not l11ll1l1111111llIl1l1):
                    l11ll1l1111111llIl1l1 = int(l11111l111l11lllIl1l1[1])

                l11ll1l1111111llIl1l1 = int(l11ll1l1111111llIl1l1)

                lll1l11111lll1l1Il1l1.l1ll1111ll1l1111Il1l1 = lll1l11111lll1l1Il1l1.l1l1ll11ll111111Il1l1(l11ll1l1111111llIl1l1)
                if (env.page_reload_on_start):
                    lll1l11111lll1l1Il1l1.l1ll1111ll1l1111Il1l1.l11l11ll11111111Il1l1(1.0)

            lll11l1ll1111ll1Il1l1(*l11111l111l11lllIl1l1, **lll1l11l1l1ll111Il1l1)

        llll1llllll1ll11Il1l1.ll11ll1lll1llll1Il1l1(waitress, 'serve', lll11ll1l11l1111Il1l1)

    def ll1l111l1ll11l1lIl1l1(lll1l11111lll1l1Il1l1) -> None:
        try:
            from flask import cli
        except ImportError:
            return 

        ll1l1l1ll1l111l1Il1l1 = Path(cli.__file__).read_text(encoding='utf-8')
        ll1l1l1ll1l111l1Il1l1 = ll1l1l1ll1l111l1Il1l1.replace('.tb_next', '.tb_next.tb_next')

        exec(ll1l1l1ll1l111l1Il1l1, cli.__dict__)

    def ll1l1l11llll1111Il1l1(lll1l11111lll1l1Il1l1) -> None:
        super().ll1l1l11llll1111Il1l1()
        import flask.app

        lll11l1ll1111ll1Il1l1 = flask.app.Flask.dispatch_request

        def lll11ll1l11l1111Il1l1(*l11111l111l11lllIl1l1: Any, **lll1l11l1l1ll111Il1l1: Any) -> Any:
            l11l1l1lll1lll1lIl1l1 = lll11l1ll1111ll1Il1l1(*l11111l111l11lllIl1l1, **lll1l11l1l1ll111Il1l1)

            try:
                if ( not lll1l11111lll1l1Il1l1.l1ll1111ll1l1111Il1l1):
                    return l11l1l1lll1lll1lIl1l1

                if (isinstance(l11l1l1lll1lll1lIl1l1, str)):
                    lllll1l111111111Il1l1 = lll1l11111lll1l1Il1l1.l1ll1111ll1l1111Il1l1.l111llll1111ll11Il1l1(l11l1l1lll1lll1lIl1l1)
                    return lllll1l111111111Il1l1
                elif ((isinstance(l11l1l1lll1lll1lIl1l1, flask.app.Response) and 'text/html' in l11l1l1lll1lll1lIl1l1.content_type)):
                    l11l1l1lll1lll1lIl1l1.data = lll1l11111lll1l1Il1l1.l1ll1111ll1l1111Il1l1.l111llll1111ll11Il1l1(l11l1l1lll1lll1lIl1l1.data.decode('utf-8')).encode('utf-8')
                else:
                    return l11l1l1lll1lll1lIl1l1
            except :
                return l11l1l1lll1lll1lIl1l1

        flask.app.Flask.dispatch_request = lll11ll1l11l1111Il1l1  # type: ignore
