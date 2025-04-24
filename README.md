# MCP
Leverage the MCP in LLM
- MCP: Model Context Protocol

##
Workflow:<br>
sequenceDiagram<br>
  participant U as User<br>
  participant C as Client App<br>
  participant L as LLM (MCP Client)<br>
  participant S as MCP Server<br>

  U->>C: “Show my GitHub repos”<br>
  C->>L: User prompt<br>
  L-->>C: {"tool_call":"github.list_repos","args":{"user":"octocat"}}<br>
  C->>S: JSON-RPC → method=github.list_repos params={"user":"octocat"}  :contentReference[oaicite:0]{index=0}<br>
  S-->>C: JSON-RPC response: ["repo1","repo2","repo3"]  :contentReference[oaicite:1]{index=1}<br>
  C->>L: tool result<br>
  L-->>C: “Here are your repos: repo1, repo2, repo3.”<br>
  C->>U: Final answer<br>

> python mcp_server.py
MCP server listening on http://localhost:8000

> python llm_client.py
Here are octocat’s public repos:
 • octocat/repoA
 • octocat/repoB
 • octocat/repoC
