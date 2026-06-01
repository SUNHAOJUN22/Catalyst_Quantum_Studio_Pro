# 外部科学计算执行安全边界

## 默认禁止

平台默认禁止：

- 执行 Gaussian。
- 执行 cubegen。
- 执行 Multiwfn。
- 执行 GoodVibes。
- 执行用户上传文件。
- 任意 shell 注入。
- 项目目录外写入。
- 将 mock/example 数据升级为真实结论。

## 安全守卫

外部执行守卫检查：

- `ENABLE_REAL_QC_EXECUTION=1`
- `confirmed_execute`
- `user_confirmed=true`
- 工具 `can_execute=true`
- 工具路径存在
- 输入输出路径不含 `..` 或空字节
- 命令模板不含 shell 控制符

任何一项失败，API 返回中文错误，并保持 `will_execute=false`。

## dry-run

`dry-run` 用于返回：

- 命令模板。
- 预期输出。
- 拒绝原因。
- warnings。
- provenance。

dry-run 不运行外部程序。

## 证据边界

模板任务为 D 级证据。只读解析成功后，结果可以作为 A 级候选计算证据，但仍需人工核验：

- 计算是否正常终止。
- 频率是否合理。
- TS 是否只有一个合理虚频。
- IRC 是否连接正确。
- 方法、基组、温度和溶剂模型是否可追溯。
- 原始文件 provenance 是否完整。
