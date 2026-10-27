#!/usr/bin/env python3
"""Validate public skill sources. Importing this module performs no I/O."""
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

TOOLS = frozenset("open_fillfolio get_portfolio_summary list_portfolios list_holdings "
                  "list_cash_and_liabilities list_activity get_asset get_spending_summary "
                  "list_bank_transactions list_budgets".split())
GEMINI_TOOLS = TOOLS - {"open_fillfolio"}
GEMINI_PROFILE = {'endpoint': 'https://free-mcp.fillfolio.com/mcp', 'resource': 'https://free-mcp.fillfolio.com/mcp', 'transport': 'streamable-http', 'oauth': {'enabled': True, 'clientId': 'fillfolio-free-gemini-cli', 'scopes': ['portfolio:read'], 'redirectUri': 'http://localhost:7777/oauth/callback'}, 'tools': ['get_asset', 'get_portfolio_summary', 'get_spending_summary', 'list_activity', 'list_bank_transactions', 'list_budgets', 'list_cash_and_liabilities', 'list_holdings', 'list_portfolios']}
GEMINI_DESCRIPTION = 'Read-only Fillfolio portfolios, spending and budgets for Free and paid accounts.'
ROOT_FILES = frozenset("README.md LICENSE CONTRIBUTING.md catalog.json requirements-dev.txt gemini-extension.json GEMINI.md".split())
LOCAL = frozenset("AGENTS.md .gitignore .git .codex dist .DS_Store __pycache__ .pytest_cache".split())
NAME = re.compile(r"fillfolio-[a-z0-9]+(?:-[a-z0-9]+)*\Z")
TOOL = re.compile(r"\b(?:get|list|open|create|update|delete|set|refresh|connect|search)_[a-z][a-z0-9_]*\b")
SENSITIVE = re.compile(
    r"/" + r"Users/|/" + r"home/|[A-Z]:\\Users\\|Projects " + r"Brain|fillfolio" + r"_github|"
    r"-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----|"
    r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|"
    r"(?:sk|rk)_(?:live|test)_[A-Za-z0-9]{16,}|AKIA[A-Z0-9]{16}|"
    r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,})\b|"
    r"\bBearer\s+[A-Za-z0-9._~-]{20,}", re.IGNORECASE)
PERSONAL = re.compile(r"(?i)\b(?:customer|reviewer)[_-]?(?:id|email|name)"
                      r"[\"']?\s*[:=]\s*[\"']?([\w@.+-]{4,})")
EMAIL = re.compile(r"\b[\w.+-]+@([\w.-]+\.[A-Za-z]{2,})\b")
LINK = re.compile(r"!?\[[^\]\n]*\]\(\s*(<[^>]+>|[^\s)]+)|^\s*\[[^\]\n]+\]:\s*(<[^>]+>|\S+)", re.M)


class ValidationError(ValueError):
    """A source or export boundary is invalid."""


def require(condition, message):
    if not condition:
        raise ValidationError(message)


def unique_mapping(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate mapping key")
        result[key] = value
    return result


class FrontmatterLoader(yaml.SafeLoader):
    pass


def yaml_mapping(loader, node):
    return unique_mapping(loader.construct_pairs(node))


FrontmatterLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, yaml_mapping)


def public_files(root):
    """Return the explicit export set; local operational files are never exported."""
    files = {}
    def visit(directory):
        for path in sorted(directory.iterdir()):
            rel = path.relative_to(root)
            if rel.parts[0] in LOCAL or path.name in {"__pycache__", ".DS_Store"} or path.suffix == ".pyc":
                continue
            require(not path.is_symlink(), f"symlink is forbidden: {rel}")
            if path.is_dir():
                require(rel.parts[0] in {"docs", "skills", "scripts", "tests", ".github"}, f"unexpected directory: {rel}")
                visit(path)
                continue
            allowed = str(rel) in ROOT_FILES
            allowed |= rel.parts[0] == "docs" and path.suffix == ".md"
            allowed |= rel.parts[0] == "skills" and len(rel.parts) == 3 and path.name == "SKILL.md"
            allowed |= rel.parts[0] in {"scripts", "tests"} and path.suffix == ".py"
            allowed |= rel.parts[:2] == ("tests", "fixtures") and path.suffix in {".json", ".md", ".txt", ".yaml", ".yml"}
            allowed |= rel.parts[:2] == (".github", "workflows") and path.suffix in {".yaml", ".yml"}
            require(allowed and path.is_file(), f"unexpected public file: {rel}")
            files[rel.as_posix()] = path.read_bytes()
    visit(root)
    require(ROOT_FILES <= files.keys(), "missing required root files")
    return dict(sorted(files.items()))


