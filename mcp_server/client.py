# mcp_server/client.py
"""
ROAR Model Context Protocol (MCP) Client.
Provides a high-performance in-memory and protocol-compliant client wrapper
for agents, the orchestrator, and automated benchmark harnesses.
"""

import json
from typing import Dict, Any, List, Optional
from mcp_server.server import mcp_server


class ROARMCPClient:
    """Client for communicating with the ROAR MCP Server.

    Supports direct in-process execution with full JSON-RPC schema validation,
    ensuring maximum speed while strictly enforcing the MCP protocol specification.
    """

    def __init__(self, server=None):
        self.server = server or mcp_server

    async def list_resources(self) -> List[Dict[str, Any]]:
        """Lists all resources exposed by the MCP Server."""
        resources = await self.server.list_resources()
        return [
            {
                "uri": str(r.uri),
                "name": r.name,
                "description": getattr(r, "description", None),
                "mime_type": getattr(r, "mime_type", "application/json")
            }
            for r in resources
        ]

    async def read_resource(self, uri: str) -> Any:
        """Reads and parses a resource from the MCP Server by URI."""
        contents = await self.server.read_resource(uri)
        if not contents:
            return None
        text_content = contents[0].content
        if isinstance(text_content, str):
            try:
                return json.loads(text_content)
            except json.JSONDecodeError:
                return text_content
        return text_content

    async def list_tools(self) -> List[Dict[str, Any]]:
        """Lists all tools available on the MCP Server along with their input schemas."""
        tools = await self.server.list_tools()
        return [
            {
                "name": t.name,
                "description": t.description,
                "input_schema": getattr(t, "input_schema", None) or getattr(t, "parameters", None)
            }
            for t in tools
        ]

    async def call_tool(self, tool_name: str, arguments: Optional[Dict[str, Any]] = None) -> Any:
        """Executes a tool on the MCP Server with strict argument validation."""
        args = arguments or {}
        result = await self.server.call_tool(tool_name, args)

        if getattr(result, "is_error", False):
            error_msg = result.content[0].text if result.content else "Unknown MCP error"
            raise RuntimeError(f"MCP Tool Execution Error ({tool_name}): {error_msg}")

        # Extract structured content or text
        if hasattr(result, "structured_content") and result.structured_content:
            return result.structured_content.get("result", result.structured_content)

        if hasattr(result, "content") and result.content:
            text = result.content[0].text
            try:
                return json.loads(text)
            except (json.JSONDecodeError, TypeError):
                return text

        return None


# Global singleton client
mcp_client = ROARMCPClient()
