# Validation

Release candidate **0.1.1**, updated October 26, 2026.

## Source and packaging

- All 15 skills pass the Skill Creator frontmatter validator.
- The repository validator checks catalog identity, declared tool dependencies, self-contained skill paths, public links and export boundaries.
- Nine offline packaging tests cover deterministic archives and checksums, standalone ZIP layout, the Gemini root-manifest ZIP and its single-archive release set, exact OAuth configuration, symlink and path rejection, unexpected files, duplicate metadata and credential-shaped literals.
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

The new Free/paid candidate retains fifteen canonical skill names and updates their content for host profiles. The earlier tests below describe the old paid-only candidate and do not establish current acceptance. We tested the official Gemini CLI 0.64.0 OAuth and MCP components with the synthetic reviewer on October 17, 2026. Ten-tool discovery, portfolio reads and pagination, the four spending/budget permission states, dashboard resource delivery and 662,704 milliseconds of continued access passed on the earlier service release. Those checks did not exercise Gemini model responses or dashboard rendering.

The package remains unreleased. We must complete acceptance on the final service release, including Gemini-only revocation and reconnection, permission restoration and the existing ChatGPT connection control. The earlier Work/Codex control is separate evidence.

These are format, packaging, source-review and synthetic execution results. They do not establish a fresh OAuth acceptance pass for every AI client. The existing ChatGPT Work desktop and Codex connections passed live acceptance before this library. Other client status is documented in [Client setup](client-setup.md).

The native Fillfolio plugin has a separate listing and release lifecycle. This library has its own version and does not change that plugin, account permissions or financial records.

## Free/paid profile acceptance

Current package and live results will be recorded after testing the new nine-tool profile with official CLI 0.65.0. Required checks cover Free limits, paid consent, optional permissions, downgrade, continued access and isolated revocation. Missing historical temporary artifacts are unavailable evidence, not regenerated PASS receipts. No new-profile release or gallery listing is claimed.

## October 26, 2026 plan-aware candidate

The revised Gemini profile uses `https://free-mcp.fillfolio.com/mcp`, public client `fillfolio-free-gemini-cli`, OAuth `portfolio:read`, and the exact localhost:7777 callback. Its nine read tools cover Free and eligible paid accounts. The fifteen canonical workflow names remain; their instructions now distinguish host profiles and plan limits.

The validator passes all fifteen skills and 31 exported files. Nine packaging tests pass, and two builds produce identical 21-file output sets. Official Gemini CLI 0.65.0 installed the extracted candidate archive in an isolated configuration; all 31 installed files match and fifteen skills are present. The CLI accepts a local folder rather than a direct ZIP path. GitHub release-asset installation and live authentication still require acceptance before publication.

Independent source review exercised Free portfolio comparison limits, Gemini dashboard requests, separate authentication/plan/consent/permission outcomes, hostile merchant text and the legacy dashboard launcher. The review found an unqualified dynamic-registration claim in the connect skill; the corrected text limits the claim to Gemini. This review did not call a model or access an account.

The shared central skill registry check reports existing inventory, recommendation and source-authority drift outside this library. The fifteen canonical library files pass their individual skill-format checks. This change does not repair unrelated generated or installed skills.

Live Free/paid reads, model conversations, idle-access and revocation checks remain pending. Historical paid-Gemini results above do not establish acceptance for the new profile.
