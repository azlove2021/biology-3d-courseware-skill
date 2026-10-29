# 变更记录

## 1.1.0 — 2026-10-29

基于《biology-3d-courseware-skill 优化建议》的 P0 / P1 / P2 落地。

### 修复

- **语音状态机竞态**：用五态 `pending / speaking / ended / cancelled / error` 替代 `speaking` 布尔值；每条语音一个 token；只有 `ended && voiceStage === stageIdx` 才进入 morph；`onerror` 800ms 兜底，另有总超时。
- **阶段示例口径**：`stage-schema.md` 的第三段改为明确的「末期Ⅰ」示例（每个子细胞 2 条染色体、4 个 DNA、4 条染色单体，`cells:2`），并注明末期Ⅱ 应为 4 个细胞。
- **离线误判**：校验脚本改用 `HTMLParser` 识别真正的 HTML 外链，不再把 `document.write` 里的 CDN 兜底字符串误判为外链。
- **图表写死**：S-01 的 `SERIES` 改为从 `STAGES.map` 派生，y 轴从数据最大值派生。

### 新增

- `courseware-profile.json` 配置：`type / voiceMode / quantityChart / interactionLevel / offlineRequired / params / publishMode / knowledgeBase`。
- `references/courseware-profile.md`、`runtime-contract.md`、`local-config.md`、`threejs-version.md`。
- `scripts/smoke_test.py`：可选 Playwright 冒烟测试，含断网验证与截图。
- `tests/test_checker.py`：10 个故障/正确样例回归，证明脚本能拦住已知错误。
- 校验脚本三层输出：静态结构 / 数据一致性 / 浏览器运行；支持 `--profile`、`--browser`、`--json`。
- JSON 数据块规范：`<script type="application/json" id="courseware-data">`，字段含 `id / name / group / counts / scope / events / visualState / source / simplifications`。
- 五层验收：数据 / 结构 / 过程 / 界面 / 教学。
- `CHANGELOG.md`、`CONTRIBUTING.md`。

### 变更

- **默认发布方式改为 `local`**：只落本地并校验；`ask` 询问一次；`auto` 才自动建仓库/Pages（需用户明确授权）。
- 知识库路径从 `SKILL.md` 移出，改由 `courseware-profile.json` 的 `knowledgeBase` 或环境变量 `BIOLOGY_KB` 配置。
- 语音默认仍为 `required`，但允许 `optional` / `disabled`，需写明理由。
- `SKILL.md` 由"10 条铁律"改为"通用底线 / 类型专属 / 可选配置"三层。

### 移除

- `SKILL.md` 中的本机路径 `E:\AAA_文档\...`。
- 旧的 `speaking` 布尔判断与 `stageIdx+0.999` 写法。

## 1.0.0 — 2026-10-29

- 首个版本：规范 + 校验脚本 + 可运行外壳。
- 固化 S-01 的主题 token、六块面板、语音 hold→morph、人教版口径、数量自检、交付清单与 GitHub Pages 发布流程。
