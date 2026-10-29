# 变更记录

## 1.3.0 — 2026-10-29

补上 v1.2 最致命的缺口：**课件"能渲染但用不了"**——3D 不能转、不能缩放、点结构没反应，讲解卡片收不起来，投影时没法全屏看实验；而验收只跑了无头冒烟，测不出这些。

### 新增

- **3D 交互契约** `references/interaction-contract.md`
  - 轨道控制器（拖拽旋转 / 滚轮缩放 / 右键平移 / `R` 复位），`view.auto` 区分自动取景与用户接管
  - `Raycaster` 点选：高亮 + 选中框 + 信息卡；透明外壳 `fallback` 降级；隐藏对象 `chainVisible()` 排除；位移 <6px 且 <600ms 才算点击
  - 双击聚焦、右栏「结构速查」8 格按钮（兼图例与点选入口）
  - 面板三档折叠 `H` / `J` / `F` + `Shift+F` 全屏；窄屏改抽屉
- **真机验收** `references/browser-testing.md`：Tabbit 登录态全流程（旋转→缩放→逐个点选→三档折叠→影院→语音→考核→断网→4 种分辨率），逐步截图
- 配置新增 `interaction3d`（`orbit+pick` / `orbit` / `none`）与 `panelHide`（`three` / `two` / `one` / `none`）
- `scripts/smoke_test.py` 扩为交互冒烟：拖拽改相机、滚轮改距离、点选开卡片、左栏折叠、`F` 进影院、断网重载
- `tests/test_checker.py` 增至 **16 例**：新增"无 Raycaster / 无滚轮监听 / 无面板折叠 / 豁免可通过"四个用例

### 变更

- `SKILL.md` 铁律 9 → 12 条：新增「3D 必须可交互」「面板必须可隐藏」「Tabbit 真机验收不可跳过」
- 执行流程 8 步 → 10 步：Step 4 建场景含交互、Step 5 面板折叠、Step 9 Tabbit 验收
- `scripts/check_courseware.py`：交互与折叠改为**阻断项**（`interaction3d=none` / `panelHide=none` 可豁免但必须写理由）
- 验收层次 5 → 6 层：新增「可用」

### 修复（样板课）

- 样板课 `demo/gene-expression/` 补齐全部交互；修复窄屏面板 `display:none` 后无入口
- S-01 减数分裂标记 `interaction3d=orbit`、`panelHide=none`（legacy 豁免，理由写入 profile）

## 1.2.0 — 2026-10-29

按「铜匠实验室」54 门高中 3D 课件的公开设计语言，整体切换版式。

### 新增

- **玻璃拟态教学驾驶舱**：顶栏 / 因果链 / 步骤条 / 左栏本步 / 中央 3D / 右栏中控台 / 底栏，七区一屏
- `references/cockpit-layout.md`：七区尺寸、内容结构、交互契约、验收清单
- `metrics` 数据：连续指标（转录进度、mRNA 长度、肽链长度）与 `counts` 并列
- **样板课** `demo/gene-expression/`：基因的表达——转录与翻译，9 步、单 HTML、断网可用
- **技能主页** `index.html`：截图、设计语言、七区图、质量门槛、使用说明
- GitHub Pages：主页 + 样板课在线可看

### 变更

- `references/theme-tokens.md` 整体重写：`#2F6BFF / #13B8C6 / #7C5CFF`、玻璃面板、单元色、组件配方
- `SKILL.md` 改为三层规则 + 七区速查；新增 `layout` / `theme` / `bundle` 配置
- `scripts/check_courseware.py`：识别新 token 与七区结构；支持 `metrics`；新增 `backdrop-filter`、`主线问题`、`本步`、`中控台`、`考核` 检查
- `tests/test_checker.py` 扩到 12 个用例，新增 `metrics` 与玻璃主题故障样例
- `references/delivery-checklist.md` 改为驾驶舱版

### 说明

- 设计语言参考铜匠实验室（<https://lab.tongjiang.app>，CC BY-NC 4.0）；只借鉴布局、配色、组件语言，不复制代码、文案、素材
- S-01 减数分裂保留为 v1.1 旧版样板（六块面板），供兼容参考

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
