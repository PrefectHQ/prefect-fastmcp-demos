[doc('Create a new MCP server'), no-exit-message]
create-server NAME: 
    uv init --bare servers/{{NAME}}
    uv add --frozen --directory servers/{{NAME}} fastmcp
    @cp .template/{fastmcp.json,main.py} servers/{{NAME}}/
    @echo "# {{NAME}} MCP Server Project\n\n🚀 Happy building!" > servers/{{NAME}}/README.md
    @uv sync
    @echo "🚀　MCP Server project '{{NAME}}' initialized."
    
[doc('Run MCP server in development mode'), no-exit-message]
dev NAME FILE='main.py':
    uv run --directory servers/{{NAME}} fastmcp dev inspector {{FILE}}