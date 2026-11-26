#!/usr/bin/env python3
"""Check the distributable plugin files; optional live test uses the free MCP only."""

import argparse
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
EXPECTED_TOOLS = {"you-search", "you-extract", "you-discover"}


def check_files():
    manifest = json.loads((ROOT / ".qoder-plugin/plugin.json").read_text())
    config_path = (ROOT / manifest["mcpServers"]).resolve()
    if not config_path.is_relative_to(ROOT) or not config_path.is_file():
        raise ValueError("MCP configuration must resolve inside the plugin")
    config = json.loads(config_path.read_text())
    server = config["mcpServers"]["youdotcom"]
    assert server == {"type": "http", "url": "https://api.you.com/mcp/free"}
    assert (ROOT / manifest["skills"]).is_dir()
    skills = sorted((ROOT / "skills").glob("*/SKILL.md"))
    assert skills, "No skills found"
    for skill in skills:
        text = skill.read_text()
        assert text.startswith("---\n")
        header = text.split("---", 2)[1]
        assert re.search(r"^name: " + re.escape(skill.parent.name) + r"$", header, re.M)
        assert re.search(r"^description: .+", header, re.M)
    print("PASS: manifest, MCP config, skill metadata ({} skills)".format(len(skills)))


def rpc(method, params):
    payload = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params})
    run = subprocess.run(
        ["curl", "--fail-with-body", "--silent", "--show-error", "--max-time", "20",
         "-X", "POST", "https://api.you.com/mcp/free",
         "-H", "Content-Type: application/json",
         "-H", "Accept: application/json, text/event-stream",
         "--data-binary", payload],
        capture_output=True, text=True, timeout=25, check=True,
    )
    events = [json.loads(line.removeprefix("data: ")) for line in run.stdout.splitlines()
              if line.startswith("data: ")]
    if not events:
        raise ValueError("No MCP JSON-RPC response")
    for event in events:
        if "error" in event:
            raise ValueError("MCP error: {}".format(event["error"].get("message", "unknown")))
    return events


def check_live():
    init = rpc("initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                              "clientInfo": {"name": "qoder-you-check", "version": "0.1.0"}})
    assert any("serverInfo" in event.get("result", {}) for event in init)
    tools = {tool["name"] for event in rpc("tools/list", {})
             for tool in event.get("result", {}).get("tools", [])}
    assert tools == EXPECTED_TOOLS, "Unexpected free tools: {}".format(sorted(tools))
    print("PASS: free MCP initialize + tools/list ({})".format(", ".join(sorted(tools))))
    # A single representative call; no private queries or credentials are transmitted.
    results = rpc("tools/call", {"name": "you-search", "arguments":
                                   {"query": "site:you.com/docs MCP server You.com", "count": 1}})
    text = " ".join(item.get("text", "") for event in results
                    for item in event.get("result", {}).get("content", []))
    assert "you.com" in text.lower(), "Search result did not contain an expected source"
    print("PASS: free MCP you-search returned a You.com source")
    extracted = rpc("tools/call", {"name": "you-extract", "arguments":
                                      {"url": "https://you.com/docs/agents/mcp-server"}})
    content = " ".join(item.get("text", "") for event in extracted
                       for item in event.get("result", {}).get("content", []))
    assert "MCP Server" in content, "Extraction did not return expected documentation text"
    print("PASS: free MCP you-extract returned documentation content")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="also call the public free You.com MCP")
    options = parser.parse_args()
    check_files()
    if options.live:
        check_live()
