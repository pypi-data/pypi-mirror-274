from reloadium.corium.vendored import logging
from pathlib import Path
from threading import Thread
import time
from typing import TYPE_CHECKING, List, Optional

from reloadium.corium import ll1l1l1ll1111lllIl1l1
from reloadium.corium.ll1l1l1ll1111lllIl1l1.lll1l1ll1l1l1ll1Il1l1 import l1111l11l1111111Il1l1
from reloadium.lib.ll1lll1l11l11111Il1l1.l11l1lll1l11l111Il1l1 import llll1l1l11llll11Il1l1
from reloadium.corium.l11lll1ll11l1111Il1l1 import llll11l1l1111lllIl1l1
from reloadium.corium.ll1lll11l11ll11lIl1l1 import l111l1l1llllll1lIl1l1
from reloadium.corium.ll111ll1l11l1ll1Il1l1 import l111111l111l1ll1Il1l1
from reloadium.corium.lllllll1lllll1l1Il1l1 import lllllll1lllll1l1Il1l1
from dataclasses import dataclass, field

if (TYPE_CHECKING):
    from reloadium.vendored.websocket_server import WebsocketServer


__RELOADIUM__ = True

__all__ = ['l111111lll11l1llIl1l1']



l11lll111lll11llIl1l1 = '\n<!--{info}-->\n<script type="text/javascript">\n   // <![CDATA[  <-- For SVG support\n     function refreshCSS() {\n        var sheets = [].slice.call(document.getElementsByTagName("link"));\n        var head = document.getElementsByTagName("head")[0];\n        for (var i = 0; i < sheets.length; ++i) {\n           var elem = sheets[i];\n           var parent = elem.parentElement || head;\n           parent.removeChild(elem);\n           var rel = elem.rel;\n           if (elem.href && typeof rel != "string" || rel.length === 0 || rel.toLowerCase() === "stylesheet") {\n              var url = elem.href.replace(/(&|\\?)_cacheOverride=\\d+/, \'\');\n              elem.href = url + (url.indexOf(\'?\') >= 0 ? \'&\' : \'?\') + \'_cacheOverride=\' + (new Date().valueOf());\n           }\n           parent.appendChild(elem);\n        }\n     }\n     let protocol = window.location.protocol === \'http:\' ? \'ws://\' : \'wss://\';\n     let address = protocol + "{address}:{port}";\n     let socket = undefined;\n     let lost_connection = false;\n\n     function connect() {\n        socket = new WebSocket(address);\n         socket.onmessage = function (msg) {\n            if (msg.data === \'reload\') window.location.href = window.location.href;\n            else if (msg.data === \'refreshcss\') refreshCSS();\n         };\n     }\n\n     function checkConnection() {\n        if ( socket.readyState === socket.CLOSED ) {\n            lost_connection = true;\n            connect();\n        }\n     }\n\n     connect();\n     setInterval(checkConnection, 500)\n\n   // ]]>\n</script>\n'














































