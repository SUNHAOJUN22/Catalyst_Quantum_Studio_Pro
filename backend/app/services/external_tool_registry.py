from __future__ import annotations

import os
from pathlib import Path
from typing import Any


ENV_BY_TOOL_TYPE: dict[str, str] = {
    "gaussian16": "GAUSSIAN16_PATH",
    "formchk": "FORMCHK_PATH",
    "cubegen": "CUBEGEN_PATH",
    "multiwfn": "MULTIWFN_PATH",
    "goodvibes": "GOODVIBES_PATH",
    "slurm": "SLURM_SBATCH_PATH",
}


def external_execution_enabled() -> bool:
    return os.getenv("ENABLE_REAL_QC_EXECUTION", "").strip() == "1"


def configured_path_for_tool(tool: dict[str, Any]) -> str | None:
    explicit = str(tool.get("executable_path") or "").strip()
    if explicit:
        return explicit
    env_name = ENV_BY_TOOL_TYPE.get(str(tool.get("tool_type") or ""))
    if not env_name:
        return None
    value = os.getenv(env_name, "").strip()
    return value or None


def tool_configuration_status(tool: dict[str, Any]) -> dict[str, Any]:
    path_value = configured_path_for_tool(tool)
    if not path_value:
        return {
            "configured": False,
            "path_exists": False,
            "env_var": ENV_BY_TOOL_TYPE.get(str(tool.get("tool_type") or "")),
            "status": "missing",
            "warnings": ["当前未配置真实软件路径。"],
        }

    path = Path(path_value)
    return {
        "configured": True,
        "path_exists": path.exists(),
        "env_var": ENV_BY_TOOL_TYPE.get(str(tool.get("tool_type") or "")),
        "status": "path-found" if path.exists() else "path-not-found",
        "warnings": [] if path.exists() else ["已登记路径，但当前文件不存在；不会执行外部程序。"],
    }


def check_version_dry_run(tool: dict[str, Any]) -> dict[str, Any]:
    status = tool_configuration_status(tool)
    return {
        "tool_type": tool.get("tool_type"),
        "display_name": tool.get("display_name"),
        "executable_path": configured_path_for_tool(tool),
        "can_run_version_check": bool(status["configured"] and status["path_exists"] and external_execution_enabled()),
        "execution_enabled": external_execution_enabled(),
        "status": "skipped",
        "warnings": [
            "默认不执行 version command；仅返回路径配置状态。",
            *status["warnings"],
        ],
        "provenance": "external_tool_registry.check_version_dry_run；未运行外部程序。",
    }
