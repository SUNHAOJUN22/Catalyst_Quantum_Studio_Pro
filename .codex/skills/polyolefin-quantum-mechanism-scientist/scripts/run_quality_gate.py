from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass


COMMANDS = [
    ("中文乱码审计", "npm run audit:mojibake", ["package.json"]),
    ("后端单元测试", "npm run test:backend", ["package.json"]),
    ("项目质量门禁", "python scripts\\quality_gate.py", ["scripts/quality_gate.py"]),
    ("前端 TypeScript 检查", "npm --prefix frontend run typecheck", ["frontend/package.json"]),
    ("前端 ESLint", "npm --prefix frontend run lint", ["frontend/package.json"]),
    ("前端生产构建", "npm --prefix frontend run build", ["frontend/package.json"]),
    ("Playwright UI 烟测", "npm run test:e2e", ["package.json"]),
]

QUICK_NAMES = {
    "中文乱码审计",
    "后端单元测试",
    "前端 TypeScript 检查",
    "前端 ESLint",
    "前端生产构建",
}


def exists_any(project: Path, required: list[str]) -> bool:
    return any((project / item).exists() for item in required)


def run_command(command: str, project: Path) -> int:
    env = os.environ.copy()
    env.setdefault("PYTHONUTF8", "1")
    env.setdefault("PYTHONIOENCODING", "utf-8")
    result = subprocess.run(
        command,
        cwd=project,
        shell=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result.returncode


def npm_script_exists(project: Path, command: str) -> bool:
    package_json = project / "package.json"
    if not package_json.exists() or not command.startswith("npm run "):
        return True
    script = command.split("npm run ", 1)[1].split()[0]
    try:
        text = package_json.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return True
    return f'"{script}"' in text


def main() -> int:
    parser = argparse.ArgumentParser(description="Run available quality gates for a research software project.")
    parser.add_argument("--project", required=True, help="Project root directory.")
    parser.add_argument("--quick", action="store_true", help="Run a reduced validation set.")
    args = parser.parse_args()

    project = Path(args.project).expanduser().resolve()
    if not project.exists():
        print(f"[FAIL] 项目目录不存在：{project}", file=sys.stderr)
        return 2

    commands = [item for item in COMMANDS if not args.quick or item[0] in QUICK_NAMES]
    failed = 0
    skipped = 0
    passed = 0

    for name, command, required in commands:
        print("=" * 72)
        if not exists_any(project, required):
            skipped += 1
            print(f"[SKIP] {name}：未发现所需文件 {', '.join(required)}")
            continue
        if not npm_script_exists(project, command):
            skipped += 1
            print(f"[SKIP] {name}：package.json 中未定义对应 npm script")
            continue
        print(f"[RUN] {name}: {command}")
        code = run_command(command, project)
        if code == 0:
            passed += 1
            print(f"[PASS] {name}")
        else:
            failed += 1
            print(f"[FAIL] {name}")
            break

    print("=" * 72)
    print(f"质量门禁总结：PASS={passed} FAIL={failed} SKIP={skipped}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
