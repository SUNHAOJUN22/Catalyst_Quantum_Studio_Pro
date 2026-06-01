# 真实科学计算软件连接说明

## 支持对象

平台当前支持登记以下真实科学计算软件或工作流组件：

- Gaussian16 / Gaussian09：生成 `.gjf/.com` 输入模板，解析 `.log/.out`。
- formchk：生成 `.chk -> .fchk` 命令模板。
- cubegen：生成 density、ESP、HOMO、LUMO cube 命令模板。
- Multiwfn：生成 QTAIM、NCI/RDG、ESP extrema 脚本模板。
- GoodVibes：生成命令模板，只读解析输出文本。
- RDKit：作为 Python 库用于分子处理；不可用时应降级提示。
- SLURM / local queue：生成批处理脚本模板，不提交任务。

## 配置方式

可通过 Settings UI、数据库 `simulation_tools` 或环境变量配置路径：

```text
GAUSSIAN16_PATH
FORMCHK_PATH
CUBEGEN_PATH
MULTIWFN_PATH
GOODVIBES_PATH
SLURM_SBATCH_PATH
QC_WORKDIR
ENABLE_REAL_QC_EXECUTION
```

默认情况下，即使路径已配置，平台也只生成模板和解析文本。

## 受控执行条件

真实执行必须同时满足：

1. 工具路径已配置且存在。
2. 任务模式为 `confirmed_execute`。
3. 用户二次确认。
4. 环境变量 `ENABLE_REAL_QC_EXECUTION=1`。
5. 命令来自白名单模板。
6. 输入、输出和工作目录不包含路径穿越。
7. 审计日志记录该操作。

当前 API 仍不会直接运行大型科学计算程序；当所有条件满足时，返回 `ready-but-not-run`，提示应由独立 runner 接管。

## 推荐真实计算流程

1. 在平台生成 Gaussian 输入模板。
2. 用户在受控 HPC / 工作站环境执行 Gaussian。
3. 使用 formchk / cubegen / Multiwfn / GoodVibes 生成后处理输出。
4. 将 `.log/.out/.cube/.txt` 输出导入平台。
5. 平台只读解析并生成 normalized JSON。
6. 人工核验收敛、频率、TS 虚频、IRC、方法、基组和 provenance。
7. 通过后才将证据等级从 D/C 提升为 A 级候选计算证据。

## 测试边界

CI 默认只测试：

- 工具路径登记。
- dry-run。
- 非法路径拒绝。
- 未开启 `ENABLE_REAL_QC_EXECUTION` 时拒绝执行。
- parser 只读解析。

CI 不执行真实 Gaussian、cubegen、Multiwfn 或 GoodVibes。
