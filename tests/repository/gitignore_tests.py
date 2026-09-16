import shutil
import subprocess
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
GITIGNORE = REPOSITORY_ROOT / ".gitignore"

IGNORED_PATHS = (
    ".env",
    ".env.local",
    "credentials.json",
    "secrets.production.json",
    "private.key",
    "certificate.pem",
    "identity.p12",
    "config.local.toml",
    "settings.local.yaml",
    "vault/memory.md",
    "vaults/personal/note.md",
    "memory/current.md",
    "memories/current.md",
    "notes/private.md",
    "attachments/photo.jpg",
    "imports/exported_notes.md",
    "exports/vault.zip",
    "backups/vault.backup",
    "local_data/state.json",
    "runtime/session.tmp",
    "indexes/search.sqlite",
    "embeddings/vectors.db",
    "vector_store/index.db-wal",
    "cache/result.json",
    "logs/mnemosyne.log",
    ".obsidian/workspace.json",
    ".obsidian/plugins/example/data.json",
    ".trash/deleted_memory.md",
    "@eaDir/metadata",
    "#recycle/deleted_memory.md",
    "#snapshot/version/memory.md",
    ".SynologyWorkingDirectory/temporary_file",
)

TRACKABLE_PATHS = (
    ".env.example",
    "README.md",
    "docs/security_boundary.md",
    "examples/config.example.toml",
    "src/mnemosyne/config.py",
    "tests/fixtures/README.md",
    ".obsidian/app.json",
)


def _is_ignored(repository: Path, path: str) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", "--quiet", "--no-index", "--", path],
        cwd=repository,
        check=False,
    )
    assert result.returncode in {0, 1}, f"git check-ignore failed for {path}"
    return result.returncode == 0


class GitignoreTests:
    def test_private_and_machine_local_paths_are_ignored(self, tmp_path: Path) -> None:
        shutil.copyfile(GITIGNORE, tmp_path / ".gitignore")
        subprocess.run(["git", "init", "--quiet"], cwd=tmp_path, check=True)

        unexpected = [path for path in IGNORED_PATHS if not _is_ignored(tmp_path, path)]

        assert unexpected == []

    def test_safe_examples_and_source_files_remain_trackable(self, tmp_path: Path) -> None:
        shutil.copyfile(GITIGNORE, tmp_path / ".gitignore")
        subprocess.run(["git", "init", "--quiet"], cwd=tmp_path, check=True)

        unexpected = [path for path in TRACKABLE_PATHS if _is_ignored(tmp_path, path)]

        assert unexpected == []
