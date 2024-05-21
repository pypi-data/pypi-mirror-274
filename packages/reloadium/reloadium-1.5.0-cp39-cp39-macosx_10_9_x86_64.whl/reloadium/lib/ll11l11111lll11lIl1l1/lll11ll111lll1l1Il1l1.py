import sys

from reloadium.corium.l1lll1ll11llll1lIl1l1.lll1111l1lllll1lIl1l1 import ll11111l1l1ll111Il1l1

__RELOADIUM__ = True

ll11111l1l1ll111Il1l1()


try:
    import _pytest.assertion.rewrite
except ImportError:
    class ll1ll11ll11lllllIl1l1:
        pass

    _pytest = lambda :None  # type: ignore
    sys.modules['_pytest'] = _pytest

    _pytest.assertion = lambda :None  # type: ignore
    sys.modules['_pytest.assertion'] = _pytest.assertion

    _pytest.assertion.rewrite = lambda :None  # type: ignore
    _pytest.assertion.rewrite.AssertionRewritingHook = ll1ll11ll11lllllIl1l1  # type: ignore
    sys.modules['_pytest.assertion.rewrite'] = _pytest.assertion.rewrite
