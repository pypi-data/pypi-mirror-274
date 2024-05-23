from contextlib import contextmanager
from pathlib import Path
import types
from typing import TYPE_CHECKING, Any, Dict, Generator, List, Tuple, Type, cast
import types

from reloadium.corium.ll1lll11l11ll11lIl1l1 import ll1lll11l11ll11lIl1l1
from reloadium.corium.ll1l1l1ll1111lllIl1l1.l111ll1ll111llllIl1l1 import ll1lll1lll1l1l1lIl1l1
from reloadium.lib.environ import env
from reloadium.corium.lllll11ll11ll1l1Il1l1 import l1l11llll11llll1Il1l1
from reloadium.lib.ll1lll1l11l11111Il1l1.lll1ll1ll111l1llIl1l1 import lll1ll1111111ll1Il1l1
from reloadium.corium.ll111ll1l11l1ll1Il1l1 import ll1l111ll1111l1lIl1l1, l1llllllll1l1l1lIl1l1, llll1l1ll1l111llIl1l1, ll1ll1l1111ll1l1Il1l1
from reloadium.corium.lll1ll1lll1l1l1lIl1l1 import llll11ll11l1l11lIl1l1
from dataclasses import dataclass, field

__RELOADIUM__ = True

ll1ll11l111ll1llIl1l1 = ll1lll11l11ll11lIl1l1.l1l1l1l1l1111l1lIl1l1(__name__)


@dataclass(**ll1ll1l1111ll1l1Il1l1)
class llllll11lll1l11lIl1l1(llll1l1ll1l111llIl1l1):
    l111lllll1111l11Il1l1 = 'FlaskApp'

    @classmethod
    def llll11111lllllllIl1l1(lll1l1ll1ll1l1l1Il1l1, llll11111l1l1lllIl1l1: llll11ll11l1l11lIl1l1.l1ll1l1l1lll1111Il1l1, ll11l11l111l111lIl1l1: Any, lll1l111111111llIl1l1: ll1l111ll1111l1lIl1l1) -> bool:
        import flask

        if (isinstance(ll11l11l111l111lIl1l1, flask.Flask)):
            return True

        return False

    def l1ll11111lll1111Il1l1(lll1111l111l1111Il1l1) -> bool:
        return True

    @classmethod
    def l1l1l1l1l111ll11Il1l1(lll1l1ll1ll1l1l1Il1l1) -> int:
        return (super().l1l1l1l1l111ll11Il1l1() + 10)


@dataclass(**ll1ll1l1111ll1l1Il1l1)
class ll1111ll111l111lIl1l1(llll1l1ll1l111llIl1l1):
    l111lllll1111l11Il1l1 = 'Request'

    @classmethod
    def llll11111lllllllIl1l1(lll1l1ll1ll1l1l1Il1l1, llll11111l1l1lllIl1l1: llll11ll11l1l11lIl1l1.l1ll1l1l1lll1111Il1l1, ll11l11l111l111lIl1l1: Any, lll1l111111111llIl1l1: ll1l111ll1111l1lIl1l1) -> bool:
        if (repr(ll11l11l111l111lIl1l1) == '<LocalProxy unbound>'):
            return True

        return False

    def l1ll11111lll1111Il1l1(lll1111l111l1111Il1l1) -> bool:
        return True

    @classmethod
    def l1l1l1l1l111ll11Il1l1(lll1l1ll1ll1l1l1Il1l1) -> int:

        return int(10000000000.0)


