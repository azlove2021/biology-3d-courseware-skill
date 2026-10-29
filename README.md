# 高中生物 3D 课件交付标准（WorkBuddy 技能）

把「铜匠实验室」54 门高中 3D 课件的公开设计语言，与 S-01 减数分裂的交付经验合并成一套可复用规范。v1.2 起版式从「六块面板」切换为**玻璃拟态教学驾驶舱**；v1.3 起补上**「能渲染」之外的能力门槛**。

- 📦 技能仓库：<https://github.com/azlove2021/biology-3d-courseware-skill>
- 🌐 技能主页（GitHub Pages）：<https://azlove2021.github.io/biology-3d-courseware-skill/>
- 🧬 样板课：<https://azlove2021.github.io/biology-3d-courseware-skill/demo/gene-expression/>

## v1.3 的关键变化：从「能渲染」到「能用」

v1.2 的样板课通过了全部自动检查，但学生**转不动、缩放不了、点结构没反应，讲解卡片也收不起来**——这是「验收只测渲染、不测使用」的必然结果。v1.3 把三件事定为交付底线：

1. **3D 必须可交互**：拖拽旋转 / 滚轮缩放 / 右键平移 / **单击结构弹信息卡** / 双击聚焦 / `R` 回预设；用户接管视角后本步不抢镜，切步回预设
2. **讲解面板必须可隐藏**：`H` 左栏 / `J` 右栏 / `F` 影院（全隐只留胶囊）/ `Shift+F` 全屏；窄屏改抽屉，不许 `display:none` 后无入口
3. **Tabbit 真机验收必做**：登录态真实浏览器跑「旋转→缩放→逐个点选→三档折叠→影院→语音真声→考核判分→断网→4 种分辨率」，逐步截图；无头 Playwright 只做回归

真机验收立刻抓到一个无头测试测不出的真 bug：**150% 系统缩放下 `setSize(w,h,false)` 让画布按设备像素布局**——画面放大 1.5 倍被裁切、点选坐标映射全错（这正是「点不中 RNA」的根因）。已修复，并加入校验脚本作为阻断项。

## v1.2 的关键变化

- **玻璃拟态教学驾驶舱**：顶栏 / 因果链 / 步骤条 / 左栏本步 / 中央 3D / 右栏中控台 / 底栏，七区一屏
- **设计 token 重写**：主蓝 `#2F6BFF`、青 `#13B8C6`、紫 `#7C5CFF`；玻璃面板 `rgba(255,255,255,.72–.84)` + `blur(12px) saturate(150%)` + 16px 圆角
- **内容结构**：6–9 步，最后一步固定「考核」；每步「问句 → 动手 → 应该看到 → 揭示结论 + 要点 / 易错点 / 考点」
- **右栏中控台**：读数卡 + 滑块 + 迷你曲线 + 参考工况 / 复位
- **`metrics` 数据**：除染色体计数外，支持连续指标（如转录进度、mRNA 长度、肽链长度）
- **校验脚本升级**：识别驾驶舱 token/七区结构；支持 `metrics`；新增 `backdrop-filter`、`主线问题`、`本步`、`中控台`、`考核` 检查
- **样板课**：`demo/gene-expression/`（基因的表达：转录与翻译），9 步、单 HTML、断网可用、0 阻断 / 0 警告

## 安装

把整个目录放到 WorkBuddy 的用户级技能目录：

```
~/.workbuddy-ai/skills/biology-3d-courseware/
```

Windows 下即：

```
C:\Users\<你的用户名>\.workbuddy-ai\skills\biology-3d-courseware\
```

重载或新开会话后，技能会自动出现在列表中。

## 内容

