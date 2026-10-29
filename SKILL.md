---
name: biology-3d-courseware
description: 高中生物 3D 交互课件（three.js 单文件离线 HTML）的交付标准与执行流程。当用户要求制作、修改或交付高中生物 3D 课件（如减数分裂、光合作用、细胞结构、实验模拟、遗传规律等），或提到"按第一个课件的标准来""课件交付""S-01 那套要求"时使用。覆盖白色鲜艳主题、语音讲解与动画同步、右侧教学面板排版、人教版专业口径、数量自检、离线单文件与发布流程。
description_zh: 高中生物 3D 课件交付标准：三层规则、语音五态同步、数据同源、离线与发布契约
description_en: Delivery standard for high-school biology 3D courseware: layered rules, voice state machine, data consistency, offline and publishing contracts
version: 1.1.0
agent_created: true
allowed-tools: Read,Write,Edit,Glob,Grep,Bash,PowerShell
---

# 高中生物 3D 课件交付标准

把「S-01 减数分裂全流程时间轴」验证过的交付方式固化为可复用规范。v1.1 起按**通用底线 / 类型专属 / 可选配置**三层组织：每条规则都有明确适用范围，不搞"一刀切铁律"。

## 何时使用

- 新做一个高中生物 3D 交互课件（S/A/B/C 任意优先级）
- 修改已有课件，且要求"按第一个的标准""和 S-01 一致"
- 交付/发布课件到 GitHub Pages
- 涉及 three.js 单文件离线 HTML、语音讲解、教学面板、数量曲线

不适用：纯知识库文档、点子计划表、二维题库页面。

## 三层规则

### 第 1 层 · 通用底线（所有课件，不可豁免）

1. **科学准确**：以人教版 2019 为准；不编造页码、显微尺寸、实验数据；有分歧先列"待核实"。
2. **简化有说明**：模型必须标「示意 · 非真实比例」；颜色注明「仅用于区分来源/结构」。
3. **数据单一来源**：阶段数据、图表、右侧读数、README 数量表全部来自同一份结构化数据；禁止各写一套。
4. **交互可用**：旋转/缩放/阶段切换/播放/复位可用；关键按钮点击后有预期变化。
5. **离线可运行**：本地 `libs/three.min.js` 优先；HTML/CSS 不得有外链；断网后必需功能仍可用。
6. **文档与实现一致**：README 写的 URL 参数、语音行为、阶段表，必须与代码一致。
7. **发布有授权**：默认只落本地；公开仓库 / Pages 前必须确认无敏感信息且用户已授权。
8. **检查通过 ≠ 科学正确**：脚本只能证明结构、数据、运行；模型过程与教学效果仍需人工核。

### 第 2 层 · 类型专属（按 `profile.type` 启用）

先读 `references/courseware-types.md` 对号入座：

| 类型 | 核心组件 | 不强制 |
|---|---|---|
| `process` 时间轴/过程 | 阶段数组、时间轴、播放/单步、数量曲线 | — |
| `anatomy` 结构/解剖 | 爆炸视图、剖切、点选高亮、部件标签 | 数量曲线可关 |
| `experiment` 实验/模拟 | 自变量滑杆、因变量读数、对照组、结论区 | 阶段数组可省 |
| `comparison` 对比 | 双场景、阶段映射、差异高亮、对比表 | — |

### 第 3 层 · 可选配置（`courseware-profile.json`）

```json
{
  "type": "process",
  "voiceMode": "required",
  "quantityChart": "required",
  "interactionLevel": "standard",
  "offlineRequired": true,
  "params": ["t", "voice", "simple"],
  "publishMode": "local",
  "knowledgeBase": ""
}
```

- `voiceMode`：`required` / `optional` / `disabled`
- `quantityChart`：`required` / `optional` / `disabled`
- `interactionLevel`：`basic` / `standard` / `advanced`
- `publishMode`：`local`（默认）/ `ask` / `auto`
- 豁免必须写明理由；写不清理由就不要豁免

详见 `references/courseware-profile.md`。

## 执行流程

### Step 0 · 立项与配置
按 `NNN_project_项目名/` 建目录；复制 `assets/courseware-profile.example.json` 为 `courseware-profile.json`，按类型改字段。

### Step 1 · 取材（先于写代码）
按 `references/local-config.md` 的优先级取材：用户材料 → `BIOLOGY_KB` → profile 的 `knowledgeBase` → 经核实的公开资料。

提取：**教材小节**、**数量关系**、**术语口径**、**易错点**。路径不存在时不要编造，标注待核实。

### Step 2 · 数据先行
先写 `<script type="application/json" id="courseware-data">`（schema 见 `references/stage-schema.md`），把数量表算通；图表、读数、README 全部从它派生。

