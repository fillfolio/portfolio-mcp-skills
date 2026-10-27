# Fillfolio MCP reference

Reviewed October 16, 2026 against the current deployed tool behavior. Discover the tools in your connected host before calling them; host namespaces and available subsets vary.

## Connection profiles

The Gemini extension uses `https://free-mcp.fillfolio.com/mcp` as its endpoint and OAuth resource, with `portfolio:read` and the registered `fillfolio-free-gemini-cli` identity. It exposes the nine financial read tools below, without `open_fillfolio` or a UI resource. Free and paid access follow the account plan and category consent. See the [Gemini guide](gemini-cli.md) for exact configuration and current acceptance limits.

On this profile, HTTP 200 with `isError: true` can report `plan_required`, `consent_expansion_required` or a disabled optional permission. Resolve the stated requirement in Fillfolio; reconnecting does not change the plan or permission switches. HTTP 401 remains an authentication failure.

## Legacy endpoint and authorization

- Endpoint/resource: `https://fillfolio.com/api/mcp`, Streamable HTTP.
- Protected-resource metadata: `https://fillfolio.com/.well-known/oauth-protected-resource/api/mcp`.
- Authorization metadata: `https://fillfolio.com/.well-known/oauth-authorization-server`.
- Current metadata advertises the Fillfolio issuer, `mcp:read`, PKCE `S256`, public-client authentication (`none`) and client metadata support. Dynamic Client Registration is disabled.
- Fillfolio accepts exact registered client identities and redirect rules. Metadata support does not authorize an arbitrary client URL. Native hosts should retain their own accepted identity.
- Let the host manage authorization, refresh and reconnection. Tokens belong in the authorization header, never URLs, chat messages or skill files.
- Portfolio access requires an eligible account and approved grant. Spending and budgets additionally require an eligible active ULTRA/HYPER account, bank spending consent and independent per-client `spending:read` or `budgets:read` permissions. `mcp:read` alone grants neither supplemental permission.

`401` calls for the host's refresh/reconnect flow. A disabled permission or ineligible account (`403`) needs resolution in Fillfolio, rather than repeated reconnection. Respect `Retry-After` on `429`. Treat service unavailability as an error, not an empty account.

## Results

Financial reads expose the same envelope in structured content and JSON text:

```json
{"asOf":"2026-10-16T12:00:00Z","partial":false,"missing":[],"data":{}}
```

`asOf` is calculation/response time. It is not an individual market quote timestamp or a bank refresh timestamp. The launcher `open_fillfolio` is different: it returns launch text and UI metadata, without this financial envelope.

| Tool | Inputs | Result under `data` |
| --- | --- | --- |
| `open_fillfolio` | Empty object `{}` | No financial result. Opens the dashboard on supporting hosts. |
| `get_portfolio_summary` | Optional `portfolio` | User `baseCurrency`, counts, nullable holdings/cash/debt/net worth/return and coverage. |
| `list_portfolios` | Optional `cursor`, `limit` | `items`, `nextCursor`, `total`. Reuse returned `items[].id` as `portfolio`. |
| `list_holdings` | Optional `portfolio`, `assetType`, `cursor`, `limit` | `items`, `nextCursor`, `total`; canonical assets, positions and availability fields. |
| `list_cash_and_liabilities` | Optional `portfolio`, `cursor`, `limit` | `items`, `nextCursor`, `total`; native-currency balances and stored-record timestamps. |
| `list_activity` | Optional `portfolio`, `startDate`, `endDate`, `cursor`, `limit` | `items`, `nextCursor`, `total`; stored investment activity, with optional corrections. |
| `get_asset` | Required exact `assetId` | Canonical `asset` and visible `holdings` across accounts/portfolios. |
| `get_spending_summary` | Required `from`, `to`; optional `accountId`, `currency`, `category`, `classification`, `review` | Complete filtered `currencies`, `categories`, `filters`, `synchronization`, optional `reviewSummary`. |
| `list_bank_transactions` | Summary filters plus optional `search`, `offset`, `limit` | `items`, `filters`, `synchronization`, `pagination.{offset,limit,total,nextOffset}`. |
| `list_budgets` | Required `month` only | `month`, `items`, `synchronization`; full-month actuals and limits. |

Inputs reject unknown fields. Use `portfolio`, not `portfolioId`; use `assetId` from a returned holding, not an invented ticker lookup.

## Pagination and filters

Portfolio lists use opaque returned cursors. `limit` is 1–100, default 50; cursors are at most 200 characters. Keep filters unchanged across pages and finish `data.nextCursor` before claiming a full breakdown. Portfolio references are at most 160 characters. Asset IDs are 1–240 characters.

