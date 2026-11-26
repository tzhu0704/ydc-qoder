# Qoder / You.com plugin research (2026-11-26)

## Findings and evidence

1. [Qoder plugin reference](https://docs.qoder.com/cli/plugins-reference) documents `.qoder-plugin/plugin.json`, bundled `skills/`, and plugin-root `.mcp.json` (with `mcp.json` fallback). [Qoder MCP reference](https://docs.qoder.com/cli/mcp-reference) supports `http` / `streamable-http` MCP transport and plugin-root MCP configs. These establish a local development shape, not marketplace approval.
2. [Qoder plugin publication](https://docs.qoder.com/developers/publishing/plugins) requires ZIP upload, listing metadata, MCP authentication/review details when applicable, a self-test report, and review. [Package an MCP service](https://docs.qoder.com/developers/plugins/package-mcp) describes an `mcp.json` referenced by a manifest; the CLI reference describes plugin-root `.mcp.json`. The precise accepted format must be validated against the *target client and publishing form*.
3. [Chinese marketplace guidelines](https://docs.qoder.com/zh/qoderwork/skill-marketplace-guidelines) say Plugin Connector dependencies must resolve to an already published Connector. This may conflict with the more general MCP-service-in-plugin publishing instructions. Ask Qoder which applies to this submission; do not claim bundled MCP bypasses Connector review.
4. [You.com MCP documentation](https://documentation.you.com/agents/mcp-server) specifies keyless `https://api.you.com/mcp/free`: `you-search`, `you-extract`, `you-discover`, 100 queries/day; free `you-extract` accepts only `url`. The authenticated `/mcp` endpoint supports OAuth 2.1 or bearer API key, and research/finance use dedicated paid endpoints. `you-contents` is deprecated in favor of `you-extract`.
5. [TinyFish's QoderWork announcement](https://www.tinyfish.ai/blog/tinyfish-connector-alibaba-qoderwork) describes an official Connector connected via OAuth in Settings → Connectors & MCP and advertises search, fetch, authenticated site interactions and browser automation. Its benchmark scores are vendor claims, not independently established comparisons here.
6. [Qwen Code extension docs](https://qwenlm.github.io/qwen-code-docs/en/users/extension/introduction/) say Qoder-format plugins can be installed and converted in Qwen Code. This is an optional compatibility test, not Qoder or Qwen marketplace publication.

## MCP interface validation (2026-11-26)

- The keyless `POST /mcp/free` accepted JSON-RPC `initialize` (protocol `2025-06-18`), and `tools/list` returned exactly `you-search`, `you-extract`, `you-discover`. Live `you-search` and single-URL `you-extract` returned results. Repeat with `python3 scripts/check_plugin.py --live` (no credential required). This proves remote MCP behavior, **not** Qoder plugin compatibility.
- With a separately supplied development credential (not stored in this repository), `tools/list` exposed `you-search`, `you-contents`, `you-extract`, `you-balance`, `you-discover` on `/mcp`, `you-research` alone on `/mcp/research`, and `you-finance` alone on `/mcp/finance`. No paid tool invocation or permission/billing check was performed; visibility is not proof of entitlement or result quality.
- A Python `urllib` request from this environment got Cloudflare 403 Error 1010; the same endpoint accepted `curl`'s user agent and completed the MCP exchange. Treat this as a client fingerprint restriction, not an outage. Test Qoder's own network stack separately; do not attempt to evade access controls.
- You.com docs describe `you-search` common parameters (`query`, `count`, `freshness`, `offset`, `extraction`, `knowledge`, `safesearch`, `extraction_source`, `crawl_timeout`, `exclude_domains`); host-only search overrides may be carried in JSON-RPC `_meta` or `X-Search-*` headers. The free `you-extract` request should contain only `url`. Paid research/finance endpoints have separate tool scopes; a free profile on those paths exposes no tools. `you-contents` remains available on authenticated `/mcp` but is deprecated.

## Product scope and gap

| User task | TinyFish public claim | This preview | Next step |
| --- | --- | --- | --- |
| Live web search | Yes | Bundled free You.com search; client untested | Validate client tool connection and response |
| Read pages | Yes | Bundled free single-URL `you-extract`; client untested | Validate HTML and PDF examples |
| Sourced briefing / verification | Web-agent sourcing claimed | Two task-specific Skills; quality not benchmarked | Evaluate citations and unsupported claims |
| One-click account sign-in | OAuth Connector | No sign-in needed for free tier; no paid sign-in path bundled | Work with Qoder on official OAuth Connector |
| Deep/finance research | Not asserted here | Not bundled | Separately scope paid endpoint and review |
| Logged-in browsing, clicks, forms | Yes | Not supported | Do not advertise parity without a separate product |

## Release gates

- Confirm Qoder IDE vs QoderWork vs CLI target and import/ZIP support; run `qoder plugins validate` where available.
- Test first-install MCP handshake, skill discovery, a full cited task, missing network, quota exhaustion, and any authorization UX in the actual target client.
- Obtain You.com publisher and branding authorization; establish Qoder Connector versus Plugin MCP acceptance and review materials. A developer key is not a distributable credential.
- Benchmark against TinyFish on matched public-web research cases: task completion, source URL validity, claim support, freshness, first useful result latency, and install success. Log environment and repeat trials; do not claim superiority before measurement.
- Submit only a reviewed, credential-free package and factual self-test report. No public submission has happened.
