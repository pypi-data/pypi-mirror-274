from reloadium.corium.vendored import logging
from pathlib import Path
from threading import Thread
import time
from typing import TYPE_CHECKING, List, Optional

from reloadium.corium import l1lll1ll11llll1lIl1l1
from reloadium.corium.l1lll1ll11llll1lIl1l1.lll1l1llll1ll111Il1l1 import l1lll1ll1lll1lllIl1l1
from reloadium.lib.ll11l11111lll11lIl1l1.ll11lll1ll11l11lIl1l1 import l11111lll11111llIl1l1
from reloadium.corium.lll1llll1l1l1lllIl1l1 import ll11l1l11111l1llIl1l1
from reloadium.corium.llll11l11ll1l11lIl1l1 import l11l1ll11ll1l1l1Il1l1
from reloadium.corium.ll11lll1ll11111lIl1l1 import l1ll1l111l11l111Il1l1
from reloadium.corium.ll111ll111ll111lIl1l1 import ll111ll111ll111lIl1l1
from dataclasses import dataclass, field

if (TYPE_CHECKING):
    from reloadium.vendored.websocket_server import WebsocketServer


__RELOADIUM__ = True

__all__ = ['l1l11l11ll1ll111Il1l1']



l1ll1111ll1l1111Il1l1 = '\n<!--{info}-->\n<script type="text/javascript">\n   // <![CDATA[  <-- For SVG support\n     function refreshCSS() {\n        var sheets = [].slice.call(document.getElementsByTagName("link"));\n        var head = document.getElementsByTagName("head")[0];\n        for (var i = 0; i < sheets.length; ++i) {\n           var elem = sheets[i];\n           var parent = elem.parentElement || head;\n           parent.removeChild(elem);\n           var rel = elem.rel;\n           if (elem.href && typeof rel != "string" || rel.length === 0 || rel.toLowerCase() === "stylesheet") {\n              var url = elem.href.replace(/(&|\\?)_cacheOverride=\\d+/, \'\');\n              elem.href = url + (url.indexOf(\'?\') >= 0 ? \'&\' : \'?\') + \'_cacheOverride=\' + (new Date().valueOf());\n           }\n           parent.appendChild(elem);\n        }\n     }\n     let protocol = window.location.protocol === \'http:\' ? \'ws://\' : \'wss://\';\n     let address = protocol + "{address}:{port}";\n     let socket = undefined;\n     let lost_connection = false;\n\n     function connect() {\n        socket = new WebSocket(address);\n         socket.onmessage = function (msg) {\n            if (msg.data === \'reload\') window.location.href = window.location.href;\n            else if (msg.data === \'refreshcss\') refreshCSS();\n         };\n     }\n\n     function checkConnection() {\n        if ( socket.readyState === socket.CLOSED ) {\n            lost_connection = true;\n            connect();\n        }\n     }\n\n     connect();\n     setInterval(checkConnection, 500)\n\n   // ]]>\n</script>\n'














































