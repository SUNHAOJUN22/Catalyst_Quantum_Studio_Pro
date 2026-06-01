from __future__ import annotations

from pathlib import Path
from typing import Any


def expected_output_status(expected_files: list[str], working_directory: str | None = None) -> dict[str, Any]:
    base = Path(working_directory) if working_directory else None
    rows: list[dict[str, Any]] = []
    for file_name in expected_files:
        path = Path(file_name)
        check_path = base / path if base and not path.is_absolute() else path
        rows.append(
            {
                "file": file_name,
                "exists": check_path.exists(),
                "path_checked": str(check_path),
            }
        )
    return {
        "outputs": rows,
        "provenance": "只检查预期输出路径是否存在，不读取或执行文件。",
    }
