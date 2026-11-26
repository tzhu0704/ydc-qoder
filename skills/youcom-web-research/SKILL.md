---
name: youcom-web-research
description: Researches current public-web topics with You.com when the user asks for recent information, competitive research, documentation lookup, or a sourced briefing.
version: 0.1.0
---

# You.com web research

Use this workflow for current public information, not for private account data.

1. Restate the research question and identify the date range, geography, and source types that matter. Ask one clarifying question only if the ambiguity changes the answer materially.
2. Use the bundled `youdotcom` MCP server's `you-search` tool for several distinct queries. For a known URL, use `you-extract` with the required `url` argument only; the free profile does not accept extraction tuning. `you-discover` can help select a You.com API, but does not itself answer the research question. If these tools are unavailable or the daily free quota is exhausted, say so; do not claim You.com results or silently substitute another provider.
3. Extract relevant primary-source pages with `you-extract`. Compare dates and distinguish first-hand evidence from commentary. Do not treat search snippets as proof of a detailed claim. If extraction fails, identify the source as unverified rather than inventing its contents.
4. Write a concise answer with links beside material claims. Include publication dates when timeliness matters, label uncertainty, and separate source claims from your inference.
5. Verify that every cited URL supports its associated claim and that no credential, internal document, or user-private data appears in the output.

The bundled free MCP endpoint needs no API key and provides search, extraction, and discovery, subject to the provider's free-use limits. It does not provide `you-research`, finance research, logged-in browsing, or browser actions. Do not submit private data to public-web search without user authorization.