@dataclass
class l11l11ll1l11ll1lIl1l1(lll1ll1111111ll1Il1l1):
    ll11111lll1l1111Il1l1 = 'Flask'

    @contextmanager
    def l1llll111ll1llllIl1l1(lll1111l111l1111Il1l1) -> Generator[None, None, None]:




        from flask import Flask as FlaskLib 

        def l11l11llll11l11lIl1l1(*l1l1111l11l111llIl1l1: Any, **llll11ll11l1l111Il1l1: Any) -> Any:
            def l111l11ll11ll1llIl1l1(l11ll11l111111llIl1l1: Any) -> Any:
                return l11ll11l111111llIl1l1

            return l111l11ll11ll1llIl1l1

        l11l1111l11l11l1Il1l1 = FlaskLib.route
        FlaskLib.route = l11l11llll11l11lIl1l1  # type: ignore

        try:
            yield 
        finally:
            FlaskLib.route = l11l1111l11l11l1Il1l1  # type: ignore

    def l11ll1l1111ll1llIl1l1(lll1111l111l1111Il1l1) -> List[Type[l1llllllll1l1l1lIl1l1]]:
        return [llllll11lll1l11lIl1l1, ll1111ll111l111lIl1l1]

    def l1ll11lll111ll11Il1l1(lll1111l111l1111Il1l1, l11l1l1l1llll1llIl1l1: types.ModuleType) -> None:
        if (lll1111l111l1111Il1l1.l1l1l1l111111lllIl1l1(l11l1l1l1llll1llIl1l1, 'flask.app')):
            lll1111l111l1111Il1l1.lll1111111l1l1l1Il1l1()
            lll1111l111l1111Il1l1.lll111ll11llll11Il1l1()
            lll1111l111l1111Il1l1.lllllll1llllll1lIl1l1()

        if (lll1111l111l1111Il1l1.l1l1l1l111111lllIl1l1(l11l1l1l1llll1llIl1l1, 'flask.cli')):
            lll1111l111l1111Il1l1.llll11lll1l111l1Il1l1()


    def l1l1l1111lll11llIl1l1(hostname: Any, port: Any, application: Any, use_reloader: Any = False, use_debugger: Any = False, use_evalex: Any = True, extra_files: Any = None, exclude_patterns: Any = None, reloader_interval: Any = 1, reloader_type: Any = 'auto', threaded: Any = False, processes: Any = 1, request_handler: Any = None, static_files: Any = None, passthrough_errors: Any = False, ssl_context: Any = None) -> Any:
        from typing import cast
        __rw_plugin__ = cast('Flask', globals().get('__rw_plugin__'))

        __rw_plugin__.l11lll111lll11llIl1l1 = __rw_plugin__.ll11lll11l11lll1Il1l1(port)  # type: ignore
        if (__rw_globals__['env'].page_reload_on_start):  # type: ignore
            __rw_plugin__.l11lll111lll11llIl1l1.ll1111l1111l11l1Il1l1(1.0)  # type: ignore
        __rw_orig__(hostname, port, application, use_reloader, use_debugger, use_evalex, extra_files, exclude_patterns, reloader_interval, reloader_type, threaded, processes, request_handler, static_files, passthrough_errors, ssl_context)  # type: ignore













    def lll1111111l1l1l1Il1l1(lll1111l111l1111Il1l1) -> None:
        try:
            import werkzeug.serving
            import flask.cli
        except ImportError:
            return 

        ll1lll1lll1l1l1lIl1l1.lllllll111l11111Il1l1(werkzeug.serving.run_simple, lll1111l111l1111Il1l1.l1l1l1111lll11llIl1l1, ll11ll1l11111ll1Il1l1={'__rw_plugin__': lll1111l111l1111Il1l1})


    def lllllll1llllll1lIl1l1(lll1111l111l1111Il1l1) -> None:
        try:
            import flask
        except ImportError:
            return 

        llll11ll11l11l1lIl1l1 = flask.app.Flask.__init__

        def l1l1ll1l1ll11111Il1l1(l11ll111l1lllll1Il1l1: Any, *l1l1111l11l111llIl1l1: Any, **llll11ll11l1l111Il1l1: Any) -> Any:
            llll11ll11l11l1lIl1l1(l11ll111l1lllll1Il1l1, *l1l1111l11l111llIl1l1, **llll11ll11l1l111Il1l1)
            with l1l11llll11llll1Il1l1():
                l11ll111l1lllll1Il1l1.config['TEMPLATES_AUTO_RELOAD'] = True

        ll1lll1lll1l1l1lIl1l1.l111ll1ll111llllIl1l1(flask.app.Flask, '__init__', l1l1ll1l1ll11111Il1l1)

    def lll111ll11llll11Il1l1(lll1111l111l1111Il1l1) -> None:
        try:
            import waitress  # type: ignore
        except ImportError:
            return 

        llll11ll11l11l1lIl1l1 = waitress.serve



        def l1l1ll1l1ll11111Il1l1(*l1l1111l11l111llIl1l1: Any, **llll11ll11l1l111Il1l1: Any) -> Any:
            with l1l11llll11llll1Il1l1():
                lll11llll1llllllIl1l1 = llll11ll11l1l111Il1l1.get('port')
                if ( not lll11llll1llllllIl1l1):
                    lll11llll1llllllIl1l1 = int(l1l1111l11l111llIl1l1[1])

                lll11llll1llllllIl1l1 = int(lll11llll1llllllIl1l1)

                lll1111l111l1111Il1l1.l11lll111lll11llIl1l1 = lll1111l111l1111Il1l1.ll11lll11l11lll1Il1l1(lll11llll1llllllIl1l1)
                if (env.page_reload_on_start):
                    lll1111l111l1111Il1l1.l11lll111lll11llIl1l1.ll1111l1111l11l1Il1l1(1.0)

            llll11ll11l11l1lIl1l1(*l1l1111l11l111llIl1l1, **llll11ll11l1l111Il1l1)

        ll1lll1lll1l1l1lIl1l1.l111ll1ll111llllIl1l1(waitress, 'serve', l1l1ll1l1ll11111Il1l1)

    def llll11lll1l111l1Il1l1(lll1111l111l1111Il1l1) -> None:
        try:
            from flask import cli
        except ImportError:
            return 

        l1l1ll11lll11ll1Il1l1 = Path(cli.__file__).read_text(encoding='utf-8')
        l1l1ll11lll11ll1Il1l1 = l1l1ll11lll11ll1Il1l1.replace('.tb_next', '.tb_next.tb_next')

        exec(l1l1ll11lll11ll1Il1l1, cli.__dict__)

    def llllllll1lll1l1lIl1l1(lll1111l111l1111Il1l1) -> None:
        super().llllllll1lll1l1lIl1l1()
        import flask.app

        llll11ll11l11l1lIl1l1 = flask.app.Flask.dispatch_request

        def l1l1ll1l1ll11111Il1l1(*l1l1111l11l111llIl1l1: Any, **llll11ll11l1l111Il1l1: Any) -> Any:
            l1111ll1l11l1ll1Il1l1 = llll11ll11l11l1lIl1l1(*l1l1111l11l111llIl1l1, **llll11ll11l1l111Il1l1)

            try:
                if ( not lll1111l111l1111Il1l1.l11lll111lll11llIl1l1):
                    return l1111ll1l11l1ll1Il1l1

                if (isinstance(l1111ll1l11l1ll1Il1l1, str)):
                    l1ll11ll11l1111lIl1l1 = lll1111l111l1111Il1l1.l11lll111lll11llIl1l1.lll1l1ll11111111Il1l1(l1111ll1l11l1ll1Il1l1)
                    return l1ll11ll11l1111lIl1l1
                elif ((isinstance(l1111ll1l11l1ll1Il1l1, flask.app.Response) and 'text/html' in l1111ll1l11l1ll1Il1l1.content_type)):
                    l1111ll1l11l1ll1Il1l1.data = lll1111l111l1111Il1l1.l11lll111lll11llIl1l1.lll1l1ll11111111Il1l1(l1111ll1l11l1ll1Il1l1.data.decode('utf-8')).encode('utf-8')
                else:
                    return l1111ll1l11l1ll1Il1l1
            except :
                return l1111ll1l11l1ll1Il1l1

        flask.app.Flask.dispatch_request = l1l1ll1l1ll11111Il1l1  # type: ignore
