from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass


TEXT_SUFFIXES = {
    ".py",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".mjs",
    ".json",
    ".md",
    ".txt",
    ".css",
    ".html",
    ".yml",
    ".yaml",
    ".toml",
    ".csv",
    ".gjf",
    ".com",
}

EXCLUDED_PARTS = {
    ".git",
    ".next",
    ".venv",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    ".pytest_cache",
}

DEFAULT_ARCHIVE_PREFIXES = (
    "archive/",
    "legacy/",
    "vendor/",
    "integrated/origin-",
    "docs/merged-from-",
)

MOJIBAKE_MARKS = [
    "\u00c3",
    "\u00c2",
    "\u00e2",
    "\u00e5",
    "\u00e7",
    "\u00e6",
    "\u00e4",
    "\u00e9",
    "\u00e8",
    "\u00ee",
    "\u00ef",
    "\u00f0",
    "\u00fe",
    "\u00ce",
    "\u00cf",
    "\u00d0",
    "\u93c2",
    "\u7481",
    "\u7ec0",
    "\u59dd",
    "\u5bee",
    "\u9359",
    "\u93bb",
    "\u935a",
    "\u9422",
    "\u9428",
    "\u4e36",
    "\u934f",
    "\u9225",
    "\u922b",
    "\u8796",
    "\u87fa",
    "\u811c",
    "\u9983",
    "\ufffd",
]

MOJIBAKE_RE = re.compile("(" + "|".join(re.escape(mark) for mark in MOJIBAKE_MARKS) + ")")


@dataclass(frozen=True)
class Finding:
    path: Path
    line_no: int
    snippet: str
    archived: bool


def is_text_candidate(path: Path, project: Path) -> bool:
    rel = path.relative_to(project).as_posix()
    if rel == "docs/MOJIBAKE_CLEANUP_REPORT.md":
        return False
    if path.name == "mojibake_audit.py":
        return False
    if path.name in EXCLUDED_PARTS:
        return False
    if any(part in EXCLUDED_PARTS for part in path.parts):
        return False
    return path.suffix.lower() in TEXT_SUFFIXES


def is_archived(path: Path, project: Path, archive_prefixes: tuple[str, ...]) -> bool:
    rel = path.relative_to(project).as_posix()
    return rel.startswith(archive_prefixes)


def scan_file(path: Path, project: Path, archive_prefixes: tuple[str, ...]) -> list[Finding]:
    findings: list[Finding] = []
    archived = is_archived(path, project, archive_prefixes)
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return findings
    for line_no, line in enumerate(text.splitlines(), start=1):
        if MOJIBAKE_RE.search(line):
            snippet = line.strip()
            if len(snippet) > 180:
                snippet = snippet[:177] + "..."
            findings.append(Finding(path=path, line_no=line_no, snippet=snippet, archived=archived))
    return findings


def write_report(project: Path, findings: list[Finding], scanned_count: int) -> Path:
    active = [item for item in findings if not item.archived]
    archived = [item for item in findings if item.archived]
    report_path = project / "docs" / "MOJIBAKE_CLEANUP_REPORT.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# 中文乱码清理审计报告",
        "",
        f"- 测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- 扫描根目录：`{project}`",
        f"- 扫描文本文件数：{scanned_count}",
        f"- 活动文件疑似乱码行数：{len(active)}",
        f"- 归档/来源目录疑似乱码行数：{len(archived)}",
        "",
        "## 判定规则",
        "",
        "本审计查找常见 UTF-8/GBK 误解码痕迹，例如 "
        + "、".join(f"`{mark}`" for mark in MOJIBAKE_MARKS[:12])
        + " 等。合法科研符号如 Δ、β、π、ρ、∇、Å、→、←、·、– 不计为乱码。",
        "",
        "## 活动文件待清理项",
        "",
    ]
    if active:
        for item in active:
            rel = item.path.relative_to(project).as_posix()
            lines.append(f"- `{rel}:{item.line_no}`：`{item.snippet}`")
    else:
        lines.append("未发现活动文件中的疑似乱码。")
    lines.extend(["", "## 归档/来源目录记录", ""])
    if archived:
        for item in archived[:300]:
            rel = item.path.relative_to(project).as_posix()
            lines.append(f"- `{rel}:{item.line_no}`：`{item.snippet}`")
        if len(archived) > 300:
            lines.append(f"- 归档目录剩余 {len(archived) - 300} 行已省略。")
    else:
        lines.append("归档/来源目录未发现疑似乱码。")
    lines.extend(
        [
            "",
            "## 清理边界",
            "",
            "- 活动源码、测试、脚本、README、CHANGELOG 和当前 docs 应优先修复。",
            "- archive、legacy、vendor、integrated/origin-* 等目录默认视为归档来源，只记录不修复。",
            "- 若乱码出现在测试断言中，必须同步修复被测文本，不能只改测试。",
        ]
    )
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan a project for Chinese mojibake.")
    parser.add_argument("--project", required=True, help="Project root directory.")
    parser.add_argument("--fail-on-active", action="store_true", help="Return 1 when active findings exist.")
    parser.add_argument(
        "--archive-prefix",
        action="append",
        default=[],
        help="Additional archive prefix to record but not fail on.",
    )
    args = parser.parse_args()

    project = Path(args.project).expanduser().resolve()
    if not project.exists():
        print(f"项目目录不存在：{project}", file=sys.stderr)
        return 2

    archive_prefixes = DEFAULT_ARCHIVE_PREFIXES + tuple(prefix.replace("\\", "/") for prefix in args.archive_prefix)
    files = [path for path in project.rglob("*") if path.is_file() and is_text_candidate(path, project)]
    findings: list[Finding] = []
    for path in sorted(files):
        findings.extend(scan_file(path, project, archive_prefixes))

    report = write_report(project, findings, len(files))
    active_count = sum(1 for item in findings if not item.archived)
    archived_count = len(findings) - active_count
    print(f"扫描完成：文本文件 {len(files)} 个，活动乱码 {active_count} 行，归档记录 {archived_count} 行。")
    print(f"报告：{report}")
    if args.fail_on_active and active_count:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
