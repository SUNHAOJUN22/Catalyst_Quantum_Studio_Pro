from __future__ import annotations

import argparse
import importlib
import math
import sys
from pathlib import Path


try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass


EXPECTED = {
    "HARTREE_TO_KCAL_MOL": 627.509474,
    "HARTREE_TO_KJ_MOL": 2625.499638,
    "HARTREE_TO_EV": 27.211386245988,
    "R_KCAL_MOL_K": 0.00198720425864083,
    "DEFAULT_TEMPERATURE_K": 350.0,
}


def check(name: str, condition: bool, detail: str) -> bool:
    print(f"[{'PASS' if condition else 'FAIL'}] {name}: {detail}")
    return condition


def core_audit() -> list[bool]:
    results = [
        check("Hartree→kcal/mol", math.isclose(1.0 * EXPECTED["HARTREE_TO_KCAL_MOL"], 627.509474), "固定常数"),
        check("Hartree→kJ/mol", math.isclose(1.0 * EXPECTED["HARTREE_TO_KJ_MOL"], 2625.499638), "固定常数"),
        check("Hartree→eV", math.isclose(1.0 * EXPECTED["HARTREE_TO_EV"], 27.211386245988), "固定常数"),
    ]
    r = EXPECTED["R_KCAL_MOL_K"]
    t = EXPECTED["DEFAULT_TEMPERATURE_K"]
    results.extend(
        [
            check("krel(0)=1", math.isclose(math.exp(0.0), 1.0), "dimensionless"),
            check("正ΔΔG‡减速", math.exp(-3.0 / (r * t)) < 1.0, "350 K"),
            check("负ΔΔG‡加速", math.exp(3.0 / (r * t)) > 1.0, "350 K"),
        ]
    )
    return results


def project_audit(project: Path) -> list[bool]:
    backend = project / "backend"
    if not backend.exists():
        print("[SKIP] 未发现 backend，完成独立公式审计。")
        return []
    sys.path.insert(0, str(backend))
    try:
        constants = importlib.import_module("app.core.constants")
        energy = importlib.import_module("app.services.energy")
    except Exception as exc:
        print(f"[FAIL] 无法导入项目科学核心：{exc}")
        return [False]

    results = []
    for name, expected in EXPECTED.items():
        actual = getattr(constants, name, None)
        results.append(check(name, actual is not None and math.isclose(float(actual), expected), str(actual)))
    delta_h, delta_kcal = energy.delta_g_binding(-150.025, [-100.0, -50.0])
    results.append(check("ΔGbind", math.isclose(delta_h, -0.025) and math.isclose(delta_kcal, -0.025 * EXPECTED["HARTREE_TO_KCAL_MOL"]), f"{delta_kcal} kcal/mol"))
    poison, label, _ = energy.delta_g_poison(-100.0, -100.01)
    results.append(check("ΔGpoison", poison > 5.0 and "生产性" in label, f"{poison} kcal/mol"))
    results.append(check("BDE kJ/mol", "bde_kj_mol" in energy.bond_dissociation_energy(-99.9, -100.0), "多单位输出"))
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit scientific constants and formulas without external chemistry execution.")
    parser.add_argument("--project", default=".", help="Project root.")
    args = parser.parse_args()
    project = Path(args.project).expanduser().resolve()
    results = core_audit() + project_audit(project)
    failed = sum(not item for item in results)
    print(f"科学公式审计：PASS={len(results) - failed} FAIL={failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
