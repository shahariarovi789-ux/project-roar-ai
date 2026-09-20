# mcp_server/__init__.py
"""
Model Context Protocol (MCP) Server and Client Package for Project ROAR.
Standardizes multi-agent context, knowledge resources, and educational tools.
"""

from mcp_server.server import mcp_server, create_roar_mcp_server
from mcp_server.client import ROARMCPClient

__all__ = ["mcp_server", "create_roar_mcp_server", "ROARMCPClient"]
