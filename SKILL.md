---
name: biology-3d-courseware
description: 高中生物 3D 交互课件（three.js 单文件离线 HTML）的交付标准与执行流程。当用户要求制作、修改或交付高中生物 3D 课件（如减数分裂、光合作用、细胞结构、实验模拟、遗传规律等），或提到"按第一个课件的标准来""课件交付""S-01 那套要求"时使用。覆盖白色鲜艳主题、语音讲解与动画同步、右侧教学面板排版、人教版专业口径、数量自检、离线单文件与 GitHub Pages 发布。
description_zh: 高中生物 3D 课件交付标准：主题、语音同步、排版、人教版专业口径与发布流程
description_en: Delivery standard for high-school biology 3D courseware: theme, voice sync, layout, textbook rigor, publishing
version: 1.0.0
agent_created: true
allowed-tools: Read,Write,Edit,Glob,Grep,Bash,PowerShell
---

# 高中生物 3D 课件交付标准

把「S-01 减数分裂全流程时间轴」验证过的交付方式固化为可复用规范。目标是：后续每个课件在**主题、语音、排版、专业性**上与第一个保持同一水准，而不是每次重新发明。

## 何时使用

- 用户要新做一个高中生物 3D 交互课件（S/A/B/C 任意优先级）
- 用户要改已有课件，且要求"按第一个的标准""和 S-01 一致"
- 用户要交付/发布课件到 GitHub Pages
- 涉及 three.js 单文件离线 HTML、语音讲解、教学面板、数量曲线等

不适用：纯知识库文档、点子计划表、二维题库页面。

## 交付铁律（硬门槛，逐条不可省）

1. **目录自包含**：新建 `NNN_project_项目名/`，所有依赖随包；不散放在工作区根目录。
2. **技术基线**：three.js **r128 UMD** + `libs/three.min.js` 本地副本；单 HTML 双击离线可用；CDN 仅作兜底（unpkg → staticfile → jsdelivr）；不用构建工具、不引 ESM/importmap、不引 addons（相机控制器自写）。
3. **主题锁死**：白色/明亮底 + 鲜艳强调色；字体、圆角、阴影、卡片、背景装饰（渐变 + 光斑 + 点阵 + blob）、简洁模式、布局骨架全部沿用 `references/theme-tokens.md`；**每课只换主强调色 `--accent` / `--accent2`**。
4. **布局固定**：header（标题 + badge + 语音/简洁/全屏/复位/重置）→ 左舞台（顶部阶段导航 + 四角 HUD）+ 右面板 → 底部播放条 + 时间轴；≤980px 上下堆叠 + 抽屉，不得直接隐藏讲解。
5. **教学面板六块**：当前阶段讲解（可朗读）→ 实时读数 → 数量变化曲线 → 本时期要点 → 易错点 → 观察任务。顺序不可乱。
6. **专业性**：以**人教版 2019** 为准；顶部标教材版本 + 章节，**每个阶段标对应教材小节**；不臆造页码、不编造显微尺寸与实验数据；页面必须有「示意 · 非真实比例」，颜色注明「仅用于区分来源/结构」。
7. **数量自检**：染色体 / DNA / 染色单体 / 细胞数 + **统计口径**四项齐全；图表数据与右侧数字由**同一份数据源**驱动，禁止各写一套。
8. **语音强制**：每个课件都要有中文旁白（`speechSynthesis`，zh-CN）；播放必须走 **hold → 朗读 → morph** 状态机（见 `references/voice-sync.md`）；语速估算与 `utterance.rate` 同源；首次点击页面后才允许发声；切换阶段立即 `cancel()`。确实不适合旁白的（如纯测验）需在交付说明写明豁免理由。
9. **交付三件套**：`README.md`（阶段表 + 操作 + URL 参数 + 教材依据）、`修改记录.md`（改了什么、为什么）、`preview.png`（首屏截图）。
10. **验证后发布**：`node --check` 校验内联脚本 → 跑 `scripts/check_courseware.py` → headless 截图抽查 → **自动建仓库并开 GitHub Pages**（用户已确认每次自动发布）。

## 执行流程

### Step 0 · 立项
读需求，查 `高中生物3D课件点子计划表.md` 确认编号/类型/优先级；按 `NNN_project_项目名/` 建目录。

