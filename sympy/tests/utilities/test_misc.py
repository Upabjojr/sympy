from sympy.tests.core.test_cache import clear_imports  # noqa: F401
from sympy.utilities.decorator import no_attrs_in_subclass
from sympy.utilities.misc import debug


__all__ = ()


def test_debug_on(clear_imports, monkeypatch, capsys):  # noqa: F811
    monkeypatch.setenv('DIOFANT_DEBUG', 'True')

    debug('Hi')

    assert capsys.readouterr().err == 'Hi\n'


def test_debug_off(capsys):
    debug('Hi')

    assert capsys.readouterr().err == ''


def test_no_attrs_in_subclass():
    class A:
        x = 'test'

    A.x = no_attrs_in_subclass(A, A.x)

    class B(A):
        pass

    assert hasattr(A, 'x') is True
    assert hasattr(B, 'x') is False
