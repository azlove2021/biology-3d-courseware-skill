---
name: biology-3d-courseware
description: 高中生物 3D 交互课件（three.js 单文件离线 HTML）的交付标准与执行流程。当用户要求制作、修改或交付高中生物 3D 课件（如基因表达、光合作用、细胞结构、实验模拟、遗传规律等），或提到"按铜匠实验室的标准来""按第一个课件的标准""课件交付""教学驾驶舱"时使用。覆盖玻璃拟态教学驾驶舱、3D 可交互（旋转/缩放/点选）、讲解面板可折叠、语音五态同步、单一数据源、人教版专业口径、离线单文件与发布流程。
description_zh: 高中生物 3D 课件交付标准：玻璃拟态驾驶舱、3D 可交互与面板折叠、语音五态、数据同源、离线与发布契约
description_en: Delivery standard for high-school biology 3D courseware: glass cockpit, interactive 3D and collapsible panels, five-state voice, single-source data, offline and publishing contracts
version: 1.3.0
agent_created: true
allowed-tools: Read,Write,Edit,Glob,Grep,Bash,PowerShell
---

# 高中生物 3D 课件交付标准

把「铜匠实验室」54 门高中 3D 课件的公开设计语言，与 S-01 减数分裂的交付经验合并成一套可复用规范。v1.2 起版式从「六块面板」切换为**玻璃拟态教学驾驶舱**。

参考对象的硬指标（已实测 54 门）：

- **单 HTML + 内联 three.js ESM**，约 0.9–1.2 MB，双击离线可用，**零外链**
- **6–9 步**，最后一步固定「考核」；每步「问句 → 动手 → 结论 + 要点 + 考点」
- **七区驾驶舱**：顶栏 / 因果链 / 步骤条 / 左栏本步 / 中央 3D / 右栏中控台 / 底栏
- **玻璃拟态**：白 72–84% + `blur(12px) saturate(150%)` + 16px 圆角 + 蓝紫柔光阴影
- 主蓝 `#2F6BFF`、青 `#13B8C6`、紫 `#7C5CFF`；正文 `#0E1A2B`；单元色 5 套

> 设计语言参考铜匠实验室（<https://lab.tongjiang.app>，CC BY-NC 4.0）。**只借鉴布局、配色、组件语言，不复制其代码、文案、素材与课程数据。**

## 何时使用

- 新做一个高中生物 3D 交互课件（任意优先级）
- 修改已有课件，要求"按铜匠实验室的标准""按驾驶舱版式"
- 交付/发布课件到 GitHub Pages
- 涉及 three.js 单文件离线、语音讲解、教学驾驶舱、数据同源

不适用：纯知识库文档、点子计划表、二维题库页面。

## 三层规则

### 第 1 层 · 通用底线（所有课件，不可豁免）

1. **科学准确**：人教版 2019 为准；不编造页码、显微尺寸、实验数据；有分歧列「待核实」。
2. **简化有说明**：必须标「示意 · 非真实比例」；颜色注明「仅用于区分结构/来源」；底栏写清示意声明。
3. **数据单一来源**：阶段数据、读数、曲线、README 表全部来自同一份 JSON；禁止各写一套。
4. **驾驶舱七区完整**：顶栏、因果链、步骤条、左栏本步、中央 3D、右栏中控台、底栏，缺一不可。
5. **3D 必须可交互**（v1.3）：左键拖拽旋转、滚轮/按钮缩放、右键平移、**单击结构弹信息卡**、双击聚焦、`R` 回预设。只做"每步一个固定机位"= 不可交付。
6. **讲解面板必须可隐藏**（v1.3）：`H` 左栏 / `J` 右栏 / `F` 影院（全隐只留胶囊）/ `Shift+F` 浏览器全屏；窄屏改抽屉，不许 `display:none` 后无入口。
7. **交互可用**：下一步/上一步必须改变机位+文案+读数；滑块必须实时改 3D 与读数；相机不瞬移；用户接管视角后本步不再抢镜。
8. **离线可运行**：单 HTML 内联 three.js，或本地 `libs/`；HTML/CSS 零外链；断网可用。
9. **文档与实现一致**：README 写的步骤、参数、语音行为，必须与代码一致。
10. **发布有授权**：默认只落本地；公开仓库/Pages 前确认无敏感信息且用户已授权。
11. **检查通过 ≠ 能用**：脚本只证明结构、数据、路径；**交付前必须用 Tabbit 在真实浏览器跑完整交互流程并截图**（见 `references/browser-testing.md`），否则不算交付。
12. **检查通过 ≠ 科学正确**：模型过程与教学效果仍需人工核。

