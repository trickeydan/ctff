"""Test that the ctff imports as expected."""

import ctff


def test_module() -> None:
    """Test that the module behaves as expected."""
    assert ctff.__version__ is not None
