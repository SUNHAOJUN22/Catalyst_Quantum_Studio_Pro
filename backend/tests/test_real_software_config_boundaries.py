from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_readme_declares_external_execution_boundary() -> None:
    text = (Path(__file__).resolve().parents[2] / "README.md").read_text(encoding="utf-8")
    for phrase in ["不执行 Gaussian", "不执行 cubegen", "不执行 Multiwfn", "不执行 GoodVibes"]:
        assert phrase in text


def test_api_execute_endpoint_rejects_without_real_execution_env() -> None:
    tool = client.post(
        "/api/simulation/tools",
        json={
            "tool_type": "gaussian16",
            "display_name": "真实执行边界测试",
            "executable_path": __file__,
            "default_mode": "confirmed_execute",
        },
    ).json()["tool"]
    job = client.post(
        "/api/simulation/jobs",
        json={
            "tool_id": tool["id"],
            "tool_type": "gaussian16",
            "job_type": "gaussian_input",
            "execution_mode": "confirmed_execute",
        },
    ).json()["job"]
    response = client.post(f"/api/simulation/jobs/{job['id']}/execute", json={"user_confirmed": True})
    assert response.status_code == 400
    assert "ENABLE_REAL_QC_EXECUTION" in str(response.json()["detail"])
