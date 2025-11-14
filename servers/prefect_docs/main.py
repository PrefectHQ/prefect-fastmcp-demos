from fastmcp import FastMCP
from fastmcp.server.proxy import ProxyClient
from settings import settings

# Mount the Prefect docs MCP server to expose its tools
mcp = FastMCP.as_proxy(
    ProxyClient(settings.docs.url, init_timeout=settings.docs.init_timeout),
    name="Prefect Documentation Search",
)

if __name__ == "__main__":
    mcp.run()