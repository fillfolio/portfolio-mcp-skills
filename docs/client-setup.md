# Client setup

Gemini profile updated on **October 27, 2026**. The other client examples retain their earlier documented setup; this change adds no new host acceptance result.

Choose the workflows you need from `skills/`. Copy each selected folder, including its `SKILL.md` and references, to your client's skill directory below. For a host that accepts ZIP uploads, use the ZIP for that workflow from a release. Keep the skill folder at the archive root. The shared file format follows the [Agent Skills specification](https://agentskills.io/specification).

## Connection requirements and status

Choose the registered profile for your host. The Gemini extension uses **`https://free-mcp.fillfolio.com/mcp`** with scope **`portfolio:read`** for Free and paid accounts. It provides nine financial read tools and no dashboard launcher or UI resource. The legacy profile below uses **`https://fillfolio.com/api/mcp`** with **`mcp:read`**. Keep each profile's endpoint, client identity, resource and scope together. Connect through your host's OAuth flow. Fillfolio accepts approved client identities and callbacks; it does not offer general-purpose client registration. A client must use an accepted identity, support PKCE with `S256`, request the active profile's scope, and bind authorization to that profile's MCP resource. Use Fillfolio's advertised MCP authentication metadata and scopes. Account sign-in scopes from an identity provider do not replace MCP authorization.

Fillfolio has registered identities for ChatGPT, Codex, Claude web, and Claude Code. Registration establishes which identity Fillfolio accepts; a successful connection also depends on the host's discovery, redirect, and token behavior. Other clients need an accepted preregistered identity and callback configuration before their OAuth connection can work. See the [public MCP contract](https://github.com/fillfolio/portfolio-mcp) for Fillfolio's authorization contract and the [MCP authorization specification](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization) for the protocol.

| Host | Skill format documented | Fillfolio connection evidence |
| --- | --- | --- |
| Codex | Local skill folders | Existing Codex setup passed live acceptance before this library |
| ChatGPT | Desktop standalone skills; plugins on supported surfaces | Existing ChatGPT Work desktop setup passed live acceptance before this library |
| Claude Code | Local skill folders | Registered identity; this library adds no new host acceptance result |
| Claude chat | Custom skill ZIP uploads | Registered identity; this library adds no new host acceptance result |
| Gemini CLI | Bundled extension with fifteen skills | Official CLI 0.65.0 Free native checks and eight model cases pass; live paid tests deferred |
| Antigravity | Project `.agents/skills/` folders | Account connection not verified |
| Cursor | Local skill folders | Conditional on an accepted identity and callback; no live acceptance claimed here |
| VS Code / GitHub Copilot | Local skill folders | Conditional on an accepted identity and callback; no live acceptance claimed here |

Library format checks do not establish OAuth compatibility. The native Fillfolio plugin and this Gemini extension have separate releases and acceptance evidence; consult their current listings for availability. Copying these skill folders installs workflow instructions; complete your host's connection or plugin installation flow to obtain tools.

## Codex