### Step 1 · 取材（先于写代码）
优先读知识库：
- `E:\AAA_文档\001-高中生物知识库\00-知识梳理与课件规划\高中生物知识库全景梳理.md`
- 同目录的点子计划表

提取四类信息：**教材依据（章节/小节）**、**数量关系**、**术语口径**、**易错点**。找不到依据时先问用户，不要凭印象编。

### Step 2 · 数据先行
先写阶段/状态数组（schema 见 `references/stage-schema.md`），把「数量自检表」在纸上算通，再动 3D。数字不通，动画一定错。

### Step 3 · 搭外壳
以 `assets/courseware-shell.html` 为基线，改标题、主色、阶段导航；保留背景装饰、简洁模式、响应式与底部控制条。

### Step 4 · 建 3D 场景
程序化建模（不依赖外部模型文件）；每个可交互对象命名并挂 `userData`；标签用投影 DOM 或 CSS2DRenderer；相机用自写轨道控制器。

### Step 5 · 接语音
按 `references/voice-sync.md` 实现状态机。关键：**画面只在语音 `onend` 后推进**，形变时长随语速缩放。

### Step 6 · 填教学面板
六块内容全部来自 Step 1 的取材；曲线与读数同源；统计口径逐阶段标注。

### Step 7 · 自检
```bash
python scripts/check_courseware.py "<项目目录>"
```
阻断项必须清零，警告项逐条判断。再做 headless 截图抽查关键状态。

### Step 8 · 文档与发布
写 README / 修改记录 / preview.png；然后：
```bash
git init && git add . && git commit -m "..."
gh repo create <英文仓库名> --public --source . --remote origin --push
gh api repos/<owner>/<repo>/pages -X POST -f source[branch]=main -f source[path]=/
```
补一个 `index.html` 门户页，让 Pages 根地址直达课件；验证 root / 课件 / three.min.js 均 200。

## 分类型范式

不同课件类型共用外壳，但 3D 场景与交互差异很大。开工前先读 `references/courseware-types.md` 对号入座：

- **时间轴 / 过程型**（减数分裂、光合作用、分泌蛋白）：阶段数组 + 时间轴 + 播放/单步
- **结构 / 解剖型**（细胞器、心脏、花的结构）：爆炸视图 + 剖切 + 点选高亮 + 名称标签
- **实验 / 模拟型**（质壁分离、酶活性、遗传杂交）：参数滑杆 + 条件控制 + 结果读数 + 对照
- **对比型**（有丝 vs 减数、光合 vs 呼吸）：双场景并排 + 同步时间轴 + 差异高亮

## 常见坑（S-01 已踩过）

- 姐妹染色单体用 `rotation.z=π` 会完全重合 → 改用 `scale.x = -1` 镜像
- 着丝粒挂在组原点会在缩放后飘走 → 挂到每条染色单体上，并反向补偿缩放
- 图表 x 轴写死 `/8` → 用 `/(数据长度-1)`
- 变量在定义前使用（TDZ）→ 先定义再引用
- 语音与动画各跑各的 → 必须用 hold/morph 状态机，不能固定时长硬推
- 用"精原细胞"当减数分裂起点 → 应为"初级精母细胞"

## 参考实现

`S-01 减数分裂全流程时间轴` 是本标准的首个合规样板，改新课件前先对照它：

- 本地：`001_project_减数分裂全流程时间轴/`
- 在线：https://azlove2021.github.io/meiosis-3d-courseware/
- 自检：`python scripts/check_courseware.py "<项目目录>"` → 0 阻断 / 0 警告
- 技能仓库：https://github.com/azlove2021/biology-3d-courseware-skill

## 资源索引

| 文件 | 用途 |
|---|---|
| `references/theme-tokens.md` | 锁定的色板、背景、布局、响应式、简洁模式 |
| `references/voice-sync.md` | hold→朗读→morph 状态机与完整代码 |
| `references/stage-schema.md` | 阶段数据结构、数量自检表模板 |
| `references/terms.md` | 术语口径与禁用表述 |
| `references/courseware-types.md` | 四类课件的范式与差异清单 |
| `references/delivery-checklist.md` | 交付前逐条勾选 |
| `scripts/check_courseware.py` | 机械校验（离线依赖/主题/语音/文档/术语） |
| `assets/courseware-shell.html` | 符合主题基线的最小外壳，复制后改内容 |
