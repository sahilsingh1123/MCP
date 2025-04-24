# server.py
from mcp.server import FastMCP
import json

mcp = FastMCP("GitHub")


# 1) Define your tool methods
@mcp.tool(name="list_repos", description="List public GitHub repos for a user")
def _impl_list_repos(user: str) -> dict:
    return {"repos": [f"{user}/repoA", f"{user}/repoB", f"{user}/repoC"]}


if __name__ == "__main__":
    print("MCP server listening on http://localhost:8000")
    mcp.run()
