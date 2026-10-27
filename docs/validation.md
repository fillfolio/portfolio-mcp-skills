# Validation

Version **0.1.1**, checked October 27, 2026.

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

## Current Gemini Free acceptance

We tested the dedicated nine-tool profile with the official Gemini CLI **0.65.0** and an account whose owner confirmed its records are synthetic. The profile uses `https://free-mcp.fillfolio.com/mcp`, `fillfolio-free-gemini-cli`, `portfolio:read` and the exact `http://localhost:7777/oauth/callback` redirect.

| Check | Observed result |
| --- | --- |
| Explicit authorization and reconnection | Browser sign-in, consent, callback and token exchange passed through the official CLI OAuth components |
| Native discovery and reads | Nine read-only tools; summary, portfolio listing, three holdings pages, returned asset ID and opening activity passed |
| Free category boundaries | Cash, spending, transactions and budgets returned the expected `plan_required` tool errors; summary still worked afterward |
| Continued access | A correct later summary followed 660 seconds with no intervening Gemini requests; token rotation was not observed |
| Gemini-only revocation | The retained session received HTTP 401 after revocation; explicit Gemini reconnection and reads passed |
| Model workflows | Eight cases passed with `gemini-3.5-flash-lite`: summary, holdings pagination, returned asset, opening activity, Free spending denial, financial-write refusal, cross-user refusal and inline hostile data |

The continued-access check ran before a web-only error-format correction. That correction changes the exact Gemini client's permission-error text, with no OAuth or refresh-code change. The corrected runtime passed the Free denials and permitted reads again. The official CLI promotes JSON error text into success-schema validation; the correction retains HTTP 200 and `isError: true` with a fixed error code in plain text. Authentication failures remain HTTP 401.

The eight model cases used the owner's existing Google AI Studio Free-tier project. No billing was enabled and no key was created. Eight CLI invocations completed; the number of model HTTP requests was not observed. The bounded headless test configuration allowed only skill activation and the nine Fillfolio read tools, with shell, file and web tools excluded. These results do not claim default headless-policy behavior or model execution of all fifteen workflows. The hostile-label case used inline synthetic data, not a live bank-import path.

Root and independent reviewers checked the saved answers for currency labels, missing values, opening-history limits, permission handling and refusal behavior. Failed diagnostic attempts remain separate from the completed run. Model credentials stayed outside the public package.

## Deferred and separate evidence

Live paid-plan fixtures, the paid permission matrix and downgrade acceptance are **deferred** by the owner. No temporary plan or fixture changes began. The current Free results do not establish paid live acceptance.

The owner supplied a fresh screenshot from the existing ChatGPT Fillfolio conversation after the Gemini revoke/reconnect sequence. Its October 27, 16:55 local retrieval shows the expected synthetic USD 10,912 net worth and a new answer. This is an owner-assisted final control, not an independently captured request or a complete before/during/after sequence. Earlier Work/Codex results remain separate evidence.

Earlier October 17 tests used official CLI 0.64.0 components and the old paid-only profile. They covered ten-tool discovery, portfolio pagination, the four spending/budget permission states, dashboard resource delivery and 662,704 milliseconds of continued access. They did not exercise model answers or dashboard rendering and do not establish acceptance of the current profile.

Current source and offline authentication tests cover exact callback/resource/scope/PKCE checks, authentication failures and replay/expiry handling. We do not claim new-profile live canceled-consent or occupied-callback-port acceptance. Antigravity authenticated access and Gemini Enterprise remain unverified or deferred. The Gemini profile provides no dashboard launcher or UI resource.

## Installation and release checks

All fifteen canonical skills pass individual format checks. The repository validator accepts 31 exported files; nine packaging tests and eight companion contract tests pass. Two final builds must produce identical bytes. Local installation uses an extracted folder: CLI 0.65.0 does not accept a direct local ZIP path. The earlier fresh GitHub candidate-ref installation matched all 31 files and fifteen skills.

The release attaches only `fillfolio-v0.1.1.zip`, with its SHA-256 in the release description. Final source commits, checksum and the fresh unqualified GitHub-release installation result belong in those release notes. Additional release assets would cause the tested CLI to select a source-tarball fallback. Older standalone downloads remain available. Gallery discovery remains pending until Google displays the extension.

The central skill-registry check reports pre-existing drift outside this library. The fifteen canonical library files pass their own format checks; this release does not repair unrelated generated skills. The native Fillfolio plugin has a separate listing and release lifecycle.
