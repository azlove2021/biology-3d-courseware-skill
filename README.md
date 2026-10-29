# 高中生物 3D 课件交付标准（WorkBuddy 技能）

把「S-01 减数分裂全流程时间轴」验证过的交付方式固化为可复用技能。后续每个课件在**主题、语音、排版、专业性**上与第一个保持同一水准。

- 📦 技能仓库：<https://github.com/azlove2021/biology-3d-courseware-skill>
- 🧪 参考实现：<https://github.com/azlove2021/meiosis-3d-courseware>

## v1.1 的关键变化

- **三层规则**：通用底线（不可豁免）/ 类型专属（按 `type` 启用）/ 可选配置（`courseware-profile.json`）
- **语音五态状态机**：`pending / speaking / ended / cancelled / error`，修掉"播放刚开始动画就抢跑"的竞态
- **单一数据源**：HTML 内嵌 `<script type="application/json" id="courseware-data">`，图表、读数、README 表全部派生
- **三层校验**：静态结构 / 数据一致性 / 浏览器运行（可选 Playwright）
- **故障样例回归**：`tests/test_checker.py` 证明脚本能拦住已知错误，而不只是让正确项目通过
- **离线与发布契约**：断网必须可运行；默认只落本地，公开仓库/Pages 需授权
- **本机路径移出公共流程**：知识库位置改由 `courseware-profile.json` 或 `BIOLOGY_KB` 配置

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
| `SKILL.md` | 三层规则 + 8 步流程 + 五层验收 + 常见坑 |
| `references/theme-tokens.md` | 锁定色板、背景、布局、响应式、简洁模式、每课主色 |
| `references/voice-sync.md` | 五态语音状态机与完整代码 |
| `references/stage-schema.md` | JSON 数据块、字段规范、数量自检、URL 参数 |
| `references/terms.md` | 术语口径与禁用表述速查 |
| `references/courseware-types.md` | 时间轴 / 解剖 / 实验 / 对比四类范式 |
| `references/courseware-profile.md` | 配置字段、豁免规则、发布方式 |
| `references/runtime-contract.md` | 离线契约、参数契约、浏览器验证、五层检查 |
| `references/local-config.md` | 本地知识库配置与取材顺序 |
| `references/threejs-version.md` | r128 依赖记录、许可证、升级回归清单 |
| `references/delivery-checklist.md` | 交付前逐条勾选（A–J 十组） |
| `scripts/check_courseware.py` | 三层校验：静态结构 / 数据一致性 / 浏览器运行 |
| `scripts/smoke_test.py` | 可选 Playwright 冒烟测试（未安装时 SKIP） |
| `tests/test_checker.py` | 校验脚本的故障样例回归（10 个用例） |
| `assets/courseware-shell.html` | 可运行外壳模板（含 JSON 数据块与五态语音） |
| `assets/courseware-profile.example.json` | 配置样例 |

## 使用

在对话里说：

- 「按课件交付标准做 S-02 ×××」
- 「按第一个课件的标准改这个课件」
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
| 通用底线 | 科学准确、简化有说明、数据同源、交互可用、离线可运行、文档一致、发布授权 | 否 |
| 类型专属 | 过程型阶段数组/曲线；解剖型爆炸视图/剖切；实验型滑杆/对照；对比型双场景/差异高亮 | 按类型 |
| 可选配置 | `voiceMode` / `quantityChart` / `interactionLevel` / `publishMode` / `params` | 是，需写明理由 |

## 兼容性

- 主要目标：WorkBuddy / CodeBuddy 技能加载器（`SKILL.md` + `references/` + `scripts/` + `assets/`）
- 元数据：`name` / `description` / `version` / `agent_created` / `allowed-tools`
- 脚本：Python 3.9+；`check_courseware.py` 的 JS 数据回退需要 Node.js（仅用于解析 `const STAGES`）
- 浏览器冒烟：Playwright + Chromium（可选，不装则跳过）
- 未在其他技能加载器上逐项验证；如需移植，请先核对其 frontmatter 字段要求

## 许可证

未指定许可证，默认保留所有权利。如需以 MIT、CC BY-NC 等协议开源，请先与作者确认后补充 `LICENSE`。

## 版本

v1.1.0 · 2026-10-29 · 变更见 [CHANGELOG.md](CHANGELOG.md)
