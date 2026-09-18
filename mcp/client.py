import asyncio
import sys
from pathlib import Path

from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

PROJECT_ROOT = Path(__file__).resolve().parent.parent


async def call_tool(session: ClientSession, name: str, arguments: dict) -> None:
    print(f"\n> {name}({arguments})")

    result = await session.call_tool(name, arguments)

    for block in result.content:
        if block.type == "text":
            print(block.text)


async def main() -> None:
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["mcp/server.py"],
        cwd=str(PROJECT_ROOT),
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()

            print("Available tools:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")

            await call_tool(session, "get_order_status", {"order_id": 103})
            await call_tool(session, "get_order_status", {"order_id": 999})


if __name__ == "__main__":
    asyncio.run(main())
