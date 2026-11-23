#!/usr/bin/env python3
"""Pack this repository into a WorkBuddy "My Experts" importable zip.

Output: dist/zaimae-v2-handbook-v<version>.zip, where <version> is read from
.codebuddy-plugin/plugin.json. The zip contains a single top-level folder named
after the plugin (from plugin.json), so that extracting it yields a folder that
can be dropped straight into the plugin directory.

Repository-only files (LICENSE, .gitignore, .gitattributes, tools/, dist/,
.git/) are excluded. Filenames are written with the UTF-8 flag set, because the
reference files under skills/zaimae-handbook/references/ have Chinese names.
"""

from __future__ import annotations

import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_JSON = ROOT / ".codebuddy-plugin" / "plugin.json"
DIST = ROOT / "dist"

EXCLUDE_DIRS = {
    ".git",
    ".github",
    ".idea",
    ".vscode",
    "__pycache__",
    "dist",
    "tools",
}
EXCLUDE_FILES = {
    ".DS_Store",
    ".gitattributes",
    ".gitignore",
    "LICENSE",
}


def plugin_info() -> tuple[str, str]:
    data = json.loads(PLUGIN_JSON.read_text(encoding="utf-8"))
    name = data["name"]
    version = data.get("version", "0.0.0")
    return name, version


def collect_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        rel = path.relative_to(ROOT)
        if any(part in EXCLUDE_DIRS for part in rel.parts):
            continue
        if not path.is_file():
            continue
        if path.name in EXCLUDE_FILES or path.name.endswith((".pyc", ".pyo")):
            continue
        files.append(rel)
    return sorted(files, key=lambda p: p.as_posix())


def main() -> None:
    name, version = plugin_info()
    files = collect_files()
    if not files:
        raise SystemExit("No files to pack - is this the repository root?")

    DIST.mkdir(exist_ok=True)
    out = DIST / f"{name}-v{version}.zip"

    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for rel in files:
            arcname = f"{name}/{rel.as_posix()}"
            info = zipfile.ZipInfo(arcname, date_time=(2026, 1, 1, 0, 0, 0))
            info.flag_bits |= 0x800  # UTF-8 filename
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, (ROOT / rel).read_bytes())

    size_kb = out.stat().st_size / 1024
    print(f"Wrote {out.relative_to(ROOT)} ({len(files)} files, {size_kb:.0f} KB)")


if __name__ == "__main__":
    main()