### 第 2 层 · 类型专属（按 `profile.type` 启用）

| 类型 | 核心组件 | 步数 | 最后一步 |
|---|---|---|---|
| `process` 过程/机制 | 阶段数据、因果链、步骤条、中控台读数/曲线 | 6–9 | 考核 |
| `anatomy` 结构/解剖 | 爆炸视图、剖切、点选高亮、部件标签 | 5–8 | 结构辨认 |
| `experiment` 实验/模拟 | 自变量滑杆、因变量读数、对照组、结论区 | 6–9 | 考核·当实验员 |
| `comparison` 对比 | 双场景、阶段映射、差异高亮、对比表 | 6–8 | 对比测验 |

参考对象的四种题材：原理与现象（39）、工业流程（9）、原理与实验（5）、模拟（1）。生物课多为「原理与现象」。

### 第 3 层 · 可选配置（`courseware-profile.json`）

```json
{
  "type": "process",
  "layout": "cockpit",
  "theme": "glass",
  "voiceMode": "required",
  "quantityChart": "required",
  "interactionLevel": "standard",
  "interaction3d": "orbit+pick",
  "panelHide": "three",
  "offlineRequired": true,
  "bundle": "inline",
  "params": ["t", "voice", "simple"],
  "publishMode": "local",
  "knowledgeBase": ""
}
```

- `layout`：`cockpit`（默认）/ `legacy`（旧六块面板，仅维护旧课件）
- `theme`：`glass`（默认）/ `bright`（无模糊的纯白降级）
- `interaction3d`：`orbit+pick`（默认，转+缩放+点选）/ `orbit`（只转+缩放）/ `none`（须写豁免理由）
- `panelHide`：`three`（默认，左栏/右栏/影院）/ `two` / `one` / `none`（须写豁免理由）
- `bundle`：`inline`（单 HTML 内联 three.js）/ `libs`（本地 libs 目录）
- `voiceMode` / `quantityChart` / `interactionLevel`：`required` / `optional` / `disabled`
- `publishMode`：`local`（默认）/ `ask` / `auto`
- 豁免必须写明理由（`exemptions` 字段）；写不清理由就不要豁免

详见 `references/courseware-profile.md`。

## 执行流程

### Step 0 · 立项与配置
按 `NNN_project_项目名/` 建目录；复制 `assets/courseware-profile.example.json`，按类型改字段。

### Step 1 · 取材（先于写代码）
按 `references/local-config.md`：用户材料 → `BIOLOGY_KB` → profile 的 `knowledgeBase` → 经核实公开资料。

提取：**教材小节**、**主线问题**、**因果链 3–5 环**、**6–9 步标题**、**每步问句/动作/观察/结论**、**易错点**。

### Step 2 · 数据先行
先写 `<script type="application/json" id="courseware-data">`（schema 见 `references/stage-schema.md`），把每步指标算通；读数、曲线、README 全部派生。

### Step 3 · 搭驾驶舱外壳
按 `references/cockpit-layout.md` 的七区结构搭壳：顶栏、因果链、步骤条、左栏本步、中央 3D、右栏中控台、底栏。主题 token 见 `references/theme-tokens.md`。

### Step 4 · 建 3D 场景（含交互）
程序化建模，不依赖外部模型；对象命名并挂 `userData.pickId`；浮动标签投影到 3D 坐标；相机每步一个预设，过渡 0.8–1.2s。

