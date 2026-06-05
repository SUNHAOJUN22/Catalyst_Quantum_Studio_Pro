from __future__ import annotations

import re
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

from app.services.external_tool_registry import external_execution_enabled, tool_configuration_status


SHELL_META_PATTERN = re.compile(r"[;&|`$<>]")


def has_unsafe_path(value: str | None) -> bool:
    if not value:
        return False
    if "\x00" in value or ".." in value:
        return True
    return False


def has_shell_injection(value: str | None) -> bool:
    if not value:
        return False
    return bool(SHELL_META_PATTERN.search(value))


def safe_path_note(value: str | None) -> str | None:
    if has_unsafe_path(value):
        return "检测到非法路径。"
    return None


def validate_confirmed_execution(tool: dict[str, Any] | None, job: dict[str, Any], user_confirmed: bool) -> dict[str, Any]:
    reasons: list[str] = []
    warnings: list[str] = []
    if not external_execution_enabled():
        reasons.append("环境变量 ENABLE_REAL_QC_EXECUTION 未设置为 1，禁止真实执行。")

    if tool is None:
        reasons.append("缺少科学计算工具配置。")
        tool_status = {"configured": False, "path_exists": False, "warnings": ["未找到工具配置。"]}
    else:
        tool_status = tool_configuration_status(tool)
        warnings.extend(tool_status["warnings"])
        if not tool_status["configured"]:
            reasons.append("未配置工具路径。")
        if not tool_status["path_exists"]:
            reasons.append("工具路径不存在。")
        if not bool(tool.get("can_execute")):
            reasons.append("当前工具未开启 confirmed_execute。")

    if str(job.get("execution_mode") or "") != "confirmed_execute":
        reasons.append("当前任务不是 confirmed_execute 模式。")
    if not user_confirmed:
        reasons.append("缺少用户二次确认。")
    if bool(job.get("will_execute")):
        warnings.append("任务记录曾被标记 will_execute=true；执行前仍需重新校验。")

    command_template = str(job.get("command_template") or "")
    if has_shell_injection(command_template):
        reasons.append("命令模板包含 shell 重定向或控制符；必须转换为经过校验的参数数组，禁止直接执行。")

    for value in [*(job.get("input_files") or []), *(job.get("output_files_expected") or [])]:
        path_warning = safe_path_note(str(value))
        if path_warning:
            reasons.append(path_warning)
            break

    allowed = not reasons
    return {
        "allowed": allowed,
        "reasons": reasons,
        "warnings": warnings,
        "tool_status": tool_status,
        "execution_enabled": external_execution_enabled(),
        "safety_boundary": "真实执行必须通过路径配置、confirmed_execute、用户二次确认和安全参数校验。",
    }


def dry_run_execution_plan(tool: dict[str, Any] | None, job: dict[str, Any]) -> dict[str, Any]:
    validation = validate_confirmed_execution(tool, job, user_confirmed=False)
    return {
        "status": "dry-run",
        "will_execute": False,
        "command_template": job.get("command_template"),
        "generated_text_preview": (job.get("generated_text") or "")[:2000],
        "validation": validation,
        "provenance": "dry-run 只返回执行计划和拒绝/放行条件；未运行外部程序。",
    }
