from app.services.external_tool_registry import check_version_dry_run, tool_configuration_status


def test_unconfigured_external_tool_reports_missing() -> None:
    status = tool_configuration_status({"tool_type": "gaussian16", "executable_path": None})
    assert status["configured"] is False
    assert status["status"] == "missing"
    assert "当前未配置真实软件路径" in "；".join(status["warnings"])


def test_check_version_is_dry_run_by_default() -> None:
    result = check_version_dry_run({"tool_type": "multiwfn", "display_name": "Multiwfn", "executable_path": None})
    assert result["status"] == "skipped"
    assert result["can_run_version_check"] is False
    assert "默认不执行 version command" in "；".join(result["warnings"])