**同时完成三件交互**（见 `references/interaction-contract.md`）：
1. 轨道控制器：拖拽旋转 / 滚轮缩放 / 右键平移 / `R` 复位，`view.auto` 区分自动与接管；
2. `Raycaster` 点选：高亮 + 选中框 + 信息卡；透明外壳用 `fallback` 降级，隐藏对象用 `chainVisible()` 排除；
3. 右栏「结构速查」：8 格按钮兼图例与点选入口。

### Step 5 · 面板折叠
`H` 左栏 / `J` 右栏 / `F` 影院 / `Shift+F` 全屏；窄屏改抽屉。影院模式必须有可退出胶囊。

### Step 6 · 接语音（五态状态机）
按 `references/voice-sync.md`：`pending / speaking / ended / cancelled / error`；每条语音一个 token；**只有当前步语音 `ended` 才允许进入下一步**；禁止 `!speaking`。

### Step 7 · 填三栏
- **左栏**：问句 → 动手 → 应该看到 → 揭示结论 → 复位；底部单元 tab
- **右栏**：读数卡 + 滑块 + 迷你图 + 预设/复位 + 结构速查
- **顶部**：主线问题 + 因果链；**底部**：上一步/下一步 + 第 X/N 步 + 示意声明

### Step 8 · 三层自检
```bash
python scripts/check_courseware.py "<项目目录>"              # 静态 + 数据
python scripts/check_courseware.py "<项目目录>" --browser     # 加浏览器冒烟
python scripts/smoke_test.py "<课件.html>" --offline          # 单独跑冒烟
python tests/test_checker.py                                  # 改脚本后必跑
```
阻断项清零；警告逐条判断。**离线验收必须断网**。

### Step 9 · Tabbit 真机验收（不可跳过）
按 `references/browser-testing.md`：在用户已登录的 Tabbit 里跑「旋转 → 缩放 → 逐个点选 → 三档折叠 → 影院 → 语音 → 考核 → 断网 → 4 种分辨率」，逐步截图存 `<项目>/shots/`。
任一项不通过 → 回 Step 4/5 修，**不许带着「能渲染但用不了」交付**。

### Step 10 · 文档与发布
写 `README.md`（步骤表 + 操作 + 快捷键 + URL 参数 + 离线说明 + 2–3 张实测截图）、`修改记录.md`、`preview.png`。

发布按 `publishMode`：`local` 只落本地；`ask` 问一次；`auto` 建仓库 + 开 Pages（需授权）。发布前扫描密钥、个人信息、内部文件。

## 七区速查

| 区 | 必备 | 尺寸 |
|---|---|---|
| 顶栏 | 标题 + 副标题 + 主线问题 + 状态/得分 + 检测/玩法 + **讲解/中控/影院** + 语音 | 高 78px |
| 因果链 | 3–5 个 chip + 箭头 + 每格一句解释 | 高约 30px |
| 步骤条 | 6–9 步编号 + 短标题 + 当前高亮 | 高 46px |
| 左栏 | 本步面包屑 + 问句 + 场景说明 + 动手 + 应该看到 + 揭示结论/复位 + 单元 tab | `clamp(320px,22vw,404px)` |
| 中央 3D | 场景 + 浮动标签 + 方程式卡 | ≥560px 宽 |
| 右栏 | 中控台 + 读数卡 + 滑块 + 迷你图 + 预设/复位 | `clamp(300px,20.5vw,348px)` |
| 底栏 | 上一步/下一步 + 第 X/N 步 + 示意声明 + 快捷键 | 高 52px |

## 五层验收

| 层次 | 检查什么 | 方式 |
|---|---|---|
| 数据 | 数值、步骤顺序、统计口径 | 脚本 + 人工 |
| 结构 | 七区是否齐、3D 对象数量/层级 | 脚本 + 人工 |
| 过程 | 每步运动是否符合生物学过程 | 人工 / 截图断言 |
| 界面 | 画面、旁白、读数是否指向同一步 | 人工 |
| **可用** | 能否旋转/缩放/点选/折叠/影院/语音/考核 | **Tabbit 真机 + 截图** |
| 教学 | 学生能否从画面看出机制 | 教师 |