| 文件 | 用途 |
|---|---|
| `SKILL.md` | 三层规则 + 8 步流程 + 七区速查 + 五层验收 + 常见坑 |
| `references/theme-tokens.md` | 玻璃拟态 token、单元色、组件、尺寸 |
| `references/cockpit-layout.md` | 七区版式、内容结构、交互契约、验收 |
| `references/voice-sync.md` | 五态语音状态机与完整代码 |
| `references/stage-schema.md` | JSON 数据块、`counts` / `metrics`、URL 参数 |
| `references/terms.md` | 术语口径与禁用表述速查 |
| `references/courseware-types.md` | 四类课件范式与差异 |
| `references/courseware-profile.md` | 配置字段、豁免规则、发布方式 |
| `references/interaction-contract.md` | 3D 轨道/缩放/点选代码、面板三档折叠、结构速查 |
| `references/browser-testing.md` | Tabbit 真机全流程验收（命令 + 判定 + 截图） |
| `references/runtime-contract.md` | 离线契约、参数契约、浏览器验证 |
| `references/local-config.md` | 本地知识库配置与取材顺序 |
| `references/threejs-version.md` | three.js 依赖记录、许可证、升级回归 |
| `references/delivery-checklist.md` | 交付前逐条勾选（A–J 十二组） |
| `scripts/check_courseware.py` | 三层校验：静态结构 / 数据一致性 / 浏览器运行 |
| `scripts/smoke_test.py` | Playwright 交互冒烟：旋转/缩放/点选/折叠/影院/断网 |
| `tests/test_checker.py` | 校验脚本的故障样例回归（18 个用例） |
| `assets/courseware-shell.html` | v1.1 旧版外壳（六块面板，兼容参考） |
| `demo/gene-expression/` | 样板课：基因的表达（单 HTML + 截图 + 文档） |
| `index.html` | 技能主页（GitHub Pages 根地址） |

## 使用

在对话里说：

- 「按课件交付标准做 S-02 ×××」
- 「按铜匠实验室的标准改这个课件」
- 「检查这个课件是否符合交付标准」

或手动跑校验：

```bash
# 静态 + 数据
python scripts/check_courseware.py "<项目目录>"

# 加浏览器冒烟（需 playwright）
python scripts/check_courseware.py "<项目目录>" --browser

# 单独跑冒烟 / 断网验证
python scripts/smoke_test.py "<课件.html>" --offline

# 改过模板或脚本后，跑回归测试
python tests/test_checker.py
```

- 退出码 `0`：通过（可能有警告）
- 退出码 `1`：存在阻断项

## 三层规则速览

| 层 | 内容 | 是否可豁免 |
|---|---|---|
| 通用底线 | 科学准确、简化有说明、数据同源、驾驶舱七区、交互可用、离线可运行、文档一致、发布授权 | 否 |
| 类型专属 | 过程型阶段/指标；解剖型爆炸视图/剖切；实验型滑杆/对照；对比型双场景/差异高亮 | 按类型 |
| 可选配置 | `layout` / `theme` / `bundle` / `voiceMode` / `quantityChart` / `interactionLevel` / `publishMode` / `params` | 是，需写明理由 |

## 兼容性

- 主要目标：WorkBuddy / CodeBuddy 技能加载器（`SKILL.md` + `references/` + `scripts/` + `assets/`）
- 元数据：`name` / `description` / `version` / `agent_created` / `allowed-tools`
- 脚本：Python 3.9+；`check_courseware.py` 的 JS 数据回退需要 Node.js（仅用于解析 `const STAGES`）
- 浏览器冒烟：Playwright + Chromium（可选，不装则跳过）
- 未在其他技能加载器上逐项验证；如需移植，请先核对其 frontmatter 字段要求

## 设计来源与许可

- 设计语言参考 **铜匠实验室** <https://lab.tongjiang.app>（CC BY-NC 4.0）：只借鉴布局、配色、组件语言；**代码、文案、3D 模型、截图均为自研**
- 技能本身未指定许可证，默认保留所有权利；如需以 MIT、CC BY-NC 等协议开源，请先与作者确认后补充 `LICENSE`
- 课件内容依据人教版 2019；示意模型非真实比例

## 版本

v1.2.0 · 2026-10-29 · 变更见 [CHANGELOG.md](CHANGELOG.md)
