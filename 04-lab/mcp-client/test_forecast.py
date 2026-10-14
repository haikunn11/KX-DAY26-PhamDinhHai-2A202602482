"""Script kiểm tra gọi trực tiếp tool get_forecast từ MCP Server (Lab 04)."""
import asyncio
import os
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from mcp import ClientSession
from mcp.client.streamable_http import create_mcp_http_client, streamable_http_client

SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8085/mcp")


async def main():
    print(f"📡 Đang kết nối tới MCP Server tại {SERVER_URL}...")
    client = create_mcp_http_client()
    async with client:
        try:
            async with streamable_http_client(SERVER_URL, http_client=client) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    print("✅ Kết nối thành công!")

                    tools = await session.list_tools()
                    print(f"🔧 Các tool khả dụng: {[t.name for t in tools.tools]}")

                    for city in ["Hanoi", "Danang"]:
                        print(f"\n🔮 Đang gọi get_forecast('{city}', days=3)...")
                        result = await session.call_tool("get_forecast", {"city": city, "days": 3})
                        print(result.content[0].text)
        except Exception as e:
            print(f"\n❌ Lỗi kết nối tới MCP Server: {e}")
            print("👉 Hãy chắc chắn bạn đã khởi động server: cd 04-lab/mcp-server && python weather.py")


if __name__ == "__main__":
    asyncio.run(main())