@dataclass
class l111111lll11l1llIl1l1:
    l111l111lll1l111Il1l1: str
    lll11llll1llllllIl1l1: int
    ll1ll11l111ll1llIl1l1: l111l1l1llllll1lIl1l1

    l1ll1l111llll11lIl1l1: Optional["WebsocketServer"] = field(init=False, default=None)
    l11l1l1l11lll1llIl1l1: str = field(init=False, default='')

    l11l11111llll1llIl1l1 = 'Reloadium page reloader'

    def llll1llll1ll11llIl1l1(lll1111l111l1111Il1l1) -> None:
        from reloadium.vendored.websocket_server import WebsocketServer

        lll1111l111l1111Il1l1.ll1ll11l111ll1llIl1l1.l11l11111llll1llIl1l1(''.join(['Starting reload websocket server on port ', '{:{}}'.format(lll1111l111l1111Il1l1.lll11llll1llllllIl1l1, '')]))

        lll1111l111l1111Il1l1.l1ll1l111llll11lIl1l1 = WebsocketServer(host=lll1111l111l1111Il1l1.l111l111lll1l111Il1l1, port=lll1111l111l1111Il1l1.lll11llll1llllllIl1l1)
        lll1111l111l1111Il1l1.l1ll1l111llll11lIl1l1.run_forever(threaded=True)

        lll1111l111l1111Il1l1.l11l1l1l11lll1llIl1l1 = l11lll111lll11llIl1l1

        lll1111l111l1111Il1l1.l11l1l1l11lll1llIl1l1 = lll1111l111l1111Il1l1.l11l1l1l11lll1llIl1l1.replace('{info}', str(lll1111l111l1111Il1l1.l11l11111llll1llIl1l1))
        lll1111l111l1111Il1l1.l11l1l1l11lll1llIl1l1 = lll1111l111l1111Il1l1.l11l1l1l11lll1llIl1l1.replace('{port}', str(lll1111l111l1111Il1l1.lll11llll1llllllIl1l1))
        lll1111l111l1111Il1l1.l11l1l1l11lll1llIl1l1 = lll1111l111l1111Il1l1.l11l1l1l11lll1llIl1l1.replace('{address}', lll1111l111l1111Il1l1.l111l111lll1l111Il1l1)

    def lll1l1ll11111111Il1l1(lll1111l111l1111Il1l1, l1l11111111l11llIl1l1: str) -> str:
        l11l1l1l1l11ll1lIl1l1 = l1l11111111l11llIl1l1.find('<head>')
        if (l11l1l1l1l11ll1lIl1l1 ==  - 1):
            l11l1l1l1l11ll1lIl1l1 = 0
        l1ll11ll11l1111lIl1l1 = ((l1l11111111l11llIl1l1[:l11l1l1l1l11ll1lIl1l1] + lll1111l111l1111Il1l1.l11l1l1l11lll1llIl1l1) + l1l11111111l11llIl1l1[l11l1l1l1l11ll1lIl1l1:])
        return l1ll11ll11l1111lIl1l1

    def l11ll111l1l1l111Il1l1(lll1111l111l1111Il1l1) -> None:
        try:
            lll1111l111l1111Il1l1.llll1llll1ll11llIl1l1()
        except Exception as lll111ll1l1l1ll1Il1l1:
            lll1111l111l1111Il1l1.ll1ll11l111ll1llIl1l1.l1l11l1lll1ll11lIl1l1('Could not start page reload server', llllllll1llll1l1Il1l1=True)

    def l111111l1ll111l1Il1l1(lll1111l111l1111Il1l1) -> None:
        if ( not lll1111l111l1111Il1l1.l1ll1l111llll11lIl1l1):
            return 

        lll1111l111l1111Il1l1.ll1ll11l111ll1llIl1l1.l11l11111llll1llIl1l1('Reloading page')
        lll1111l111l1111Il1l1.l1ll1l111llll11lIl1l1.send_message_to_all('reload')
        lllllll1lllll1l1Il1l1.l1111l1lll11l1llIl1l1()

    def l1l1l1ll11111lllIl1l1(lll1111l111l1111Il1l1) -> None:
        if ( not lll1111l111l1111Il1l1.l1ll1l111llll11lIl1l1):
            return 

        lll1111l111l1111Il1l1.ll1ll11l111ll1llIl1l1.l11l11111llll1llIl1l1('Stopping reload server')
        lll1111l111l1111Il1l1.l1ll1l111llll11lIl1l1.shutdown()

    def ll1111l1111l11l1Il1l1(lll1111l111l1111Il1l1, l1llllll1ll1l111Il1l1: float) -> None:
        def lllll111lll111l1Il1l1() -> None:
            time.sleep(l1llllll1ll1l111Il1l1)
            lll1111l111l1111Il1l1.l111111l1ll111l1Il1l1()

        l1111l11l1111111Il1l1(lll1l1l1l11l1l1lIl1l1=lllll111lll111l1Il1l1, ll11lll111lll1l1Il1l1='page-reloader').start()


