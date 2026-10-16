#!/usr/bin/env python3
"""Build deterministic public release archives, using only validated bytes."""
import hashlib
import json
import os
import tempfile
import zipfile
from pathlib import Path

from validate import ValidationError, require, validate


def digest(data):
    return hashlib.sha256(data).hexdigest()


def archive(path, files):
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_STORED) as output:
        for name, data in sorted(files.items()):
            entry = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            entry.create_system, entry.external_attr = 3, 0o100644 << 16
            output.writestr(entry, data)


def build(root):
    root = Path(root).resolve()
    catalog, files = validate(root)
    version = catalog["version"]
    library = f"portfolio-mcp-skills-v{version}.zip"
    archives = [library] + [f"skills/{s['name']}.zip" for s in catalog["skills"]]
    expected = set(archives) | {"SHA256SUMS", "release-manifest.json"}
    dist = root / "dist"
    require(not dist.is_symlink(), "dist cannot be a symlink")
    if dist.exists():
        for path in dist.rglob("*"):
            rel = path.relative_to(dist).as_posix()
            require(not path.is_symlink(), f"dist symlink: {rel}")
            require(rel == "skills" and path.is_dir() or rel in expected and path.is_file(), f"unexpected dist entry: {rel}")
    with tempfile.TemporaryDirectory(prefix="portfolio-mcp-skills-build-") as temporary:
        stage = Path(temporary)
        (stage / "skills").mkdir()
        archive(stage / library, {f"portfolio-mcp-skills/{p}": data for p, data in files.items()})
        for skill in catalog["skills"]:
            source = f"{skill['path']}/SKILL.md"
            archive(stage / f"skills/{skill['name']}.zip", {f"{skill['name']}/SKILL.md": files[source]})
        manifest = {"version": version, "files": [{"path": p, "sha256": digest(data), "size": len(data)} for p, data in files.items()],
                    "archives": [{"path": p, "sha256": digest((stage / p).read_bytes())} for p in sorted(archives)]}
        (stage / "release-manifest.json").write_bytes((json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8"))
        sums = "".join(f"{digest((stage / p).read_bytes())}  {p}\n" for p in sorted(expected - {"SHA256SUMS"}))
        (stage / "SHA256SUMS").write_bytes(sums.encode("utf-8"))
        (dist / "skills").mkdir(parents=True, exist_ok=True)
        for name in sorted(expected):
            os.replace(stage / name, dist / name)
    return dist


if __name__ == "__main__":
    try:
        destination = build(Path(__file__).resolve().parents[1])
        print(f"Built library, {len(list((destination / 'skills').glob('*.zip')))} skill ZIPs, release manifest and checksums in {destination.name}/")
    except (OSError, ValidationError) as error:
        raise SystemExit(str(error))