Copy `skills/<selected-folder>` to `~/.agents/skills/<selected-folder>` for personal use, or `.agents/skills/<selected-folder>` in a project. Codex documents these discovery locations and supports explicit skill selection with `$` or `/skills`. [Codex skill guide](https://learn.chatgpt.com/docs/build-skills)

Add a remote server entry to your personal `~/.codex/config.toml` if your current setup does not already provide the Fillfolio connection:

```toml
[mcp_servers.fillfolio]
url = "https://fillfolio.com/api/mcp"
```

Then run `codex mcp login fillfolio` and complete the browser authorization. Reuse the current registered Codex identity and matching callback behavior. A custom client ID or callback override must match a separate accepted registration. Codex documents HTTP configuration, OAuth login, CIMD selection, and callback rules in its [MCP guide](https://learn.chatgpt.com/docs/extend/mcp?surface=cli).

## ChatGPT

Use the skill or plugin installation flow available on your surface. OpenAI documents standalone skills in the ChatGPT desktop app and plugins across supported ChatGPT surfaces. Hosted ChatGPT uses installed plugin connectors for remote MCP tools; ChatGPT web does not read your local Codex configuration. Uploading a `SKILL.md` as an ordinary attachment does not install or connect Fillfolio. [Skill availability](https://learn.chatgpt.com/docs/build-skills), [plugin installation](https://learn.chatgpt.com/docs/plugins), [hosted MCP setup](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)

Use an existing private or eligible host setup you already have access to. This repository provides no public directory installation link. Complete Fillfolio OAuth when the host prompts you, then select the workflow you installed.

## Claude Code

Copy `skills/<selected-folder>` to `~/.claude/skills/<selected-folder>` for personal use, or `.claude/skills/<selected-folder>` in a project. Invoke it with `/skill-name` or describe a matching task. [Claude Code skills](https://code.claude.com/docs/en/skills)

For a new connection, add the endpoint and open `/mcp` in an interactive Claude Code session to sign in:

```sh
claude mcp add --transport http --scope user fillfolio https://fillfolio.com/api/mcp
```

Claude Code supports CIMD discovery and preregistered OAuth clients. Use its registered published identity with the current Fillfolio endpoint. If a separate registration requires a fixed callback, follow Claude Code's `--client-id` and `--callback-port` instructions with the exact accepted values. [Claude Code MCP authentication](https://code.claude.com/docs/en/mcp)

## Claude chat

Upload a selected workflow ZIP through **Customize → Skills → + → Create skill → Upload a skill**, then enable it. Claude requires code execution for skills. The ZIP must contain the skill folder at its root, with `SKILL.md` inside. [Upload and enable skills](https://support.claude.com/en/articles/12512180-use-skills-in-claude), [ZIP structure](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)

Add the endpoint through **Customize → Connectors → Add custom connector** and complete OAuth. Select Claude's published identity when it matches Fillfolio's accepted registration. Fillfolio does not dynamically register Claude clients. The own-client option requires an existing accepted client ID and callback registration. Organization policy can require an owner to add the connector. [Custom connector setup](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp)

Claude's hosted callback is `https://claude.ai/api/mcp/auth_callback`. Its hosted connector traffic comes from Anthropic's infrastructure. Claude documents the discovery fields it requires before selecting CIMD in its [connector authentication guide](https://claude.com/docs/connectors/building/authentication).

## Cursor

Copy `skills/<selected-folder>` to `~/.cursor/skills/<selected-folder>` for personal use, or `.cursor/skills/<selected-folder>` in a project. Cursor also reads `.agents/skills/` and `~/.agents/skills/`. Personal local skills need separate syncing for Cloud Agents. A GitHub repository import through Cursor's UI requires a plugin package; use manual copying for this library. [Cursor skills](https://cursor.com/docs/skills)

Use the following pattern in `~/.cursor/mcp.json` or a project's `.cursor/mcp.json` **only after Fillfolio accepts a client registration for that Cursor surface**. Replace the placeholder with its registered public client ID before use:

```json
{
  "mcpServers": {
    "fillfolio": {
      "url": "https://fillfolio.com/api/mcp",
      "auth": {
        "CLIENT_ID": "<REGISTERED_PUBLIC_CLIENT_ID>"
      }
    }
  }
}
```

Cursor documents `http://localhost:8787/callback` for desktop and `https://www.cursor.com/agents/mcp/oauth/callback` for web/Agents. Fillfolio must accept the relevant callback with the client registration. Follow Cursor's OAuth prompts after setup. [Cursor remote MCP and static OAuth](https://cursor.com/docs/mcp)

## VS Code / GitHub Copilot

Copy `skills/<selected-folder>` to `.agents/skills/<selected-folder>`, `.github/skills/<selected-folder>`, or `.claude/skills/<selected-folder>` in a project. Personal locations include `~/.agents/skills/`, `~/.copilot/skills/`, and `~/.claude/skills/`. [VS Code Agent Skills](https://code.visualstudio.com/docs/agent-customization/agent-skills)

The following VS Code-specific `.vscode/mcp.json` pattern requires an accepted client registration and callback configuration. Replace the placeholder with its registered public client ID before use:

```json
{
  "servers": {
    "fillfolio": {
      "type": "http",
      "url": "https://fillfolio.com/api/mcp",
      "oauth": {
        "clientId": "<REGISTERED_PUBLIC_CLIENT_ID>"
      }
    }
  }
}
```

VS Code opens a browser for OAuth on first connection. Its documentation also describes portable `.mcp.json` configurations with a top-level `mcpServers` object. Use the configuration format supported by your selected VS Code agent session. [OAuth configuration](https://code.visualstudio.com/docs/agents/reference/mcp-configuration), [configuration locations](https://code.visualstudio.com/docs/agent-customization/mcp-servers)

## Gemini CLI

Install the combined extension:

```sh
gemini extensions install https://github.com/fillfolio/portfolio-mcp-skills
```

Before the first account read, run `/mcp auth fillfolio` inside Gemini CLI and use the browser consent flow. Run the command again when reauthorization is needed. The extension uses public client `fillfolio-free-gemini-cli`, requests `portfolio:read`, and fixes the callback to `http://localhost:7777/oauth/callback`. Keep that port available. [Fillfolio Gemini guide](gemini-cli.md), [Gemini extension format](https://geminicli.com/docs/extensions/reference/), [Gemini MCP authentication](https://geminicli.com/docs/tools/mcp-server/)

As of October 27, 2026, the client is active. Free native checks and eight synthetic model cases pass with official CLI 0.65.0; live paid tests are deferred. Free accounts can read one selected manual portfolio and three active assets. Paid categories require eligible access and explicit consent; spending and budgets also require separate client permissions. Gemini provides no dashboard launcher or UI resource on this endpoint. An installed extension alone does not establish authenticated access.

## Antigravity

For instruction-only use, clone this repository and copy selected canonical `skills/<selected-folder>` directories into your project's `.agents/skills/`. Preserve each folder name and its `SKILL.md`. Avoid copying a skill over a locally edited copy. [Antigravity skills](https://antigravity.google/docs/skills)

These folders provide workflows. The Fillfolio account connection in Antigravity is **not verified**; authenticated tools require a separately accepted OAuth identity/callback and host acceptance. No Antigravity store listing or working MCP connection is claimed.

## Gemini Enterprise

Gemini Enterprise uses an organization-administered custom MCP connection. This CLI extension does not configure that service. Enterprise authentication and administrator setup remain deferred. [Google custom MCP setup](https://docs.cloud.google.com/gemini/enterprise/docs/connectors/custom-mcp-server/set-up-custom-mcp-server)

## Other MCP clients

Check whether your client reads the Agent Skills format and where it discovers skill folders. If it does, copy only your selected workflow folders into that location. If it lacks skill discovery, you can read a workflow's instructions as a manual reference, subject to the tools your host exposes.

Remote MCP support alone does not establish a Fillfolio connection. Confirm the client's accepted OAuth identity and callback, resource binding, PKCE `S256`, and the scope required by that registered profile before setup. Keep credentials in the host's OAuth connection flow. Consult the [MCP authorization specification](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization) and your client's official documentation.
