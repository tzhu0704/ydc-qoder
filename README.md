# You.com Research Assistant for Qoder (development preview)

A Qoder plugin for public-web search, page extraction, sourced research, and claim verification. It bundles two Skills and a connection to You.com's **keyless free MCP endpoint**. No account or API key is needed for the basic tools; the provider currently limits free use to 100 queries per day. This is not a browser automation plugin and is not yet published or approved by Qoder.

## What it includes

- `youcom-web-research`: find and read current public sources and prepare a cited briefing.
- `youcom-source-verification`: compare checkable claims against original and independent sources.
- `.mcp.json`: `https://api.you.com/mcp/free`, exposing `you-search`, `you-extract`, and `you-discover`.

The free endpoint does **not** expose paid `you-research` or `you-finance` tools. It does not log in to websites, click, fill forms, or automate a browser. Do not send private data to public search without authorization.

## Try locally

Import this folder in the Qoder plugin UI, or, if Qoder CLI is installed, run `qoder plugins validate .` and `qoder plugins install . --scope local`. Reload plugins and inspect the MCP server status. Try: “Search for this week's You.com API updates, extract the original documentation pages, and cite each substantive claim.” Test both successful connection and quota/network failures. The actual Qoder client import, MCP handshake, and OAuth experience still require client-side verification.

For a credential-free local smoke test, run `python3 scripts/check_plugin.py --live`. It validates the package, connects to the free endpoint and calls search and extraction once each. It does not exercise Qoder's plugin loader.

## Before pushing to GitHub

Run `python3 scripts/prepublish_check.py` and review the files you plan to stage. `.gitignore` excludes local environment files, credentials, generated ZIPs, and build artifacts; it does not remove any secrets already committed to Git history. Do not commit development API keys, private test logs, or real user inputs. If a secret was previously committed, rotate it and clean the repository history before publishing.

Do not add the developer's local You.com key to this directory. Users who need paid tools should configure their own You.com MCP connection through an approved client credential mechanism; do not assume that doing so upgrades the bundled free connection.

## Release status

`0.1.0` is a development preview. Before public submission, confirm target Qoder client compatibility, publisher authorization, branding, MCP review policy, and whether a bundled MCP service needs a previously published Connector. Record a client-side self-test including authorization and errors. Only then submit a credential-free ZIP with `.qoder-plugin/`, `.mcp.json`, `skills/`, and this README at its root via [My extensions](https://qoder.com/account/apphub-publications). Review and public listing are separate steps.

See [research and competitive gap analysis](docs/RESEARCH.md) and [development guide](docs/DEVELOPMENT.md).