@dataclass
class l1l11l11ll1ll111Il1l1:
    l1l11l111ll1lll1Il1l1: str
    l11ll1l1111111llIl1l1: int
    llll11lll1ll11llIl1l1: l11l1ll11ll1l1l1Il1l1

    lll111lll11ll11lIl1l1: Optional["WebsocketServer"] = field(init=False, default=None)
    ll1lll1ll1lllll1Il1l1: str = field(init=False, default='')

    lll1ll1lll1l1l1lIl1l1 = 'Reloadium page reloader'

    def ll11l11111l1l11lIl1l1(lll1l11111lll1l1Il1l1) -> None:
        from reloadium.vendored.websocket_server import WebsocketServer

        lll1l11111lll1l1Il1l1.llll11lll1ll11llIl1l1.lll1ll1lll1l1l1lIl1l1(''.join(['Starting reload websocket server on port ', '{:{}}'.format(lll1l11111lll1l1Il1l1.l11ll1l1111111llIl1l1, '')]))

        lll1l11111lll1l1Il1l1.lll111lll11ll11lIl1l1 = WebsocketServer(host=lll1l11111lll1l1Il1l1.l1l11l111ll1lll1Il1l1, port=lll1l11111lll1l1Il1l1.l11ll1l1111111llIl1l1)
        lll1l11111lll1l1Il1l1.lll111lll11ll11lIl1l1.run_forever(threaded=True)

        lll1l11111lll1l1Il1l1.ll1lll1ll1lllll1Il1l1 = l1ll1111ll1l1111Il1l1

        lll1l11111lll1l1Il1l1.ll1lll1ll1lllll1Il1l1 = lll1l11111lll1l1Il1l1.ll1lll1ll1lllll1Il1l1.replace('{info}', str(lll1l11111lll1l1Il1l1.lll1ll1lll1l1l1lIl1l1))
        lll1l11111lll1l1Il1l1.ll1lll1ll1lllll1Il1l1 = lll1l11111lll1l1Il1l1.ll1lll1ll1lllll1Il1l1.replace('{port}', str(lll1l11111lll1l1Il1l1.l11ll1l1111111llIl1l1))
        lll1l11111lll1l1Il1l1.ll1lll1ll1lllll1Il1l1 = lll1l11111lll1l1Il1l1.ll1lll1ll1lllll1Il1l1.replace('{address}', lll1l11111lll1l1Il1l1.l1l11l111ll1lll1Il1l1)

    def l111llll1111ll11Il1l1(lll1l11111lll1l1Il1l1, l1l1ll1ll11ll1l1Il1l1: str) -> str:
        l111lll111l1l111Il1l1 = l1l1ll1ll11ll1l1Il1l1.find('<head>')
        if (l111lll111l1l111Il1l1 ==  - 1):
            l111lll111l1l111Il1l1 = 0
        lllll1l111111111Il1l1 = ((l1l1ll1ll11ll1l1Il1l1[:l111lll111l1l111Il1l1] + lll1l11111lll1l1Il1l1.ll1lll1ll1lllll1Il1l1) + l1l1ll1ll11ll1l1Il1l1[l111lll111l1l111Il1l1:])
        return lllll1l111111111Il1l1

    def l1l1ll1ll1lll111Il1l1(lll1l11111lll1l1Il1l1) -> None:
        try:
            lll1l11111lll1l1Il1l1.ll11l11111l1l11lIl1l1()
        except Exception as ll1lll1lll11l111Il1l1:
            lll1l11111lll1l1Il1l1.llll11lll1ll11llIl1l1.ll11llll11lll1llIl1l1('Could not start page reload server', l1l1ll1llll111llIl1l1=True)

    def llllll11ll11ll11Il1l1(lll1l11111lll1l1Il1l1) -> None:
        if ( not lll1l11111lll1l1Il1l1.lll111lll11ll11lIl1l1):
            return 

        lll1l11111lll1l1Il1l1.llll11lll1ll11llIl1l1.lll1ll1lll1l1l1lIl1l1('Reloading page')
        lll1l11111lll1l1Il1l1.lll111lll11ll11lIl1l1.send_message_to_all('reload')
        ll111ll111ll111lIl1l1.ll1111l111ll111lIl1l1()

    def l1l1l1l111l1l11lIl1l1(lll1l11111lll1l1Il1l1) -> None:
        if ( not lll1l11111lll1l1Il1l1.lll111lll11ll11lIl1l1):
            return 

        lll1l11111lll1l1Il1l1.llll11lll1ll11llIl1l1.lll1ll1lll1l1l1lIl1l1('Stopping reload server')
        lll1l11111lll1l1Il1l1.lll111lll11ll11lIl1l1.shutdown()

    def l11l11ll11111111Il1l1(lll1l11111lll1l1Il1l1, l1l1111l11l1l1llIl1l1: float) -> None:
        def l1lll1l11l11l1llIl1l1() -> None:
            time.sleep(l1l1111l11l1l1llIl1l1)
            lll1l11111lll1l1Il1l1.llllll11ll11ll11Il1l1()

        l1lll1ll1lll1lllIl1l1(l1111ll1ll1llll1Il1l1=l1lll1l11l11l1llIl1l1, l1l111lll1lll111Il1l1='page-reloader').start()


