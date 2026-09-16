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


def run_history_scanner(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCANNER), "--root", str(root), "--history"],
        check=False,
        capture_output=True,
        text=True,
    )


def make_root(tmp_path: Path) -> Path:
    root = tmp_path / "repository"
    (root / "security").mkdir(parents=True)
    shutil.copy(CONFIG, root / "security" / CONFIG.name)
    return root


def commit_all(root: Path, message: str) -> None:
    subprocess.run(["git", "add", "--all"], cwd=root, check=True)
    subprocess.run(["git", "commit", "--quiet", "-m", message], cwd=root, check=True)


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

    def test_clean_history_passes(self, tmp_path: Path) -> None:
        root = make_root(tmp_path)
        subprocess.run(["git", "init", "--quiet"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Synthetic Test"], cwd=root, check=True)
        subprocess.run(
            ["git", "config", "user.email", "synthetic@example.invalid"],
            cwd=root,
            check=True,
        )
        example = root / ".env.example"
        field = "MNEMOSYNE" + "_VAULT_PATH"
        example.write_text(f"{field}=<private-vault-path>\n", encoding="utf-8")
        commit_all(root, "safe synthetic history")

        result = run_history_scanner(root)

        assert result.returncode == 0

    def test_removed_private_value_still_fails_history_scan(self, tmp_path: Path) -> None:
        root = make_root(tmp_path)
        subprocess.run(["git", "init", "--quiet"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Synthetic Test"], cwd=root, check=True)
        subprocess.run(
            ["git", "config", "user.email", "synthetic@example.invalid"],
            cwd=root,
            check=True,
        )
        config = root / "config.txt"
        field = "MNEMOSYNE" + "_VAULT_PATH"
        synthetic_value = "/" + "volume9/history-canary"
        config.write_text(f"{field}={synthetic_value}\n", encoding="utf-8")
        commit_all(root, "add synthetic history canary")
        config.write_text(f"{field}=<private-vault-path>\n", encoding="utf-8")
        commit_all(root, "remove synthetic history canary")

        assert run_scanner(root).returncode == 0

        result = run_history_scanner(root)

        assert result.returncode == 1
        assert "private-config-value" in result.stderr
        assert synthetic_value not in result.stderr
