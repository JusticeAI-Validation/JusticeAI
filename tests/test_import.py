"""Test basic imports."""


def test_import_justiceai() -> None:
    """Test that justiceai can be imported."""
    import justiceai

    assert justiceai.__version__ == "0.1.0"
    assert justiceai.__author__ == "Gustavo Haase"


def test_module_has_license() -> None:
    """Test that license is defined."""
    import justiceai

    assert justiceai.__license__ == "MIT"
