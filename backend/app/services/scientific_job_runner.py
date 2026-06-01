from __future__ import annotations

from typing import Any

from app.services.external_execution_guard import dry_run_execution_plan, validate_confirmed_execution


def build_dry_run_result(tool: dict[str, Any] | None, job: dict[str, Any]) -> dict[str, Any]:
    return dry_run_execution_plan(tool, job)


def confirm_job_for_execution(job: dict[str, Any], user_confirmed: bool, confirmation_phrase: str | None = None) -> dict[str, Any]:
    if not user_confirmed:
        return {
            "confirmed": False,
            "status": "blocked",
            "detail": "缺少用户二次确认，不能进入 confirmed_execute。",
        }
    expected = "我确认执行真实科学计算"
    if confirmation_phrase and confirmation_phrase != expected:
        return {
            "confirmed": False,
            "status": "blocked",
            "detail": f"确认短语不匹配。请使用：{expected}",
        }
    return {
        "confirmed": True,
        "status": "confirmed",
        "detail": "任务已记录二次确认；执行前仍会重新校验工具路径和 ENABLE_REAL_QC_EXECUTION。",
    }


def execute_confirmed_job(tool: dict[str, Any] | None, job: dict[str, Any], user_confirmed: bool) -> dict[str, Any]:
    validation = validate_confirmed_execution(tool, job, user_confirmed=user_confirmed)
    if not validation["allowed"]:
        return {
            "status": "blocked",
            "will_execute": False,
            "validation": validation,
            "detail": "真实科学计算执行已被安全守卫拦截。",
        }
    return {
        "status": "ready-but-not-run",
        "will_execute": False,
        "validation": validation,
        "detail": "安全条件已满足，但当前实现仍要求外部 runner 单独接管；API 不直接运行 Gaussian/cubegen/Multiwfn。",
    }
