# Development and release guide

## Current tree

```text
qoder-you/
├── .qoder-plugin/plugin.json
├── .mcp.json
├── skills/youcom-web-research/SKILL.md
├── skills/youcom-source-verification/SKILL.md
├── docs/CONTEXT.md
├── docs/DEVELOPMENT.md
├── docs/RESEARCH.md
└── README.md
```

The Skills and bundled keyless You.com MCP connection form an initial integrated draft, not a client-tested or marketplace-approved product. Keep the package free of API keys, tokens, passwords, user data, and internal company information. Store paid-tier credentials only in an approved local or platform-managed secret mechanism; never commit them or put them into the publishing ZIP.

## Development sequence

1. **Choose product and use cases.** Record target Qoder client/version, target users, concrete tasks, expected You.com endpoints, supported countries, and acceptable attribution. Make the Skills sufficiently specific to real workflows rather than a loose collection of unrelated commands.
2. **Validate the connection model.** Test the bundled keyless MCP connection in the target Qoder client; separately test authentication and authorization for any paid-tier plan using user-managed credentials. Confirm the publishing route for any MCP dependency. The Chinese guidelines say a Plugin's referenced Connector must be a valid published entry; do not assert that bundling an MCP service bypasses that rule.
3. **Implement minimum useful behavior.** Add only tools and permissions needed for the selected use cases. Handle missing credentials, request failures, timeouts, rate limits, and citations clearly. Do not claim You.com was used when it was not.
4. **Test in the target client.** Import the project into Qoder, check that both Skills load, exercise successful and failure cases, and verify citations against the actual sources. Document actual client/version, inputs, outputs, and limitations in a self-test report before submission.
5. **Package and review.** From the project directory, build a ZIP with `.qoder-plugin/` at the ZIP root, alongside `.mcp.json`, `skills/` and any other needed runtime resources; exclude `docs/`, development artifacts, and secrets unless required for runtime. Inspect the ZIP listing and validate JSON/frontmatter. Update all version mentions for each submission.
6. **Publish only when authorized.** Supply listing details, publisher attribution, permissions/account requirements, and review materials on Qoder 「我的发布」 → 「发布 Plugin」. A submitted ZIP is not public until it passes review. Track both review and listing status there.

## Acceptance criteria before submission

- An actual You.com connection works in the intended Qoder client and fails safely when unconfigured.
- A reviewer can reproduce every advertised capability with clear setup instructions and no embedded secret.
- Every bundled Skill has a unique lowercase hyphenated name, third-person trigger description, operational steps, safeguards, and verification guidance.
- The ZIP root includes `.qoder-plugin/plugin.json`; its manifest and every included resource are readable and consistent with the intended client.
- Publisher identity, service branding, third-party dependencies, data handling, and marketplace eligibility have been confirmed with the responsible parties.
- A self-test report covers expected calls, errors, permissions, availability, and any UI behavior actually provided. No unsupported integration or approval claim appears in the public listing.

## Reference material

See [CONTEXT.md](CONTEXT.md) for screenshot-derived publishing rules and links to official Qoder documentation. Verify any release-critical details against the live form before shipping.
