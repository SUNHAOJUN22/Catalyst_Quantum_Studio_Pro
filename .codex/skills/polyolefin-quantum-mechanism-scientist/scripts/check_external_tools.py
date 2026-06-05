from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass


ENVIRONMENTS = {
    "Gaussian16": "GAUSSIAN16_PATH",
    "formchk": "FORMCHK_PATH",
    "cubegen": "CUBEGEN_PATH",
    "Multiwfn": "MULTIWFN_PATH",
    "GoodVibes": "GOODVIBES_PATH",
    "SLURM sbatch": "SLURM_SBATCH_PATH",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect scientific software paths without executing them.")
    parser.add_argument("--project", default=".", help="Project root used only for context.")
    args = parser.parse_args()
    project = Path(args.project).expanduser().resolve()
    print(f"项目：{project}")
    print("安全边界：只检查环境变量和路径是否存在，不执行 version command 或科学软件。")
    configured = 0
    for title, env_name in ENVIRONMENTS.items():
        raw = os.getenv(env_name, "").strip()
        if not raw:
            print(f"[MISSING] {title}: {env_name} 未配置")
            continue
        path = Path(raw).expanduser()
        exists = path.exists()
        configured += int(exists)
        print(f"[{'FOUND' if exists else 'INVALID'}] {title}: {path}")
    enabled = os.getenv("ENABLE_REAL_QC_EXECUTION", "").strip() == "1"
    print(f"ENABLE_REAL_QC_EXECUTION={'1' if enabled else '0/未配置'}")
    print(f"有效工具路径：{configured}/{len(ENVIRONMENTS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
