from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class DocsMcpSettings(BaseSettings):
    """Docs MCP proxy settings."""

    model_config = SettingsConfigDict(
        env_prefix="PREFECT_DOCS_MCP_", extra="ignore", env_file=".env"
    )

    url: str = Field(
        default="https://prefect-docs.fastmcp.app/mcp",
        description="URL for the Prefect docs MCP server to proxy",
    )

    init_timeout: float = Field(
        default=10.0,
        description="Timeout in seconds for initializing the docs proxy connection",
    )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="PREFECT_DOCS_MCP_",
        extra="ignore",
        env_file=".env"
    )
    
    docs: DocsMcpSettings = Field(
        default_factory=DocsMcpSettings,
        description="Prefect Documentation MCP proxy settings",
    )
    
    
settings = Settings()