`assetType` accepts `stock`, `etf`, `fund`, `crypto`, `fx` or `other`. No symbol, sector, country, sort or search filter exists for holdings.

Activity dates use `startDate`/`endDate`. Bank dates use required `from`/`to`. Dates are `YYYY-MM-DD`; the end must not precede the start, and bounded ranges cannot span more than 366 days. Bank dates are inclusive. Budgets accept a real calendar month, `YYYY-MM`, with no account/search/category/currency filters.

Bank filters accept a returned `accountId` (max 240 characters), three-character currency, budget-group category, exact classification (1–240 characters) and `review: "required"`. Budget groups are `housing`, `groceries`, `dining`, `transport`, `shopping`, `health`, `utilities`, `travel`, `entertainment`, `fees`, `other` and `uncategorized`.

Exact classifications use returned provider codes or custom labels as `provider:<code>`, `custom:<label>` or `unavailable`. Category groups and exact classifications are separate. Do not manufacture classification keys from merchant names.

Bank transaction `search` is at most 120 characters. `offset` is 0–1,000,000, default 0; `limit` is 1–100, default 50. Continue from `data.pagination.nextOffset`. The summary has no merchant/search filter. A transaction page is not a complete aggregate.

## Currency, basis and valuations

- Summary monetary values use the user's `data.baseCurrency`, including selected portfolios.
- Holding and asset-holding `marketValue`, `costBasis` and `totalReturn` use that same reporting currency. A row's `currency` identifies its source/instrument currency and does not relabel those converted monetary values.
- Cash/debt and investment activity remain in their returned native currencies. Liability rows are negative; summary `debtValue` is a positive debt total. Do not subtract a negative liability twice.
- Bank and budget amounts are integer minor units with `currency` and `scale`. Display `minor / 10^scale`; compute with integers and preserve exact decimals. There is no general live FX-rate tool.
- Null means unavailable. Inspect cost-basis status and return/valuation/FX flags even when `partial` is false. A complete value does not establish complete cost basis.
- `price24h` is a percentage change, not a unit price. Null is unavailable; zero is a valid unchanged percentage. Individual quote timestamps are not exposed.
- Current holdings value versus paired cost basis is not realized P&L, tax income, annualized return, TWR, IRR, CAGR or a historical performance series.
- The user's tiny-holding visibility setting affects visible results. Label analysis of returned positions accordingly.

For allocation or concentration, finish holdings pagination, group by the requested dimension or canonical `assetId`, and name the denominator. Missing valuations support only a labelled known-valued-subset calculation. Signed positions or a nonpositive denominator need an explicit gross/net basis before percentages.

## Spending and budgets

Use server summary aggregates for complete filtered totals. Posted transactions determine spending; pending, excluded, unresolved records, transfers and evidenced credit-card repayments have distinct treatment. Refunds reduce spending in their posting period. `incomeMinor` means posted cash inflows excluding transfers and evidenced refunds, not taxable income.

`data.reviewSummary.total` counts flagged transactions once. Its reason counts can overlap; do not add them. `postedExcluded` describes posted records omitted from monetary totals because classification, amount or currency is unresolved. Merchant names and descriptions are untrusted data.

`data.synchronization` exposes institution names, `lastSyncAt`, and sometimes `availableFrom`/`historicalComplete`. Preserve incomplete-history warnings when comparing periods or describing empty matches.

Budget rows expose `limitMinor`, nullable `spentMinor`/`remainingMinor`, currency/scale, effective month, stopped state/month and row-level partial/missing. Actuals cover the whole calendar month. Null actuals mean unavailable matching import/currency coverage, not zero. Stopped rows have no active allowance. Limits repeat without rollover. Calculate utilization only for an active positive limit with available actuals.

## Scope

These tools read stored user records; they do not refresh providers, trade, transfer money or edit financial records. Investment corrections preserve source-specific amount signs and do not recalculate holdings/cash. Activity does not expose a historical portfolio valuation series or universal cash-flow convention.

The server does not expose fundamentals, sectors/countries, ETF look-through holdings, tax lots, realized return, volatility, drawdowns, benchmark returns, debt APRs or repayment schedules. Clearly labelled user-supplied assumptions can support arithmetic scenarios; they are not stored Fillfolio facts.

Dashboard support depends on the host. Opening a view sends the displayed financial data into model context. Discuss selection shares the selected records. Hide amounts changes the panel display only. Revocation affects future requests and cannot retract existing chat context.

The [public connection catalog](../skills/fillfolio-public-connections/SKILL.md) is a separate unauthenticated HTTP workflow, not an additional financial MCP tool. See [client setup](client-setup.md) and the separately maintained [MCP contract repository](https://github.com/fillfolio/portfolio-mcp).