## 常见坑

- 还在用旧六块面板 → v1.2 起改为驾驶舱七区
- **只做「每步一个固定机位」→ 学生转不动、点不中，等于不可用**（v1.2 的教训）
- **点选永远选中核膜/细胞膜** → 半透明容器要先跳过，用 `fallback` 降级
- **`visible=false` 的对象仍会被 raycast 命中** → 自写 `chainVisible()`
- **拖拽被当成点击** → 位移 < 6px 且 < 600ms 才算点选
- **聚焦贴脸** → 用 `max(4.5, max(r*.62, s*1.7))`，别用 `s*1.05`
- **窄屏 `display:none` 后再无入口** → 改抽屉 + 顶栏按钮
- **影院模式回不去** → 胶囊必须有「退出影院」，`Esc` 优先退出影院
- 玻璃面板做成不透明纯白 → 失去层次；必须 `backdrop-filter` + 半透明
- 正文超过 14px → 驾驶舱信息密度高，会溢出
- 步骤超过 9 步或没有「考核」→ 一屏讲不完，且缺闭环
- 滑块只改数字不改 3D → 学生看不出因果
- 相机瞬移 → 用 0.8–1.2s 缓动过渡
- 面板遮住 3D 主体 → 中央至少留 560px
- 复制铜匠实验室的 logo/文案/素材 → 只借鉴设计语言，不复制内容
- 语音用 `!speaking` 判断 → 播放刚开始就抢跑；用五态状态机
- 姐妹染色单体 `rotation.z=π` 会重合 → 用 `scale.x=-1` 镜像
- 图表 x/y 轴写死 → 从数据长度与最大值派生
- **只跑无头 Playwright 就交付** → 无头测不出手感、字体、语音；必须 Tabbit 真机

## 资源索引

| 文件 | 用途 |
|---|---|
| `references/theme-tokens.md` | 玻璃拟态 token、单元色、组件、尺寸 |
| `references/cockpit-layout.md` | 七区版式、内容结构、交互契约、验收 |
| `references/interaction-contract.md` | 3D 轨道/缩放/点选代码、面板三档折叠、结构速查 |
| `references/browser-testing.md` | Tabbit 真机全流程验收（命令 + 判定 + 截图） |
| `references/voice-sync.md` | 五态语音状态机与完整代码 |
| `references/stage-schema.md` | JSON 数据块、字段、数量/指标、URL 参数 |
| `references/terms.md` | 术语口径与禁用表述 |
| `references/courseware-types.md` | 四类课件范式与差异 |
| `references/courseware-profile.md` | 配置字段、豁免、发布方式 |
| `references/runtime-contract.md` | 离线契约、参数契约、浏览器验证 |
| `references/local-config.md` | 本地知识库配置与取材顺序 |
| `references/threejs-version.md` | three.js 依赖记录与升级回归 |
| `references/delivery-checklist.md` | 交付前逐条勾选 |
| `scripts/check_courseware.py` | 三层校验（静态/数据/运行） |
| `scripts/smoke_test.py` | Playwright 冒烟：旋转/缩放/点选/折叠/影院/断网 |
| `tests/test_checker.py` | 校验脚本的故障样例回归（16 例） |
| `assets/courseware-shell.html` | v1.1 旧版外壳（六块面板，兼容参考） |
| `demo/gene-expression/` | v1.2 驾驶舱样板（可直接复制改内容） |
| `assets/courseware-profile.example.json` | 配置样例 |

## 参考实现

- **v1.2 驾驶舱样板**：`demo/gene-expression/`（基因的表达：转录与翻译）
  - 在线：https://azlove2021.github.io/biology-3d-courseware-skill/demo/gene-expression/
  - 9 步、玻璃拟态七区、语音五态、右栏中控台、最后一步考核
- **v1.1 旧版样板**：`001_project_减数分裂全流程时间轴/`（S-01 减数分裂，六块面板，保留作兼容参考）
- 技能仓库：https://github.com/azlove2021/biology-3d-courseware-skill
