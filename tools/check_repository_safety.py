#!/usr/bin/env python3
"""Reject tracked files that cross Mnemosyne's public repository boundary."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

PROHIBITED_ROOTS = {
    "attachments",
    "backups",
    "cache",
    "embeddings",
    "exports",
    "imports",
    "indexes",
    "local_data",
    "logs",
    "memories",
    "memory",
    "notes",
    "runtime",
    "vault",
    "vaults",
    "vector_store",
}
PROHIBITED_SUFFIXES = {
    ".db",
    ".jks",
    ".key",
    ".keystore",
    ".log",
    ".p12",
    ".pem",
    ".pfx",
    ".sqlite",
    ".sqlite3",
    ".token",
}
PROHIBITED_NAMES = {
    "credentials.json",
    "secrets.json",
    "service-account.json",
}
IGNORED_FALLBACK_PARTS = {
    ".git",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
}
PRIVATE_ASSIGNMENT = re.compile(
    r"(?i)\b(MNEMOSYNE_VAULT_PATH|NAS_HOST|NAS_USERNAME|NAS_SHARE)\s*=\s*([^\s#]+)"
)
CONTENT_RULES = (
    (
        "private-ip-address",
        re.compile(
            r"(?<![0-9])(?:10(?:\.[0-9]{1,3}){3}|192\.168(?:\.[0-9]{1,3}){2}|"
            r"172\.(?:1[6-9]|2[0-9]|3[01])(?:\.[0-9]{1,3}){2})(?![0-9])"
        ),
    ),
    ("nas-volume-path", re.compile(r"(?i)(?<![A-Za-z0-9_])/volume[0-9]+/")),
    ("windows-user-path", re.compile(r"(?i)\b[A-Z]:\\Users\\[^\\\s]+")),
    ("unc-network-path", re.compile(r"\\\\[^\\\s]+\\[^\\\s]+")),
)


@dataclass(frozen=True)
class Finding:
    rule: str
    path: Path
    line: int | None = None

    def render(self, root: Path) -> str:
        try:
            display_path = self.path.relative_to(root)
        except ValueError:
            display_path = self.path
        location = f"{display_path}:{self.line}" if self.line else str(display_path)
        return f"{location}: blocked by {self.rule}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="repository root (default: current directory)",
    )
    parser.add_argument("paths", nargs="*", type=Path, help="specific files or directories to scan")
    return parser.parse_args()


def load_placeholders(root: Path) -> frozenset[str]:
    config_path = root / "security" / "repository_safety.toml"
    with config_path.open("rb") as config_file:
        config = tomllib.load(config_file)
    return frozenset(config["allowlist"]["placeholder_values"])


def tracked_files(root: Path) -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=root,
        check=False,
        capture_output=True,
    )
    if result.returncode == 0:
        return [root / Path(item.decode()) for item in result.stdout.split(b"\0") if item]
    return [
        path
        for path in root.rglob("*")
        if path.is_file()
        and not any(part in IGNORED_FALLBACK_PARTS for part in path.relative_to(root).parts)
        and not any(part.endswith(".egg-info") for part in path.relative_to(root).parts)
    ]


def requested_files(root: Path, paths: list[Path]) -> list[Path]:
    if not paths:
        return tracked_files(root)

    files: list[Path] = []
    for path in paths:
        resolved = path if path.is_absolute() else root / path
        if resolved.is_dir():
            files.extend(candidate for candidate in resolved.rglob("*") if candidate.is_file())
        elif resolved.is_file():
            files.append(resolved)
    return files


def path_finding(root: Path, path: Path) -> Finding | None:
    try:
        relative = path.relative_to(root)
    except ValueError:
        relative = path

    parts = tuple(part.casefold() for part in relative.parts)
    name = path.name.casefold()
    suffix = path.suffix.casefold()

    if parts and parts[0] in PROHIBITED_ROOTS:
        return Finding("prohibited-private-root", path)
    if ".obsidian" in parts or "@eadir" in parts:
        return Finding("private-application-metadata", path)
    if name == ".env" or (name.startswith(".env.") and name != ".env.example"):
        return Finding("private-environment-file", path)
    if name in PROHIBITED_NAMES or suffix in PROHIBITED_SUFFIXES:
        return Finding("sensitive-file-type", path)
    return None


def content_findings(path: Path, placeholders: frozenset[str]) -> list[Finding]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []

    findings: list[Finding] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        assignment = PRIVATE_ASSIGNMENT.search(line)
        if assignment and assignment.group(2) not in placeholders:
            findings.append(Finding("private-config-value", path, line_number))
        for rule, pattern in CONTENT_RULES:
            if pattern.search(line):
                findings.append(Finding(rule, path, line_number))
    return findings


def scan(root: Path, paths: list[Path]) -> list[Finding]:
    placeholders = load_placeholders(root)
    findings: list[Finding] = []
    for path in requested_files(root, paths):
        blocked_path = path_finding(root, path)
        if blocked_path:
            findings.append(blocked_path)
            continue
        findings.extend(content_findings(path, placeholders))
    return findings


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    findings = scan(root, args.paths)
    if findings:
        print("Repository safety check failed:", file=sys.stderr)
        for finding in findings:
            print(f"- {finding.render(root)}", file=sys.stderr)
        print("Detected values are intentionally redacted.", file=sys.stderr)
        return 1
    print("Repository safety check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
