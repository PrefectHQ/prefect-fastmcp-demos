# Prefect FastMCP Demos

This repository contains the source code of the Prefect Sales Engineering team's [FastMCP](https://gofastmcp.com) server demos.

## How to use

You can use this repository as a template for building your own FastMCP projects.

Feel free to:
- **Fork** it into your GitHub account
- **Clone** it and modify it as you like

This repository uses [Just](https://just.systems/) to automate tasks. All recipes are in the [`justfile`](justfile).

### Add a new FastMCP server project

To create a new FastMCP server, run:

```bash
just create-server <name>
```

This creates a directory at `servers/<name>` with the appropriate template files.

### Run the FastMCP server

To test your server locally, run:

```bash
just dev <name>
```

This starts the FastMCP server in development mode.

When you're ready to deploy, check out [FastMCP.cloud](https://fastmcp.cloud), a managed platform for hosting MCP servers that helps you move quickly from development to production!

## Dependency management

This repository uses [uv's workspace](https://docs.astral.sh/uv/concepts/projects/workspaces/) functionality to manage dependencies across multiple FastMCP server projects. Each server can have its own dependencies specified in its `pyproject.toml`, while shared dependencies can be managed at the workspace level.

Additionally, [`constraint-dependencies`](https://docs.astral.sh/uv/reference/settings/#constraint-dependencies) are defined at the workspace level to ensure a consistent version of shared libraries across all servers.

FastMCP.cloud installs dependencies using `uv pip install -r path/to/pyproject.toml`. Including the constraint at the workspace level ensures correct versions are used during server builds.

### How to set up a shared dependency

To add a workspace-level constraint, add the version to the `[tool.uv]` section in the root `pyproject.toml`:

```toml
[tool.uv]
constraint-dependencies = [
    "fastmcp==2.3.0",
    "your-dependency==x.y.z",
]
```

Then, in each server's `pyproject.toml`, you can include the dependency without specifying a version:

```bash
uv add --frozen --directory servers/<name> your-dependency
```

This ensures that all servers use the same version of `your-dependency` as specified in the workspace constraints.
