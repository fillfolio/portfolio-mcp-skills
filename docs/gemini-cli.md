# Fillfolio for Gemini CLI

The extension combines the fifteen canonical skills in this repository with `GEMINI.md` context and the remote Fillfolio MCP configuration.

**Preparation status, October 26, 2026:** the 0.1.1 package awaits completion of live Gemini acceptance. The install instructions below apply after acceptance and publication. Gallery discovery remains pending until Google displays the listing. This profile has nine financial read tools and no dashboard launcher or UI resource.

## Install and connect

Use an official Gemini CLI version that passes the recorded acceptance checks. The release evidence will identify the tested version; package validation alone does not establish a minimum supported version.

```sh
gemini extensions install https://github.com/fillfolio/portfolio-mcp-skills
```

Review the extension and its MCP connection before accepting installation. Open Gemini CLI, then authenticate before the first account read:

```text
/mcp auth fillfolio
```

Complete Fillfolio sign-in and consent in the browser. Run `/mcp auth fillfolio` again when reauthorization is needed. Gemini CLI 0.65.0's automatic sign-in path does not preserve the configured client ID and callback; use the explicit command for Fillfolio. Keep passwords, verification codes and tokens in that flow. Ask “Show my Fillfolio portfolio summary” to test authenticated reads. If the host reports a disabled permission, open Fillfolio Settings to manage it; reconnecting does not enable permission toggles.

The manifest uses these accepted values:

| Setting | Value |
| --- | --- |
| HTTP endpoint and OAuth resource | `https://free-mcp.fillfolio.com/mcp` |
| Public client ID | `fillfolio-free-gemini-cli` |
| Scope | `portfolio:read` |
| Exact callback | `http://localhost:7777/oauth/callback` |
| Authentication | Authorization Code with PKCE S256, no client secret |

Leave port 7777 free for the callback. Stop an interrupted authentication attempt before trying again. Use the extension's preregistered Gemini client and exact callback. Fillfolio does not dynamically register Gemini clients.

The hosted service supports Free and paid accounts. Free includes one selected manual portfolio and three active assets, with the account-wide Free quota. Additional categories require eligible paid access and explicit consent. Provider coverage, stored history and account plan affect the available records. Spending and transactions require bank spending consent and this client's `spending:read` permission. Budgets require its separate `budgets:read` permission. Use Fillfolio Settings to revoke future access.

Users supply their own Gemini account, model access and quota. Fillfolio does not pay for model usage. Google's quotas and account terms apply.

## Data and host limits

The connection reads stored portfolio, brokerage, exchange, bank and wallet records. It cannot trade, move funds, edit data or budgets, or trigger a provider refresh. Preserve currencies, missing exchange rates and cost basis, incomplete bank history and source synchronization times in answers. A generated response time does not establish quote freshness.

The AI service receives the records returned through MCP. On hosts that render Fillfolio's dashboard, opening a view shares its data and Discuss selection shares selected records. Hide amounts masks the panel only and cannot retract prior context. This profile provides no dashboard launcher or UI resource; use its financial read tools for portfolio or eligible spending questions.

## Manual updates and removal

Review new release notes, then update on demand:

```sh
gemini extensions update fillfolio
```

Remove the local extension with:

```sh
gemini extensions uninstall fillfolio
```

Removing an extension does not establish server-side revocation. Revoke the Gemini grant in Fillfolio Settings to end future account access. The project configures no synchronization or scheduled update job.

## Packaging and publication

Run the repository validator, tests and builder before publishing. The builder preserves the library and standalone skill formats and creates a separate `dist/gemini/` release set:

- `fillfolio-v0.1.1.zip`, with `gemini-extension.json`, `GEMINI.md` and `skills/` at its root.
- `release-manifest.json`, with the source-file and archive checksums.
- `SHA256SUMS`, covering the ZIP and release metadata.

Upload **only the ZIP** to the 0.1.1 GitHub release. Put its SHA-256 in the release description; retain the metadata and checksum files as local evidence. Gemini CLI 0.65.0 selects a generic ZIP only when the release has one attached asset. Additional assets cause source-tarball fallback. The unqualified install must select the extension ZIP. Keep older release assets available for standalone skill installation. Publish the root manifest on the default branch and add the `gemini-cli-extension` topic only after native acceptance passes. Google controls gallery validation and discovery. [Extension releases and discovery](https://geminicli.com/docs/extensions/releasing/)

## Other Google clients

Copy selected skill folders to `.agents/skills/` for Antigravity instruction discovery. Its Fillfolio account connection is not verified. Gemini Enterprise authentication and organization setup remain deferred. See the [client setup guide](client-setup.md).

## Official links and license

- [Developer website](https://fillfolio.com/)
- [Official MCP connection page](https://fillfolio.com/mcp)
- [Canonical MCP contract](https://github.com/fillfolio/portfolio-mcp)
- [Canonical skills, releases and support](https://github.com/fillfolio/portfolio-mcp-skills)

The public materials use the MIT license. VMPRO LLC operates the hosted Fillfolio service under separate account, plan and permission requirements.
