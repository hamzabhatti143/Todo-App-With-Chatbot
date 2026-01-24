"""
MCP Server Initialization and Startup

This module initializes the FastMCP server, configures transport, and starts the server.
Supports both stdio (development) and HTTP (production) transports.
"""

import os
from app.mcp_server.tools import mcp


def main():
    """
    Start MCP server with configured transport.

    Environment Variables:
        MCP_TRANSPORT: Transport type - "stdio" or "http" (default: "http")
        MCP_PORT: Port for HTTP transport (default: 8001)
        MCP_HOST: Host for HTTP transport (default: "0.0.0.0")
    """
    transport = os.getenv("MCP_TRANSPORT", "http")

    if transport == "stdio":
        # Development mode: stdio transport for local testing
        print("Starting MCP server with stdio transport...")
        mcp.run(transport="stdio")
    else:
        # Production mode: HTTP transport
        host = os.getenv("MCP_HOST", "0.0.0.0")
        port = int(os.getenv("MCP_PORT", "8001"))

        print(f"Starting MCP server on {host}:{port}...")
        mcp.run(
            transport="streamable-http",
            json_response=True,  # Optimize for performance
            host=host,
            port=port
        )


if __name__ == "__main__":
    main()