@dataclass
class l1l11lll1l1l11llIl1l1(l11111lll11111llIl1l1):
    l1ll1111ll1l1111Il1l1: Optional[l1l11l11ll1ll111Il1l1] = field(init=False, default=None)

    llllllllll11l11lIl1l1 = '127.0.0.1'
    l1l111l1l1lll1llIl1l1 = 4512

    def l11lll1111l1lll1Il1l1(lll1l11111lll1l1Il1l1) -> None:
        ll11l1l11111l1llIl1l1.ll11l1lll11l1l1lIl1l1.l1l1lll111llllllIl1l1.l1111111l1l1l1llIl1l1('html')

    def lll11111lllll1llIl1l1(lll1l11111lll1l1Il1l1, lll11llll1111111Il1l1: Path, l111lll111111l1lIl1l1: List[l1ll1l111l11l111Il1l1]) -> None:
        if ( not lll1l11111lll1l1Il1l1.l1ll1111ll1l1111Il1l1):
            return 

        from reloadium.corium.l11l111lll1l1111Il1l1.lll1lllll11111l1Il1l1 import l11l1l1111l1llllIl1l1

        if ( not any((isinstance(l11ll11lll1ll11lIl1l1, l11l1l1111l1llllIl1l1) for l11ll11lll1ll11lIl1l1 in l111lll111111l1lIl1l1))):
            if (lll1l11111lll1l1Il1l1.l1ll1111ll1l1111Il1l1):
                lll1l11111lll1l1Il1l1.l1ll1111ll1l1111Il1l1.llllll11ll11ll11Il1l1()

    def lll111llllll11l1Il1l1(lll1l11111lll1l1Il1l1, lll11llll1111111Il1l1: Path) -> None:
        if ( not lll1l11111lll1l1Il1l1.l1ll1111ll1l1111Il1l1):
            return 
        lll1l11111lll1l1Il1l1.l1ll1111ll1l1111Il1l1.llllll11ll11ll11Il1l1()

    def l1l1ll11ll111111Il1l1(lll1l11111lll1l1Il1l1, l11ll1l1111111llIl1l1: int) -> l1l11l11ll1ll111Il1l1:
        while True:
            ll1ll1l1ll111111Il1l1 = (l11ll1l1111111llIl1l1 + lll1l11111lll1l1Il1l1.l1l111l1l1lll1llIl1l1)
            try:
                lllll1l111111111Il1l1 = l1l11l11ll1ll111Il1l1(l1l11l111ll1lll1Il1l1=lll1l11111lll1l1Il1l1.llllllllll11l11lIl1l1, l11ll1l1111111llIl1l1=ll1ll1l1ll111111Il1l1, llll11lll1ll11llIl1l1=lll1l11111lll1l1Il1l1.l1l1111111lll11lIl1l1)
                lllll1l111111111Il1l1.l1l1ll1ll1lll111Il1l1()
                lll1l11111lll1l1Il1l1.ll1l1l11llll1111Il1l1()
                break
            except OSError:
                lll1l11111lll1l1Il1l1.l1l1111111lll11lIl1l1.lll1ll1lll1l1l1lIl1l1(''.join(["Couldn't create page reloader on ", '{:{}}'.format(ll1ll1l1ll111111Il1l1, ''), ' port']))
                lll1l11111lll1l1Il1l1.l1l111l1l1lll1llIl1l1 += 1

        return lllll1l111111111Il1l1

    def ll1l1l11llll1111Il1l1(lll1l11111lll1l1Il1l1) -> None:
        lll1l11111lll1l1Il1l1.l1l1111111lll11lIl1l1.lll1ll1lll1l1l1lIl1l1('Injecting page reloader')

    def llllll11l1l1ll1lIl1l1(lll1l11111lll1l1Il1l1) -> None:
        super().llllll11l1l1ll1lIl1l1()

        if (lll1l11111lll1l1Il1l1.l1ll1111ll1l1111Il1l1):
            lll1l11111lll1l1Il1l1.l1ll1111ll1l1111Il1l1.l1l1l1l111l1l11lIl1l1()
