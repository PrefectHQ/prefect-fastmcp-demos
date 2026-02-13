from pathlib import Path

from fastmcp import FastMCP
from fastmcp.server.providers import FileSystemProvider

# Create a FastMCP server for the finance tools
mcp = FastMCP(
    providers=[
        FileSystemProvider(Path(__file__).parent / "mcp")
    ]
)

if __name__ == "__main__":
    mcp.run()
