import mnemosyne


def test_package_exposes_version() -> None:
    assert mnemosyne.__version__ == "0.0.0"
