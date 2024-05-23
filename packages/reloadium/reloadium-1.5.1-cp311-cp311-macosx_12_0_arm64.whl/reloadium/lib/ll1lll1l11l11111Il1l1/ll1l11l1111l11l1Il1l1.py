import sys

from reloadium.corium.ll1l1l1ll1111lllIl1l1.l111l1lllllll1llIl1l1 import l1111l1lllll1l1lIl1l1

__RELOADIUM__ = True

l1111l1lllll1l1lIl1l1()


try:
    import _pytest.assertion.rewrite
except ImportError:
    class l1l1lllllll11l1lIl1l1:
        pass

    _pytest = lambda :None  # type: ignore
    sys.modules['_pytest'] = _pytest

    _pytest.assertion = lambda :None  # type: ignore
    sys.modules['_pytest.assertion'] = _pytest.assertion

    _pytest.assertion.rewrite = lambda :None  # type: ignore
    _pytest.assertion.rewrite.AssertionRewritingHook = l1l1lllllll11l1lIl1l1  # type: ignore
    sys.modules['_pytest.assertion.rewrite'] = _pytest.assertion.rewrite