@dataclass
class lll1ll1111111ll1Il1l1(llll1l1l11llll11Il1l1):
    l11lll111lll11llIl1l1: Optional[l111111lll11l1llIl1l1] = field(init=False, default=None)

    ll111lll11l1lll1Il1l1 = '127.0.0.1'
    l111l1111ll11l11Il1l1 = 4512

    def llllll1ll1ll1lllIl1l1(lll1111l111l1111Il1l1) -> None:
        llll11l1l1111lllIl1l1.l1l1lll11ll11l11Il1l1.l1ll11l11ll11l11Il1l1.ll1l1l111l1lll11Il1l1('html')

    def ll11l1lllll111l1Il1l1(lll1111l111l1111Il1l1, lllll11l1l1ll1llIl1l1: Path, ll1l1l1llll1ll11Il1l1: List[l111111l111l1ll1Il1l1]) -> None:
        if ( not lll1111l111l1111Il1l1.l11lll111lll11llIl1l1):
            return 

        from reloadium.corium.l1ll1l1llll1l11lIl1l1.l1l11l11ll11ll11Il1l1 import l11l11lllllll1llIl1l1

        if ( not any((isinstance(l1lll111111l1l11Il1l1, l11l11lllllll1llIl1l1) for l1lll111111l1l11Il1l1 in ll1l1l1llll1ll11Il1l1))):
            if (lll1111l111l1111Il1l1.l11lll111lll11llIl1l1):
                lll1111l111l1111Il1l1.l11lll111lll11llIl1l1.l111111l1ll111l1Il1l1()

    def ll1lll1l1l1lll11Il1l1(lll1111l111l1111Il1l1, lllll11l1l1ll1llIl1l1: Path) -> None:
        if ( not lll1111l111l1111Il1l1.l11lll111lll11llIl1l1):
            return 
        lll1111l111l1111Il1l1.l11lll111lll11llIl1l1.l111111l1ll111l1Il1l1()

    def ll11lll11l11lll1Il1l1(lll1111l111l1111Il1l1, lll11llll1llllllIl1l1: int) -> l111111lll11l1llIl1l1:
        while True:
            ll1llllll1ll11l1Il1l1 = (lll11llll1llllllIl1l1 + lll1111l111l1111Il1l1.l111l1111ll11l11Il1l1)
            try:
                l1ll11ll11l1111lIl1l1 = l111111lll11l1llIl1l1(l111l111lll1l111Il1l1=lll1111l111l1111Il1l1.ll111lll11l1lll1Il1l1, lll11llll1llllllIl1l1=ll1llllll1ll11l1Il1l1, ll1ll11l111ll1llIl1l1=lll1111l111l1111Il1l1.ll11111l1l11l1llIl1l1)
                l1ll11ll11l1111lIl1l1.l11ll111l1l1l111Il1l1()
                lll1111l111l1111Il1l1.llllllll1lll1l1lIl1l1()
                break
            except OSError:
                lll1111l111l1111Il1l1.ll11111l1l11l1llIl1l1.l11l11111llll1llIl1l1(''.join(["Couldn't create page reloader on ", '{:{}}'.format(ll1llllll1ll11l1Il1l1, ''), ' port']))
                lll1111l111l1111Il1l1.l111l1111ll11l11Il1l1 += 1

        return l1ll11ll11l1111lIl1l1

    def llllllll1lll1l1lIl1l1(lll1111l111l1111Il1l1) -> None:
        lll1111l111l1111Il1l1.ll11111l1l11l1llIl1l1.l11l11111llll1llIl1l1('Injecting page reloader')

    def l11lll1l11l1111lIl1l1(lll1111l111l1111Il1l1) -> None:
        super().l11lll1l11l1111lIl1l1()

        if (lll1111l111l1111Il1l1.l11lll111lll11llIl1l1):
            lll1111l111l1111Il1l1.l11lll111lll11llIl1l1.l1l1l1ll11111lllIl1l1()
