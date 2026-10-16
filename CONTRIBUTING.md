# Contributing

Add a skill when it serves a distinct user goal supported by Fillfolio's current tools. Improvements to an existing workflow are preferable to a second skill for the same task.

- Keep each skill self-contained in `skills/<name>/SKILL.md`; standalone ZIP installation must preserve its instructions.
- Use a matching lowercase name, a quoted description of at most 200 characters and `license: MIT` in YAML frontmatter. Describe the user's trigger, then write the workflow.
- Register the folder and all tools it may call in `catalog.json`. A tool dependency does not grant access or promise host support.
- Check the live tool schema and [MCP reference](docs/mcp-reference.md). Preserve pagination, currency and coverage semantics. Label derived calculations and user-supplied assumptions.
- Keep account reads in the connected MCP tool namespace. Use the host's OAuth flow for sign-in and Fillfolio Settings for permissions. Do not add password collection or direct token handling.
- Use synthetic examples. Exclude customer records, reviewer details, local operational files and credentials.
- Verify client-specific instructions against official documentation and state which behavior was actually tested.

Run `python3 scripts/validate.py` and `python3 scripts/build.py`. The validator checks folder metadata, catalog dependencies, references and public-package boundaries. Review the resulting ZIP contents and checksums before release. Test substantive workflow changes with synthetic tool responses, including incomplete results and pagination.

The repository owns this public library. Updating it does not update Fillfolio's hosted server or an installed/submitted plugin. Release those surfaces through their own processes.
