---
name: youcom-source-verification
description: Checks public-web claims against You.com search results and original sources when the user asks to fact-check, verify a link, or compare conflicting reports.
version: 0.1.0
---

# Verify web claims

1. Extract each checkable claim and its claimed date. Distinguish factual assertions from predictions or opinions.
2. Use the bundled `youdotcom` MCP server's `you-search` tool for the original source and at least one independent corroborating or contradicting source. If it is unavailable or its quota is exhausted, state that You.com verification cannot be performed in this environment.
3. Use `you-extract` with only the `url` parameter to read primary sources; check the relevant passages, dates, geography, and scope. Do not infer a source's position from a snippet alone. If extraction fails, mark the claim unverified rather than fabricate evidence.
4. Report each claim as supported, contradicted, or not established, with direct source URLs and a short explanation. Keep unresolved conflicts visible.
5. Before responding, recheck that citations resolve and that evidence actually supports the stated verdict.

Do not enter API keys into prompts, examples, or published plugin files.
