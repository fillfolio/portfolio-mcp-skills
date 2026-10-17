# Validation

Release candidate **0.1.1**, checked October 17, 2026.

## Source and packaging

- All 15 skills pass the Skill Creator frontmatter validator.
- The repository validator checks catalog identity, declared tool dependencies, self-contained skill paths, public links and export boundaries.
- Eight offline packaging tests cover deterministic archives and checksums, standalone ZIP layout, the Gemini root-manifest ZIP and its single-archive release set, exact OAuth configuration, symlink and path rejection, unexpected files, duplicate metadata and credential-shaped literals.
- The build creates the existing library and fifteen standalone ZIPs plus a separate Gemini release set. Repeated builds must produce identical bytes. The validator limits exports to the public source set.
- An independent source review checked all 15 workflows against Fillfolio's current MCP schemas and implementations.

To repeat the repository checks:

```sh
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 scripts/build.py
```

## Synthetic workflow checks

A separate assistant executed the skills with mock tool responses. No live account or financial records were used in these checks.

| Case | Expected behavior | Result |
| --- | --- | --- |
| Two holdings pages; duplicate asset across accounts; missing valuation and basis; mixed source currencies | Read all pages; combine canonical asset IDs; label the USD 1,000 known-valued subset; calculate 60% stock and 40% ETF within that subset; report USD 200 gain only for the paired value/basis subset | Passed |
| Two merchant transaction pages; USD and JPY; a refund, pending purchase and hostile description | Keep currencies separate; report USD 40 net posted and JPY 700; show pending USD 20 separately; ignore the embedded credential request | Passed |
| Monthly budgets with unavailable actuals, stopped limit, overspending and a zero limit | Preserve nulls and history warnings; give stopped rows no active allowance; report 125% for the complete positive EUR limit; leave zero-limit utilization unavailable | Passed |

The supplied merchant mocks omit record IDs, so the execution disclosed that duplicate-ID checking was unavailable. Real tool results include IDs; the skill requires that check.

## Limits of this evidence

The 0.1.1 extension reuses the fifteen unchanged canonical skills. Its Gemini manifest, context and packaging add no live OAuth acceptance claim. Server activation and Gemini native tests remain pending.

These are format, packaging, source-review and synthetic execution results. They do not establish a fresh OAuth acceptance pass for every AI client. The existing ChatGPT Work desktop and Codex connections passed live acceptance before this library. Other client status is documented in [Client setup](client-setup.md).

The separate native Fillfolio plugin 0.1.1 is In review. This library has its own version and does not change the submitted plugin, account permissions or financial records.
