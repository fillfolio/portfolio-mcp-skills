# Fillfolio portfolio MCP skills

Reusable skills for discussing your stored Fillfolio portfolio, stocks, ETFs, funds, crypto, cash, bank spending and budgets with an AI assistant.

Connect an accepted MCP client to **`https://fillfolio.com/api/mcp`**, then install the workflows you need. The skills follow the [Agent Skills format](https://agentskills.io/specification). They provide instructions for using Fillfolio's read-only tools; your client handles authentication and model usage.

## Choose a workflow

| Skill | What you can ask |
| --- | --- |
| [Connect or open Fillfolio](skills/fillfolio-connect/SKILL.md) | Connect my account or open the plugin dashboard. |
| [Portfolio overview](skills/fillfolio-portfolio-overview/SKILL.md) | Explain my net worth, cash, debt and available return. |
| [Holdings allocation](skills/fillfolio-holdings-allocation/SKILL.md) | Break down my stocks, ETFs, funds and crypto. |
| [Concentration review](skills/fillfolio-concentration-review/SKILL.md) | Which visible holdings account for the largest exposures? |
| [Asset review](skills/fillfolio-asset-review/SKILL.md) | Where do I hold this exact asset? |
| [Compare portfolios](skills/fillfolio-compare-portfolios/SKILL.md) | Compare my saved portfolios in one reporting currency. |
| [Cost basis and return](skills/fillfolio-cost-basis-review/SKILL.md) | Explain current gains and missing cost basis. |
| [Cash and debt](skills/fillfolio-cash-debt-review/SKILL.md) | Show cash and liabilities by their native currencies. |
| [Investment activity](skills/fillfolio-investment-activity/SKILL.md) | Summarize stored investment activity for a date range. |
| [Spending overview](skills/fillfolio-spending-overview/SKILL.md) | Show last month's spending by category and currency. |
| [Compare spending](skills/fillfolio-compare-spending/SKILL.md) | Compare two periods with the same filters. |
| [Merchant review](skills/fillfolio-merchant-review/SKILL.md) | Review all matching transactions for a merchant. |
| [Transaction review queue](skills/fillfolio-transaction-review/SKILL.md) | Explain the bank records that need my review. |
| [Budget review](skills/fillfolio-budget-review/SKILL.md) | Compare monthly limits with stored actuals. |
| [Public connection catalog](skills/fillfolio-public-connections/SKILL.md) | Check a brokerage, exchange, bank or blockchain connection. |

The first fourteen workflows use authenticated MCP. The public connection catalog uses an unauthenticated HTTP endpoint and requires a host that can fetch it.

## Gemini CLI extension

Version **0.1.1** bundles the fifteen workflows, Gemini context and a dedicated OAuth configuration in one extension. **Preparation status, October 17, 2026:** packaging is ready for validation; server activation and live Gemini acceptance remain pending. This status does not claim a working Gemini connection or gallery listing.

After the release passes acceptance and publishes, install it with:

```sh
gemini extensions install https://github.com/fillfolio/portfolio-mcp-skills
```

Open Gemini CLI, run `/mcp auth fillfolio`, and complete browser sign-in and consent. Ask “Show my Fillfolio portfolio summary.” Use your own Gemini access and quota. See the [Gemini guide](docs/gemini-cli.md) for callback requirements, manual updates and current evidence. Gemini CLI dashboard rendering is unverified.

## Standalone skills

1. [Connect your AI client](docs/client-setup.md). Confirm that Fillfolio accepts its OAuth identity and callback.
2. Download a selected skill ZIP from [Releases](https://github.com/fillfolio/portfolio-mcp-skills/releases), or clone this repository:

   ```sh
   git clone https://github.com/fillfolio/portfolio-mcp-skills.git
   ```

3. Copy the selected folder from `skills/` to your client's skill directory, or upload its ZIP through the client's skill installer. Each folder works on its own. For example, Codex reads personal skills from `~/.agents/skills/`; Claude Code reads `~/.claude/skills/`.
4. Select the installed skill or ask a matching question. Complete sign-in through the client's OAuth interface.

[Client setup](docs/client-setup.md) covers ChatGPT, Codex, Claude Code, Claude chat, Cursor, VS Code and other compatible hosts, with links to their official instructions. MCP support, skill support and dashboard rendering are separate capabilities. Registration and account eligibility also affect access.

**Status, October 16, 2026:** the existing ChatGPT Work desktop and Codex connections passed live acceptance. This library does not establish a new authentication pass for every client. Fillfolio's separate native plugin **0.1.1 is In review**; public directory approval is pending. This skill library has its own **0.1.1** release candidate and does not replace that submitted package.

## Data and access

Fillfolio tools read stored account records. They cannot place trades, move money, edit records or budgets, or trigger provider refreshes. Access depends on your plan, connected providers, stored history and the approved client. Spending and budgets also require bank spending consent and separate per-client permissions.

The workflows preserve reporting currencies, missing valuations, cost-basis coverage, incomplete bank history and synchronization information. A response timestamp does not establish quote freshness. Current value versus cost is not a historical investment-performance series. See the [MCP reference](docs/mcp-reference.md) for the supported fields and calculations.

Your selected AI service receives the financial records returned to its chat. Opening a dashboard view shares that view's data; Discuss selection shares the selected records. Hide amounts masks the panel only and cannot retract data already shared. Manage or revoke future access in Fillfolio Settings. Keep credentials in the host's OAuth interface.

## Directory submissions

The [submission ledger](docs/directory-submissions.md) tracks directory routes, prerequisites and public outcomes for this library and its [MCP companion](https://github.com/fillfolio/portfolio-mcp). The [AI-related policy report](docs/ai-submission-policies.md) identifies owner-only authorship routes and disclosure requirements.

## Maintain or extend the library

[`catalog.json`](catalog.json) records the fifteen canonical workflows and their tool dependencies. The [public MCP contract](https://github.com/fillfolio/portfolio-mcp) is maintained separately. Read [CONTRIBUTING.md](CONTRIBUTING.md) before adding a workflow.

```sh
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate.py
python3 scripts/build.py
```

The builder preserves the complete library and standalone skill ZIP formats in `dist/`. It also creates one Gemini extension ZIP with its manifest at the archive root in `dist/gemini/`. For the Gemini release, upload **only the ZIP** and put its SHA-256 in the release description. Keep `release-manifest.json` and `SHA256SUMS` as local release evidence. Gemini CLI 0.64.0 selects the generic ZIP only when the release has one attached asset; additional assets cause source-tarball fallback. Older release assets remain available. Consumers need no Python dependency to read or install a skill. See [validation evidence](docs/validation.md) for the checks and their scope.

MIT license. Fillfolio is operated by VMPRO LLC. [Developer website](https://fillfolio.com/) · [Privacy](https://fillfolio.com/privacy) · [Official MCP connection page](https://fillfolio.com/mcp)
