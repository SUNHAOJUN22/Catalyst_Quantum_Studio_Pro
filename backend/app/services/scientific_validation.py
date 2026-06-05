from __future__ import annotations

from typing import Any

from app.core.constants import (
    DEFAULT_TEMPERATURE_K,
    HARTREE_TO_EV,
    HARTREE_TO_KCAL_MOL,
    HARTREE_TO_KJ_MOL,
    R_KCAL_MOL_K,
)


FORMULA_CONTRACTS = [
    {
        "key": "delta_g_bind",
        "formula": "ΔGbind = G(complex) − ΣG(fragments)",
        "input_unit": "Hartree",
        "output_units": ["Hartree", "kcal/mol"],
    },
    {
        "key": "delta_g_poison",
        "formula": "ΔGpoison = G(O→Ti complex) − G(C=C π-complex)",
        "input_unit": "Hartree",
        "output_units": ["kcal/mol"],
        "boundaries": ["> +5：生产性插入占优", "0 至 +5：配位竞争", "< 0：Ti 毒化风险"],
    },
    {
        "key": "insertion_profile",
        "formula": "ΔG‡ = G(TS) − G(free active site + monomer)",
        "input_unit": "Hartree",
        "output_units": ["kcal/mol"],
    },
    {
        "key": "relative_rate",
        "formula": "krel = exp[-ΔΔG‡/(RT)]",
        "input_unit": "kcal/mol, K",
        "output_units": ["dimensionless"],
        "numerical_policy": "指数限制在 [-50, 50]，避免浮点上溢；极端输入返回有限近似值。",
    },
    {
        "key": "bond_dissociation_energy",
        "formula": "BDE = ΣG(radical fragments) − G(parent)",
        "input_unit": "Hartree",
        "output_units": ["Hartree", "kcal/mol", "kJ/mol", "eV"],
    },
    {
        "key": "radical_competition",
        "formula": "S_LCB = R_branch/(R_branch + R_scission + R_oxidation)",
        "input_unit": "consistent kinetic units",
        "output_units": ["dimensionless"],
    },
]


def scientific_validation_manifest() -> dict[str, Any]:
    return {
        "contract_version": "2026.06",
        "constants": {
            "hartree_to_kcal_mol": HARTREE_TO_KCAL_MOL,
            "hartree_to_kj_mol": HARTREE_TO_KJ_MOL,
            "hartree_to_ev": HARTREE_TO_EV,
            "r_kcal_mol_k": R_KCAL_MOL_K,
            "default_temperature_k": DEFAULT_TEMPERATURE_K,
        },
        "formulas": FORMULA_CONTRACTS,
        "evidence_policy": {
            "A": "真实计算且收敛、频率/TS/IRC 与 provenance 完整，并经人工科学核验。",
            "B": "真实实验且样品、工艺、表征条件完整。",
            "C": "只读解析结果、文献线索或用户输入，尚未完成全部科学核验。",
            "D": "mock/example、失败解析或仅有任务模板。",
        },
        "execution_policy": {
            "default": "template_only/read_only",
            "external_execution": "API 默认不执行外部程序；命令模板含 shell 控制符时必须拒绝。",
            "uploaded_files": "只读解析，不把上传内容作为命令执行。",
        },
        "paper_boundary": "自动解析成功不等于 A 级证据；只有完成方法、收敛、频率/TS/IRC 和来源核验后才可进入论文结论。",
    }


def assess_parser_evidence(
    parser_name: str,
    quality: str,
    is_mock: bool,
    normalized: dict[str, Any] | None = None,
) -> dict[str, Any]:
    normalized = normalized or {}
    if is_mock or quality == "failed":
        return {
            "evidence_grade": "D",
            "eligible_grade": "D",
            "paper_ready": False,
            "reason": "示例数据或失败解析不能作为真实科学结论。",
        }

    eligible_grade = "A"
    if parser_name in {"gaussian", "gaussian_log", "parse_gaussian_log"}:
        normal = normalized.get("normal_termination")
        if isinstance(normal, dict):
            normal = normal.get("value")
        if quality != "complete" or normal is not True:
            eligible_grade = "C"

    return {
        "evidence_grade": "C",
        "eligible_grade": eligible_grade,
        "paper_ready": False,
        "reason": "只读解析已获得结构化数据，但仍需人工核验方法、基组、收敛、频率/TS/IRC 与原始文件来源。",
    }
