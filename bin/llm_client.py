# client.py
import json
from openai import OpenAI
import os
import asyncio
from dotenv import load_dotenv
from mcp import (
    ClientSession,
    StdioServerParameters,
)  # high-level client API :contentReference[oaicite:5]{index=5}
from mcp.client.stdio import (
    stdio_client,
)  # STDIO transport helper :contentReference[oaicite:6]{index=6}

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")


# A) Define “function” spec for OpenAI (unchanged)
client = OpenAI()
functions = [
    {
        "name": "list_repos",
        "description": "List public GitHub repos for a user",
        "parameters": {
            "type": "object",
            "properties": {"user": {"type": "string"}},
            "required": ["user"],
        },
    }
]


async def main():
    # —––– connect to MCP server over stdio
    server_params = StdioServerParameters(
        command="python",
        args=["/Users/sahilsingh/coding/github_codes/MCP/bin/mcp_server.py"],
        env=None,
    )

    async with stdio_client(server_params) as (r, w):
        async with ClientSession(r, w) as session:
            await session.initialize()
            # messages = [
            #     {
            #         "role": "system",
            #         "content": (
            #             "You are an AI assistant with access to a tool "
            #             "called list_repos(user) that returns a user’s GitHub repositories. "
            #             "Whenever a user asks for GitHub repositories, call that tool."
            #         ),
            #     },
            #     {"role": "user", "content": "Show me octocat’s GitHub repos"},
            # ]
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are an AI assistant with access to a tool "
                    ),
                },
                {"role": "user", "content": "Show me octocat’s GitHub repos"},
            ]

            # 4) Ask the LLM
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                functions=functions,
                function_call="auto",
            )
            msg = resp.choices[0].message

            # 5) If LLM wants to call our tool…
            if msg.function_call is not None:
                fname = msg.function_call.name  # "list_repos"
                args = json.loads(msg.function_call.arguments)
                print(f"fname and args = {fname}({args})")

                # 6) Map to the actual MCP method "github.list_repos"
                #     (server_name.method_name)
                result = await session.call_tool(
                    f"{fname}", args  # ← yields "GitHub.list_repos"
                )
                json_str = result.model_dump_json()
                print("json_str", json_str)

                # 7) Feed result back into the LLM
                follow = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "user",
                            "content": "Show me octocat’s GitHub repos",
                        },
                        msg,
                        {
                            "role": "function",
                            "name": fname,
                            "content": json_str,
                        },
                    ],
                )
                print(follow.choices[0].message.content)
            else:
                print(msg.content)


if __name__ == "__main__":
    asyncio.run(main())
