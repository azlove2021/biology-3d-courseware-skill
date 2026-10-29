# 贡献指南

## 修改前

1. 先读 `SKILL.md` 的三层规则，确认改动属于哪一层
2. 涉及数据结构的改动，先改 `references/stage-schema.md`
3. 涉及语音的改动，先改 `references/voice-sync.md`
4. 改模板或脚本后，必须跑回归测试

## 新增一种课件类型

1. 在 `references/courseware-types.md` 增加一节：必备组件、交互、常见坑
2. 在 `courseware-profile.md` 的 `type` 允许值中登记
3. 在 `check_courseware.py` 的 `ALLOWED["type"]` 中登记
4. 如有专属数据结构，在 `stage-schema.md` 增加 schema
5. 补一个最小样例（可放 `tests/`），并让校验脚本能识别

## 修改模板

- 主题 token、布局、六块面板：改 `references/theme-tokens.md` 与 `assets/courseware-shell.html`，两者必须一致
- 语音：只改 `references/voice-sync.md` 与模板中的同一段逻辑，禁止另写一套
- 数据：只改 `stage-schema.md` 与模板的 JSON 数据块，图表必须继续从数据派生

## 运行检查

```bash
# 语法
python -m py_compile scripts/check_courseware.py scripts/smoke_test.py

# 回归测试（改脚本/模板后必跑）
python tests/test_checker.py

# 用参考实现跑一遍
python scripts/check_courseware.py "../001_project_减数分裂全流程时间轴"

# 可选浏览器冒烟
python scripts/smoke_test.py "../001_project_减数分裂全流程时间轴/S-01_减数分裂.html" --offline
```

要求：

- `tests/test_checker.py` 全过
- 参考实现 0 阻断
- 新增故障样例时，确认脚本真的会拦住它

## 提交

- 一次提交只做一件事；提交信息写清"改了什么、为什么"
- 不提交密钥、个人信息、本机绝对路径、内部文件
- 更新 `CHANGELOG.md` 的"未发布"或对应版本
- 兼容性变化（字段改名、默认值变化）必须单独标注

## 风格

- 中文说明，术语按 `references/terms.md`
- 规则写"适用范围 + 可豁免条件"，不写无边界的"必须"
- 代码片段可直接复制运行，不写伪代码
- 不引用未核实的页码、实验数据
