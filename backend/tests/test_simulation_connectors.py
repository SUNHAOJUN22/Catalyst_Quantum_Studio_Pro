from fastapi.testclient import TestClient
import sys

from app.main import app


client = TestClient(app)


def test_simulation_tool_registry_defaults_are_non_executable() -> None:
    response = client.get("/api/simulation/tools")
    assert response.status_code == 200
    payload = response.json()
    assert "不执行 Gaussian" in payload["safety_boundary"]
    assert payload["tools"]
    assert all(tool["can_execute"] is False for tool in payload["tools"] if tool["id"] < 0)
    assert any(tool["tool_type"] == "gaussian16" for tool in payload["tools"])


def test_create_and_validate_simulation_tool_does_not_execute_version_command() -> None:
    response = client.post(
        "/api/simulation/tools",
        json={
            "tool_type": "multiwfn",
            "display_name": "Multiwfn 模板",
            "executable_path": "C:\\Tools\\Multiwfn\\Multiwfn.exe",
            "working_directory": "D:\\safe-work",
            "default_mode": "template_only",
            "allowed_extensions": [".fchk", ".cube", ".txt"],
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["tool"]["can_execute"] is False
    assert payload["validation"]["validation_status"] == "template-valid"
    assert "未执行 version command" in "；".join(payload["validation"]["warnings"])

    validation = client.post(f"/api/simulation/tools/{payload['tool']['id']}/validate-template")
    assert validation.status_code == 200
    assert "不执行 Gaussian" in validation.json()["validation"]["safety_note"]


def test_simulation_tool_rejects_path_traversal_with_chinese_error() -> None:
    response = client.post(
        "/api/simulation/tools",
        json={
            "tool_type": "gaussian16",
            "display_name": "非法路径测试",
            "executable_path": "..\\Gaussian\\g16.exe",
            "default_mode": "template_only",
        },
    )
    assert response.status_code == 400
    assert "检测到非法路径" in response.json()["detail"]


def test_simulation_job_builder_generates_templates_without_execution() -> None:
    response = client.post(
        "/api/simulation/jobs",
        json={"tool_type": "cubegen", "job_type": "cubegen_esp", "molecule_name": "MCSOMe"},
    )
    assert response.status_code == 200
    payload = response.json()
    job = payload["job"]
    assert job["will_execute"] is False
    assert job["evidence_grade"] == "D"
    assert "cubegen" in job["command_template"]
    assert "未运行外部科学计算程序" in payload["safety_boundary"]

    ready = client.post(f"/api/simulation/jobs/{job['id']}/mark-ready")
    assert ready.status_code == 200
    assert ready.json()["job"]["will_execute"] is False


def test_confirmed_execution_guard_blocks_without_env_and_confirmation() -> None:
    tool_response = client.post(
        "/api/simulation/tools",
        json={
            "tool_type": "gaussian16",
            "display_name": "Gaussian confirmed guard",
            "executable_path": sys.executable,
            "default_mode": "confirmed_execute",
        },
    )
    assert tool_response.status_code == 200
    tool = tool_response.json()["tool"]
    assert tool["can_execute"] is True

    version = client.post(f"/api/simulation/tools/{tool['id']}/check-version")
    assert version.status_code == 200
    assert version.json()["version_check"]["status"] == "skipped"
    assert version.json()["version_check"]["can_run_version_check"] is False

    job_response = client.post(
        "/api/simulation/jobs",
        json={
            "tool_id": tool["id"],
            "tool_type": "gaussian16",
            "job_type": "gaussian_input",
            "execution_mode": "confirmed_execute",
            "molecule_name": "MCSOMe",
        },
    )
    assert job_response.status_code == 200
    job = job_response.json()["job"]

    dry_run = client.post(f"/api/simulation/jobs/{job['id']}/dry-run")
    assert dry_run.status_code == 200
    assert dry_run.json()["dry_run"]["will_execute"] is False
    assert "ENABLE_REAL_QC_EXECUTION" in "；".join(dry_run.json()["dry_run"]["validation"]["reasons"])

    blocked = client.post(f"/api/simulation/jobs/{job['id']}/execute", json={"user_confirmed": False})
    assert blocked.status_code == 400
    assert "缺少用户二次确认" in str(blocked.json()["detail"])

    confirm = client.post(f"/api/simulation/jobs/{job['id']}/confirm", json={"user_confirmed": True})
    assert confirm.status_code == 200
    assert confirm.json()["job"]["will_execute"] is False

    still_blocked = client.post(f"/api/simulation/jobs/{job['id']}/execute", json={"user_confirmed": True})
    assert still_blocked.status_code == 400
    assert "ENABLE_REAL_QC_EXECUTION" in str(still_blocked.json()["detail"])


def test_simulation_read_only_parsers_keep_quality_and_evidence_boundaries() -> None:
    nbo = client.post(
        "/api/simulation/parse/nbo",
        json={"file_name": "nbo.txt", "text": "n(O)->Ti E(2)=18.2 gap=0.31 Fock=0.08"},
    )
    assert nbo.status_code == 200
    assert nbo.json()["quality"] == "partial"
    assert nbo.json()["evidence_grade"] == "C"
    assert nbo.json()["eligible_evidence_grade"] == "A"
    assert nbo.json()["paper_ready"] is False

    empty = client.post("/api/simulation/parse/goodvibes", json={"file_name": "empty.out", "text": ""})
    assert empty.status_code == 200
    assert empty.json()["quality"] == "failed"
    assert empty.json()["evidence_grade"] == "D"
    assert empty.json()["warnings"]


def test_mcp_tools_expose_simulation_connector_capabilities() -> None:
    tools = client.get("/api/mcp/tools").json()["tools"]
    names = {tool["name"] for tool in tools}
    expected = {
        "generate_cubegen_template",
        "generate_formchk_template",
        "generate_multiwfn_qtaim_template",
        "generate_multiwfn_nci_template",
        "generate_multiwfn_esp_template",
        "generate_goodvibes_parse_task",
        "generate_goodvibes_template",
        "generate_slurm_script_template",
        "parse_nbo",
        "parse_qtaim",
        "parse_nci",
        "parse_goodvibes",
        "calculate_insert_barrier",
        "calculate_bde_sio",
        "calculate_bde_roor",
        "calculate_radical_kinetics",
        "validate_external_tool",
        "dry_run_simulation_job",
        "confirm_simulation_job",
        "execute_confirmed_simulation_job",
        "generate_chinese_report",
    }
    assert expected.issubset(names)
    for tool in tools:
        if tool["name"] in expected:
            assert tool["can_execute_external"] is False

    forbidden = client.post("/api/mcp/run-tool", json={"tool_name": "execute-gaussian", "arguments": {}})
    assert forbidden.status_code == 400
    assert "安全白名单" in forbidden.json()["detail"]

    template = client.post("/api/mcp/run-tool", json={"tool_name": "generate-cubegen-template", "arguments": {"template_type": "esp"}})
    assert template.status_code == 200
    assert template.json()["result"]["will_execute"] is False

    validation = client.post("/api/mcp/run-tool", json={"tool_name": "validate_external_tool", "arguments": {"tool_type": "gaussian16", "executable_path": "..\\bad.exe"}})
    assert validation.status_code == 200
    assert validation.json()["result"]["validation_status"] == "invalid-path"
