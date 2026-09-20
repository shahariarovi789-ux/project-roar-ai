# tests/test_mcp_server.py
"""
Unit and integration tests for ROAR Model Context Protocol (MCP) Server and Adapter.
"""

import pytest
from mcp_server.client import mcp_client
from agents.mcp_adapter import MCPOrchestratorAdapter
from db.storage import create_account


@pytest.mark.asyncio
async def test_mcp_resources_list():
    resources = await mcp_client.list_resources()
    uris = [r["uri"] for r in resources]
    assert "roar://curriculum/dag" in uris
    assert "roar://hardware/profile" in uris


@pytest.mark.asyncio
async def test_mcp_read_dag_resource():
    dag = await mcp_client.read_resource("roar://curriculum/dag")
    assert isinstance(dag, dict)
    assert dag.get("total_nodes") == 36
    assert len(dag.get("nodes", [])) == 36


@pytest.mark.asyncio
async def test_mcp_read_node_resource():
    node = await mcp_client.read_resource("roar://curriculum/node/node_01")
    assert isinstance(node, dict)
    assert node.get("id") == "node_01"
    assert "Introduction to prompt engineering" in node.get("title", "")
    assert node.get("difficulty_tier") == 1


@pytest.mark.asyncio
async def test_mcp_tools_list():
    tools = await mcp_client.list_tools()
    tool_names = [t["name"] for t in tools]
    assert "retrieve_grounding_context" in tool_names
    assert "verify_node_unlocked" in tool_names
    assert "compute_socratic_hint" in tool_names
    assert "grade_prompt_submission" in tool_names
    assert "update_learner_progress" in tool_names


@pytest.mark.asyncio
async def test_mcp_tool_verify_unlocked():
    res = await mcp_client.call_tool("verify_node_unlocked", {
        "user_id": "test_mcp_user_verify",
        "node_id": "node_01"
    })
    assert isinstance(res, dict)
    assert res.get("node_id") == "node_01"
    assert res.get("unlocked") is True


@pytest.mark.asyncio
async def test_mcp_tool_retrieve_grounding():
    res = await mcp_client.call_tool("retrieve_grounding_context", {
        "topic": "Few-Shot Prompting",
        "n_results": 2
    })
    assert isinstance(res, dict)
    assert "chunks_retrieved" in res
    assert "grounding_text" in res


@pytest.mark.asyncio
async def test_mcp_tool_update_progress():
    user_id = "test_mcp_progress_user"
    try:
        await create_account(user_id, user_id, "test_hash")
    except Exception:
        pass

    res = await mcp_client.call_tool("update_learner_progress", {
        "user_id": user_id,
        "node_id": "node_01",
        "score": 0.95,
        "passed": True
    })
    assert isinstance(res, dict)
    assert res.get("user_id") == user_id
    assert res.get("passed") is True
    assert res.get("mastery_score") == 0.95
    assert res.get("completed_nodes_count") >= 1


@pytest.mark.asyncio
async def test_mcp_orchestrator_adapter_session():
    user_id = "test_mcp_adapter_user"
    try:
        await create_account(user_id, user_id, "test_hash")
    except Exception:
        pass

    session = await MCPOrchestratorAdapter.get_or_create_session(user_id)
    assert isinstance(session, dict)
    assert session.get("mcp_enabled") is True
    assert session.get("current_node", {}).get("id") is not None
