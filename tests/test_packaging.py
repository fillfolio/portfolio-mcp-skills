"""Offline tests of export boundaries and reproducible installation packages."""
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from build import build, digest
from validate import TOOLS, ValidationError, validate


class PackagingTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        for name in ("README.md", "LICENSE", "CONTRIBUTING.md", "requirements-dev.txt", "GEMINI.md"):
            (self.root / name).write_text("MIT License\nSynthetic example.\n", encoding="utf-8")
        self.catalog = {"schemaVersion": 1, "version": "0.1.0", "license": "MIT", "repository": "https://github.com/fillfolio/portfolio-mcp-skills",
                        "mcp": {"tools": sorted(TOOLS)}, "skills": []}
        for index in range(15):
            name = f"fillfolio-test-{index:02d}"
            path = self.root / "skills" / name
            path.mkdir(parents=True)
            (path / "SKILL.md").write_text(f'---\nname: {name}\ndescription: "Synthetic workflow."\nlicense: MIT\n---\nCall `open_fillfolio`.\n', encoding="utf-8")
            self.catalog["skills"].append({"name": name, "path": f"skills/{name}", "tools": ["open_fillfolio"], "access": "authenticated-mcp"})
        self.manifest = {
            "name": "fillfolio", "version": "0.1.0", "contextFileName": "GEMINI.md",
            "mcpServers": {"fillfolio": {
                "httpUrl": "https://fillfolio.com/api/mcp",
                "oauth": {"enabled": True, "clientId": "fillfolio-gemini-cli",
                          "scopes": ["mcp:read"], "redirectUri": "http://localhost:7777/oauth/callback"},
            }},
        }
        self.save_manifest()
        self.save_catalog()

    def save_manifest(self):
        (self.root / "gemini-extension.json").write_text(json.dumps(self.manifest), encoding="utf-8")

    def save_catalog(self):
        (self.root / "catalog.json").write_text(json.dumps(self.catalog), encoding="utf-8")

    def test_reproducible_complete_and_standalone_archives(self):
        (self.root / "AGENTS.md").write_text("local instructions", encoding="utf-8")
        catalog, sources = validate(self.root)
        dist = build(self.root)
        first = {p.relative_to(dist): p.read_bytes() for p in dist.rglob("*") if p.is_file()}
        build(self.root)
        self.assertEqual(first, {p.relative_to(dist): p.read_bytes() for p in dist.rglob("*") if p.is_file()})
        with zipfile.ZipFile(dist / "portfolio-mcp-skills-v0.1.0.zip") as library:
            self.assertEqual(library.namelist(), [f"portfolio-mcp-skills/{p}" for p in sources])
            for entry in library.infolist():
                self.assertEqual(entry.date_time, (1980, 1, 1, 0, 0, 0))
                self.assertEqual(entry.external_attr >> 16, 0o100644)
                self.assertEqual(library.read(entry), sources[entry.filename.split("/", 1)[1]])
        for skill in catalog["skills"]:
            with zipfile.ZipFile(dist / "skills" / f"{skill['name']}.zip") as standalone:
                self.assertEqual(standalone.namelist(), [f"{skill['name']}/SKILL.md"])
        for line in (dist / "SHA256SUMS").read_text().splitlines():
            expected, name = line.split("  ")
            self.assertEqual(expected, digest((dist / name).read_bytes()))
        manifest = json.loads((dist / "release-manifest.json").read_text())
        self.assertEqual({p["path"]: p["sha256"] for p in manifest["files"]}, {p: digest(data) for p, data in sources.items()})

    def test_gemini_archive_is_self_contained_and_release_unambiguous(self):
        catalog, sources = validate(self.root)
        gemini = build(self.root) / "gemini"
        self.assertEqual({p.name for p in gemini.iterdir()}, {"fillfolio-v0.1.0.zip", "SHA256SUMS", "release-manifest.json"})
        self.assertEqual(len(list(gemini.glob("*.zip"))), 1)
        with zipfile.ZipFile(gemini / "fillfolio-v0.1.0.zip") as extension:
            self.assertEqual(extension.namelist(), list(sources))
            self.assertEqual(json.loads(extension.read("gemini-extension.json")), self.manifest)
            for entry in extension.infolist():
                self.assertEqual(extension.read(entry), sources[entry.filename])
                self.assertEqual(entry.date_time, (1980, 1, 1, 0, 0, 0))
                self.assertEqual(entry.external_attr >> 16, 0o100644)
            self.assertEqual(len([p for p in extension.namelist() if p.endswith("/SKILL.md")]), len(catalog["skills"]))
        for line in (gemini / "SHA256SUMS").read_text().splitlines():
            expected, name = line.split("  ")
            self.assertEqual(expected, digest((gemini / name).read_bytes()))
        metadata = json.loads((gemini / "release-manifest.json").read_text())
        self.assertEqual(metadata["releaseAssets"], ["fillfolio-v0.1.0.zip"])
        self.assertEqual(metadata["archives"], [{"path": "fillfolio-v0.1.0.zip", "sha256": digest((gemini / "fillfolio-v0.1.0.zip").read_bytes())}])
        self.assertEqual({p["path"]: p["sha256"] for p in metadata["files"]}, {p: digest(data) for p, data in sources.items()})

    def test_reject_gemini_auth_configuration_drift(self):
        original = json.dumps(self.manifest)
        for change in ("version", "client", "callback", "endpoint", "scope", "oauth-off", "oauth-number", "secret", "extra-server", "context"):
            self.manifest = json.loads(original)
            server = self.manifest["mcpServers"]["fillfolio"]
            if change == "version":
                self.manifest["version"] = "9.9.9"
            elif change == "client":
                server["oauth"]["clientId"] = "another-client"
            elif change == "callback":
                server["oauth"]["redirectUri"] = "http://localhost:9999/oauth/callback"
            elif change == "endpoint":
                server["httpUrl"] = "https://example.com/api/mcp"
            elif change == "scope":
                server["oauth"]["scopes"] = ["mcp:read", "mcp:write"]
            elif change == "oauth-off":
                server["oauth"]["enabled"] = False
            elif change == "oauth-number":
                server["oauth"]["enabled"] = 1
            elif change == "secret":
                server["oauth"]["clientSecret"] = "synthetic"
            elif change == "extra-server":
                self.manifest["mcpServers"]["unexpected"] = {"command": "synthetic"}
            else:
                self.manifest["contextFileName"] = "../outside.md"
            self.save_manifest()
            with self.subTest(change=change), self.assertRaises(ValidationError):
                build(self.root)
        self.manifest = json.loads(original)
        self.save_manifest()
        path = self.root / "gemini-extension.json"
        path.write_text(path.read_text().replace('"name": "fillfolio"', '"name": "fillfolio", "name": "fillfolio"'))
        with self.assertRaises(ValidationError):
            validate(self.root)
        self.save_manifest()
        (self.root / "GEMINI.md").write_text(" ")
        with self.assertRaises(ValidationError):
            validate(self.root)

    def test_reject_symlink_and_unknown_file(self):
        link = self.root / "docs"
        link.symlink_to(self.root / "skills", target_is_directory=True)
        with self.assertRaises(ValidationError):
            validate(self.root)
        link.unlink()
        (self.root / "account-export.csv").write_text("synthetic", encoding="utf-8")
        with self.assertRaises(ValidationError):
            build(self.root)
        self.assertFalse((self.root / "dist").exists())

    def test_reject_incomplete_dependencies_and_duplicate_metadata(self):
        source = self.root / self.catalog["skills"][0]["path"] / "SKILL.md"
        original = source.read_text()
        for addition in ("Call `get_asset`.\n", "[parent](../../README.md)\n", "[escape](../../../../outside.md)\n"):
            source.write_text(original + addition, encoding="utf-8")
            with self.assertRaises(ValidationError):
                validate(self.root)
        source.write_text(original.replace("license: MIT", "license: MIT\nlicense: MIT"), encoding="utf-8")
        with self.assertRaises(ValidationError):
            validate(self.root)

    def test_reject_sensitive_literals_without_rejecting_placeholder_words(self):
        readme = self.root / "README.md"
        for value in ("/" + "Users/person/private", "Bearer " + "a" * 32, "customer" + "_email: person@" + "invalid.test"):
            readme.write_text(value, encoding="utf-8")
            with self.assertRaises(ValidationError):
                validate(self.root)
        readme.write_text("Keep credentials, tokens and customer data private. customer_id: synthetic", encoding="utf-8")
        validate(self.root)

    def test_preserve_foreign_dist_content(self):
        dist = self.root / "dist"
        dist.mkdir()
        foreign = dist / "keep.txt"
        foreign.write_text("owned by someone else", encoding="utf-8")
        with self.assertRaises(ValidationError):
            build(self.root)
        self.assertEqual(foreign.read_text(), "owned by someone else")
        foreign.unlink()
        for directory in ("skills", "gemini"):
            link = dist / directory
            link.symlink_to(self.root / "skills", target_is_directory=True)
            with self.subTest(directory=directory), self.assertRaises(ValidationError):
                build(self.root)
            link.unlink()

    def test_catalog_identity_and_dependency_boundaries(self):
        original = json.dumps(self.catalog)
        for change in ("duplicate", "path", "unknown", "count"):
            self.catalog = json.loads(original)
            if change == "duplicate":
                self.catalog["skills"][1]["name"] = self.catalog["skills"][0]["name"]
            elif change == "path":
                self.catalog["skills"][0]["path"] = "../outside"
            elif change == "unknown":
                self.catalog["skills"][0]["tools"] = ["delete" + "_accounts"]
            else:
                self.catalog["skills"].pop()
            self.save_catalog()
            with self.subTest(change=change), self.assertRaises(ValidationError):
                validate(self.root)


if __name__ == "__main__":
    unittest.main()
