import mnemosyne


class MnemosynePackageTests:
    def test_package_exposes_version(self) -> None:
        assert mnemosyne.__version__ == "0.0.0"