### Step 3 · 搭外壳
以 `assets/courseware-shell.html` 为基线：主题 token、背景装饰、六块面板、响应式、简洁模式、底部控制条。

### Step 4 · 建 3D 场景
程序化建模，不依赖外部模型文件；对象命名并挂 `userData`；标签用投影 DOM；相机用自写轨道控制器。

### Step 5 · 接语音（五态状态机）
按 `references/voice-sync.md`：`pending / speaking / ended / cancelled / error`，每条语音一个 token；**只有当前阶段语音 `ended` 才进入 morph**。禁止用 `!speaking` 判断。

### Step 6 · 填教学面板
六块顺序固定：讲解 → 实时读数 → 数量曲线 → 本时期要点 → 易错点 → 观察任务。曲线与读数同源；统计口径逐阶段标注。

### Step 7 · 三层自检
```bash
python scripts/check_courseware.py "<项目目录>"              # 静态 + 数据
python scripts/check_courseware.py "<项目目录>" --browser     # 加浏览器冒烟
python scripts/smoke_test.py "<课件.html>" --offline          # 单独跑冒烟
python tests/test_checker.py                                  # 回归测试（改脚本后必跑）
```
阻断项必须清零；警告逐条判断。**离线验收必须断网**，不能只看本地文件存在。

### Step 8 · 文档与发布
写 `README.md`（阶段表 + 操作 + URL 参数 + 离线/联网说明）、`修改记录.md`、`preview.png`。

发布按 `publishMode`：
- `local`：只交付本地
- `ask`：交付时问一次
- `auto`：建仓库 + 开 Pages（仅限用户明确授权）

发布前扫描密钥、个人信息、内部文件；用户指定私有仓库时不得擅自改公开。

## 五层验收

| 层次 | 检查什么 | 方式 |
|---|---|---|
| 数据 | 数值、阶段顺序、统计口径 | 脚本 + 人工 |
| 结构 | 对象数量、层级、身份 | 脚本 + 人工 |
| 过程 | 各阶段运动是否符合生物学过程 | 人工 / 截图断言 |
| 界面 | 画面、旁白、数据是否指向同一阶段 | 人工 |
| 教学 | 学生能否从画面看出机制 | 教师 |

## 常见坑（S-01 已踩过）

- 姐妹染色单体用 `rotation.z=π` 会完全重合 → 改用 `scale.x = -1` 镜像
- 着丝粒挂在组原点会在缩放后飘走 → 挂到每条染色单体上并反向补偿缩放
- 图表 x 轴写死 `/8`、y 轴写死 `/9` → 从数据长度与最大值派生
- 变量在定义前使用（TDZ）→ 先定义再引用
- 语音用 `!speaking` 判断结束 → 播放刚开始就抢跑；改用五态状态机
- 用"精原细胞"当减数分裂起点 → 应为"初级精母细胞"
- 末期Ⅰ与末期Ⅱ混成一个示例 → 末期Ⅱ每个子细胞 2 条染色体、共 4 个细胞

## 资源索引

| 文件 | 用途 |
|---|---|
| `references/theme-tokens.md` | 色板、背景、布局、响应式、简洁模式、每课主色 |
| `references/voice-sync.md` | 五态语音状态机与完整代码 |
| `references/stage-schema.md` | JSON 数据块、字段、数量自检、URL 参数 |
| `references/terms.md` | 术语口径与禁用表述 |
| `references/courseware-types.md` | 四类课件范式与差异 |
| `references/courseware-profile.md` | 配置字段、豁免、发布方式 |
| `references/runtime-contract.md` | 离线契约、参数契约、浏览器验证 |
| `references/local-config.md` | 本地知识库配置与取材顺序 |
| `references/threejs-version.md` | r128 依赖记录与升级回归 |
| `references/delivery-checklist.md` | 交付前逐条勾选 |
| `scripts/check_courseware.py` | 三层校验（静态/数据/运行） |
| `scripts/smoke_test.py` | 可选 Playwright 冒烟测试 |
| `tests/test_checker.py` | 校验脚本的故障样例回归 |
| `assets/courseware-shell.html` | 可运行外壳模板（含 JSON 数据块） |
| `assets/courseware-profile.example.json` | 配置样例 |

## 参考实现

`S-01 减数分裂全流程时间轴` 是本标准的首个合规样板：

- 本地：`001_project_减数分裂全流程时间轴/`
- 在线：https://azlove2021.github.io/meiosis-3d-courseware/
- 自检：`python scripts/check_courseware.py "<项目目录>"` → 0 阻断 / 0 警告
- 技能仓库：https://github.com/azlove2021/biology-3d-courseware-skill
