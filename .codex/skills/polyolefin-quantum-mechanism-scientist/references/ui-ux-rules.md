# UI/UX Rules

Use Google Workspace / Google Cloud logic for professional scientific software.

## Product Metaphors

- Google Drive: projects, molecules, Gaussian outputs, cube files, datasets, and reports are manageable resources.
- Google Docs: report outline, chapter preview, comments, evidence annotations, and source panels.
- Google Sheets: experiments, descriptors, energy tables, candidate matrices, filtering, sorting, and batch actions.
- Google Colab: Gaussian input generation, parser workflows, task templates, reproducible calculation cells.
- Google Cloud Console: APIs, tasks, logs, provenance, warnings, permissions, and safety boundaries.

## Layout

- Grouped navigation instead of long ungrouped lists.
- Top bar with project name, global search, data-source status, theme, and settings.
- Page header with Chinese title, one-sentence purpose, primary action, and status summary.
- Main work area plus right-side details/evidence panel where useful.
- Tables before decorative card grids for dense scientific information.

## Chinese-First Interface

Use Chinese for:

- Menu labels
- Buttons
- Chart titles
- Tooltips
- Legends
- Error messages
- Report text
- Evidence and source explanations

English scientific terms may appear as smaller secondary labels.

## Empty States

Use explicit recovery messages:

- 当前未上传真实 Gaussian 输出。
- 当前仅显示示例数据，不能作为真实结论。
- PDF 文本层疑似字体编码异常，请导入 OCR 文本。
- 缺少 π-complex 和 O→Ti complex，无法计算 ΔGpoison。
- 仅读取，不执行 Gaussian。

## Visual Restraint

- Avoid excessive nested cards.
- Keep chart heights stable.
- Show units on axes and tooltips.
- Use badges for evidence grade, mock/real status, source quality, parser quality, and warnings.
- Check mobile width around 390px for text overflow.
