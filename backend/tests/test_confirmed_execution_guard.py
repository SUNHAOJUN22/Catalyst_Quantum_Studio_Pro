from app.services.external_execution_guard import dry_run_execution_plan, has_shell_injection, has_unsafe_path, validate_confirmed_execution


def test_path_and_shell_injection_detection() -> None:
    assert has_unsafe_path("..\\outside\\g16.exe") is True
    assert has_shell_injection("g16 < input.gjf > output.log") is True
    assert has_shell_injection("g16 input.gjf") is False


def test_confirmed_execution_guard_blocks_default_environment() -> None:
    tool = {
        "tool_type": "gaussian16",
        "display_name": "Gaussian16",
        "executable_path": __file__,
        "can_execute": True,
    }
    job = {
        "execution_mode": "confirmed_execute",
        "will_execute": False,
        "command_template": "g16 < input.gjf > output.log",
        "input_files": ["input.gjf"],
        "output_files_expected": ["output.log"],
    }
    result = validate_confirmed_execution(tool, job, user_confirmed=True)
    assert result["allowed"] is False
    assert any("ENABLE_REAL_QC_EXECUTION" in reason for reason in result["reasons"])

    dry_run = dry_run_execution_plan(tool, job)
    assert dry_run["will_execute"] is False
    assert dry_run["status"] == "dry-run"
