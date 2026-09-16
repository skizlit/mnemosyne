from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).parents[2]
SCANNER = REPOSITORY_ROOT / "tools" / "check_repository_safety.py"
CONFIG = REPOSITORY_ROOT / "security" / "repository_safety.toml"


def run_scanner(root: Path, *paths: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCANNER), "--root", str(root), *(str(path) for path in paths)],
        check=False,
        capture_output=True,
        text=True,
    )


def make_root(tmp_path: Path) -> Path:
    root = tmp_path / "repository"
    (root / "security").mkdir(parents=True)
    shutil.copy(CONFIG, root / "security" / CONFIG.name)
    return root


class CheckRepositorySafetyTests:
    def test_public_placeholder_passes(self, tmp_path: Path) -> None:
        root = make_root(tmp_path)
        example = root / ".env.example"
        field = "MNEMOSYNE" + "_VAULT_PATH"
        example.write_text(f"{field}=<private-vault-path>\n", encoding="utf-8")

        result = run_scanner(root, example)

        assert result.returncode == 0
        assert "passed" in result.stdout

    def test_prohibited_vault_path_fails(self, tmp_path: Path) -> None:
        root = make_root(tmp_path)
        private_note = root / "notes" / "private.md"
        private_note.parent.mkdir()
        private_note.write_text("synthetic note\n", encoding="utf-8")

        result = run_scanner(root, private_note)

        assert result.returncode == 1
        assert "prohibited-private-root" in result.stderr

    def test_synthetic_private_config_fails_without_echoing_value(self, tmp_path: Path) -> None:
        root = make_root(tmp_path)
        config = root / "config.txt"
        field = "MNEMOSYNE" + "_VAULT_PATH"
        synthetic_value = "/" + "volume9/synthetic-vault"
        config.write_text(f"{field}={synthetic_value}\n", encoding="utf-8")

        result = run_scanner(root, config)

        assert result.returncode == 1
        assert "private-config-value" in result.stderr
        assert "nas-volume-path" in result.stderr
        assert synthetic_value not in result.stderr
