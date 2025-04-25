# MCP
Leverage the MCP in LLM
- MCP: Model Context Protocol

## Workflow:<br>
sequenceDiagram
    participant U as User
    participant C as client.py
    participant L as OpenAI LLM
    participant M as MCP Server

    U->>C: “Show me octocat’s GitHub repos”
    C->>L: ChatCompletion(functions=[…], function_call="auto")
    L-->>C: {function_call: "github.list_repos", arguments: {"user":"octocat"}}
    C->>M: MCP JSON-RPC “call_tool” via ClientSession.call_tool :contentReference[oaicite:4]{index=4}
    M-->>C: ["octocat/repoA",…]
    C->>L: ChatCompletion(messages including function response)
    L-->>C: “Here are your repos…”
    C->>U: Final answer

> python mcp_server.py
MCP server listening on http://localhost:8000

> python llm_client.py
Here are octocat’s public repos:
 • octocat/repoA
 • octocat/repoB
 • octocat/repoC

## How to run
> uv run --active bin/llm_client.py
