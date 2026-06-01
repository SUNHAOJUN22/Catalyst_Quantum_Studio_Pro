from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_mcp_simulation_guard_tools_are_registered() -> None:
    tools = client.get("/api/mcp/tools").json()["tools"]
    by_name = {tool["name"]: tool for tool in tools}
    for name in [
        "validate_external_tool",
        "dry_run_simulation_job",
        "confirm_simulation_job",
        "execute_confirmed_simulation_job",
        "generate_formchk_template",
        "generate_multiwfn_esp_template",
        "generate_goodvibes_template",
        "calculate_bde_roor",
    ]:
        assert name in by_name
        assert by_name[name]["can_execute_external"] is False


def test_mcp_external_tool_validation_does_not_execute() -> None:
    response = client.post(
        "/api/mcp/run-tool",
        json={"tool_name": "validate_external_tool", "arguments": {"tool_type": "gaussian16", "executable_path": "C:\\Tools\\g16.exe"}},
    )
    assert response.status_code == 200
    payload = response.json()["result"]
    assert payload["validation_status"] == "template-valid"
    assert "未执行 version command" in "；".join(payload["warnings"])