def validate(root):
    """Return (catalog, validated bytes); never fetch links or inspect user state."""
    root = Path(root).resolve()
    files = public_files(root)
    try:
        catalog = json.loads(files["catalog.json"], object_pairs_hook=unique_mapping)
        require(isinstance(catalog, dict), "catalog must be an object")
        require(catalog.get("schemaVersion") == 1 and catalog.get("license") == "MIT", "invalid catalog schema/license")
        require(re.fullmatch(r"\d+\.\d+\.\d+", catalog.get("version", "")), "invalid release version")
        require(catalog.get("repository") == "https://github.com/fillfolio/portfolio-mcp-skills", "unexpected repository")
        extension = json.loads(files["gemini-extension.json"], object_pairs_hook=unique_mapping)
        require(catalog.get("mcpProfiles") == {"gemini-cli": GEMINI_PROFILE}, "Gemini profile differs from accepted configuration")
        expected_extension = {
            "name": "fillfolio", "version": catalog["version"], "description": GEMINI_DESCRIPTION,
            "contextFileName": "GEMINI.md",
            "mcpServers": {"fillfolio": {"httpUrl": GEMINI_PROFILE["endpoint"], "oauth": GEMINI_PROFILE["oauth"]}},
        }
        require(extension == expected_extension and type(extension["mcpServers"]["fillfolio"]["oauth"]["enabled"]) is bool,
                "Gemini manifest differs from the accepted OAuth configuration")
        require(bool(files["GEMINI.md"].strip()), "Gemini context cannot be empty")
        known = catalog.get("mcp", {}).get("tools", [])
        require(isinstance(known, list) and len(known) == len(TOOLS) and set(known) == TOOLS, "unknown or missing MCP tools")
        skills = catalog.get("skills", [])
        require(isinstance(skills, list) and bool(skills), "catalog must contain at least one skill")
        names, paths = set(), set()
        for skill in skills:
            name, path, tools = skill.get("name", ""), skill.get("path", ""), skill.get("tools", [])
            require(NAME.fullmatch(name) and len(name) <= 64 and name not in names, "invalid or duplicate skill name")
            require(path == f"skills/{name}" and path not in paths, "invalid or duplicate skill path")
            require(isinstance(tools, list) and len(tools) == len(set(tools)) and set(tools) <= TOOLS, f"invalid tools: {name}")
            require(skill.get("access") in {"authenticated-mcp", "public-http"}, f"invalid access: {name}")
            optional = skill.get("optionalTools", [])
            require(isinstance(optional, list) and len(optional) == len(set(optional)) and set(optional) <= set(tools) & {"open_fillfolio"}, f"invalid optional tools: {name}")
            if skill["access"] == "authenticated-mcp":
                require(set(tools) - set(optional) <= GEMINI_TOOLS, f"required tools unavailable in Gemini profile: {name}")
            names.add(name)
            paths.add(path)
            source = files.get(f"{path}/SKILL.md", b"").decode("utf-8")
            match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n(.+)", source, re.S)
            require(match, f"missing frontmatter/body: {name}")
            meta = yaml.load(match[1], Loader=FrontmatterLoader)
            require(isinstance(meta, dict) and set(meta) == {"name", "description", "license"}, f"frontmatter fields: {name}")
            require(meta["name"] == name and meta["license"] == "MIT", f"frontmatter name/license: {name}")
            require(isinstance(meta["description"], str) and 0 < len(meta["description"]) <= 200, f"description length: {name}")
            mentioned = set(TOOL.findall(match[2]))
            require(mentioned == set(tools), f"tool dependencies differ from instructions: {name}")
        actual = {p.rsplit("/", 1)[0] for p in files if p.startswith("skills/")}
        require(actual == paths, "catalog and skill folders differ")
        require(b"MIT License" in files["LICENSE"], "MIT license file required")
        for rel, data in files.items():
            source = data.decode("utf-8")
            require(not SENSITIVE.search(source), f"private path or credential literal: {rel}")
            require(all(m[1].lower() in {"example", "placeholder", "synthetic", "redacted"} for m in PERSONAL.finditer(source)), f"personal record literal: {rel}")
            require(all(m[1].lower() in {"example.com", "example.org", "example.net", "fillfolio.com"} for m in EMAIL.finditer(source)), f"personal email literal: {rel}")
            if not rel.endswith(".md"):
                continue
            for link in LINK.finditer(source):
                target = (link[1] or link[2]).strip("<>")
                url = urlsplit(target)
                if url.scheme or url.netloc:
                    require(url.scheme in {"http", "https", "mailto"}, f"unsupported link scheme: {rel}")
                    continue
                dest = (root / rel).parent / unquote(url.path) if url.path else root / rel
                resolved = dest.resolve()
                require(resolved.is_relative_to(root), f"link escapes repository: {rel}")
                local = resolved.relative_to(root).as_posix()
                require(local in files, f"missing or nonpublic link: {rel}: {target}")
                if rel.startswith("skills/"):
                    require(resolved.is_relative_to((root / rel).parent), f"skill depends on parent path: {rel}")
    except (KeyError, TypeError, AttributeError, UnicodeError, json.JSONDecodeError, yaml.YAMLError) as exc:
        raise ValidationError(f"malformed public source: {type(exc).__name__}") from exc
    return catalog, files


if __name__ == "__main__":
    try:
        result, exported = validate(Path(__file__).resolve().parents[1])
        print(f"Validated {len(result['skills'])} skills and {len(exported)} public files.")
    except (OSError, ValidationError) as error:
        raise SystemExit(str(error))
