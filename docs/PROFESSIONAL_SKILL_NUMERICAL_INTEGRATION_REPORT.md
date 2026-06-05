# 专业 Skill、数理契约与科学仿真接口升级报告

## 1. 升级范围

- 项目：Catalyst Quantum Studio Pro
- 日期：2026-06-05
- 专业 Skill：`polyolefin-quantum-mechanism-scientist`
- 目标：把量子化学公式、证据等级、外部科学软件连接、MCP 接口、中文 UI 和自动化测试统一为可审计协议。

## 2. 数理核心

代码级固定常数：

| 常数 | 数值 | 状态 |
|---|---:|---|
| Hartree → kcal/mol | 627.509474 | PASS |
| Hartree → kJ/mol | 2625.499638 | PASS |
| Hartree → eV | 27.211386245988 | PASS |
| R | 0.00198720425864083 kcal mol^-1 K^-1 | PASS |
| 默认温度 | 350 K | PASS |

机器可读接口：

```text
GET /api/scientific-computation/validation-manifest
```

该接口公开 ΔGbind、ΔGpoison、插入势垒、krel、BDE 和自由基竞争公式，同时说明输入/输出单位、指数稳定策略和证据边界。

## 3. 证据等级修正

只读 parser 成功不再自动等同 A 级证据。

- 当前解析等级：C
- 可升级等级：A
- `paper_ready`：默认 `false`
- 升级条件：方法/基组、收敛、频率、TS 虚频、IRC、自旋和 provenance 完整核验
- mock、失败解析和模板：D 级

该规则避免把“文本字段被成功提取”误写成“量子化学结论已经成立”。

## 4. 科学软件连接器

当前支持 Gaussian16、formchk、cubegen、Multiwfn、GoodVibes、RDKit、SLURM 和只读 parser 的配置、模板、dry-run 与解析接口。

真实执行仍默认关闭。安全守卫要求：

- 外部执行显式启用；
- 工具路径已配置且存在；
- `confirmed_execute` 模式；
- 用户二次确认；
- 路径无穿越；
- 命令不得包含 shell 重定向或控制符；
- 未来 runner 必须使用参数数组、隔离工作目录、资源限制和审计日志。

本轮检查发现本机未配置 Gaussian16、formchk、cubegen、Multiwfn、GoodVibes 和 SLURM 路径，因此未执行任何外部科学程序。

## 5. MCP 扩展

新增：

- `audit_scientific_formulas`
- `inspect_external_tool_configuration`

两项工具均为只读操作，`can_execute_external = false`。前者返回数理契约，后者只检查路径/环境变量，不运行 version command。

## 6. 专业 Skill

Skill 新增参考协议：

- `references/numerical-rigor.md`
- `references/simulation-connectors.md`
- `references/mcp-tools.md`
- `references/reporting-rules.md`

Skill 新增可复用脚本：

- `scripts/scientific_formula_audit.py`
- `scripts/check_external_tools.py`

官方 `quick_validate.py` 验证结果：PASS。

## 7. UI 验证

“科学计算连接器”页面新增“数理与证据契约”区块，显示：

- 契约版本；
- Hartree 多单位换算；
- 主要公式；
- 输入/输出单位；
- 自动解析不等于论文 A 级证据的提示。

Playwright 与内置浏览器复核均确认：

- “数理与证据契约”唯一可见；
- `Hartree → kJ/mol：2625.499638` 正常显示；
- 浏览器控制台无 error；
- 390px 移动端无横向溢出。

## 8. 自动化验证

| 验证 | 结果 |
|---|---|
| Backend pytest | 88 passed |
| Skill 独立公式审计 | 14 passed, 0 failed |
| 数理严谨性审计 | PASS |
| 全功能 API smoke | PASS |
| 中文乱码审计 | 活动乱码 0 |
| Frontend Vitest | 99 passed |
| TypeScript strict | PASS |
| ESLint | PASS |
| Next.js production build | PASS |
| Playwright E2E | PASS |
| 根目录 quality gate | PASS 14 / FAIL 0 / SKIP 1 |

## 9. 科学结论边界

本轮工作验证的是软件公式、接口、解析、证据分级和安全守卫，不是对 DCS、MCSOMe、DMOS 或过氧化物体系的真实量子化学结论。

当前没有由本轮任务新产生的 A 级真实计算或 B 级真实实验结果。模板、mock 数据和自动化测试数值不能作为论文结论。

## 10. 剩余风险

1. 真实 marching-cubes / Three.js 完整等值面重建仍未实现，质量门禁保持 SKIP。
2. 外部科学软件未配置，真实 runner 尚未实现；当前系统只提供安全的模板、dry-run 和只读解析。
3. 真实 Gaussian/NBO/Multiwfn 输出仍需扩充多方法、多版本回归样本。
4. `ΔGpoison` 等阈值附近应进一步加入不确定度和敏感性分析，避免硬阈值过度解释。
