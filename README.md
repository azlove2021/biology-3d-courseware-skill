# 高中生物 3D 课件交付标准（WorkBuddy 技能）

把「S-01 减数分裂全流程时间轴」验证过的交付方式固化为可复用技能。后续每个课件在**主题、语音、排版、专业性**上与第一个保持同一水准。

- 📦 技能仓库：<https://github.com/azlove2021/biology-3d-courseware-skill>

## 这个技能解决什么

- 新做高中生物 3D 交互课件时，不再每次重新发明页面结构、配色、语音同步方式
- 用一套机械校验脚本兜住"看起来差不多、其实漏了"的问题
- 把"人教版口径、数量自检、统计口径、示意声明"变成硬门槛，而不是靠记忆

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
| `SKILL.md` | 10 条交付铁律 + 8 步执行流程 + 常见坑 |
| `references/theme-tokens.md` | 锁定色板、背景、布局、响应式、简洁模式、每课主色映射 |
| `references/voice-sync.md` | hold→朗读→morph 状态机与完整代码 |
| `references/stage-schema.md` | 阶段数据结构、数量自检表模板、URL 书签 |
| `references/terms.md` | 术语口径与禁用表述速查 |
| `references/courseware-types.md` | 时间轴 / 解剖 / 实验 / 对比四类范式 |
| `references/delivery-checklist.md` | 交付前逐条勾选（A–I 九组） |
| `scripts/check_courseware.py` | 机械校验：离线依赖、主题、语音、文档、术语 |
| `assets/courseware-shell.html` | 符合主题基线的可运行外壳 |

## 使用

在对话里说：

- 「按课件交付标准做 S-02 ×××」
- 「按第一个课件的标准改这个课件」
- 「检查这个课件是否符合交付标准」

或手动跑校验：

```bash
python scripts/check_courseware.py "<项目目录>"
```

- 退出码 `0`：通过（可能有警告）
- 退出码 `1`：存在阻断项

## 核心硬门槛

1. 单 HTML + 本地 `libs/three.min.js`，双击离线可用
2. 白色/明亮底 + 鲜艳强调色，只换主强调色
3. 右侧六块面板：讲解 → 读数 → 曲线 → 要点 → 易错点 → 观察任务
4. 人教版 2019，每阶段标教材小节
5. 染色体 / DNA / 染色单体 / 细胞数 + 统计口径，图表与数字同源
6. 语音 hold→朗读→morph，讲完一段再进下一阶段
7. README + 修改记录 + preview.png
8. 校验通过后自动发布 GitHub Pages

## 参考实现

- 课件仓库：<https://github.com/azlove2021/meiosis-3d-courseware>
- 在线预览：<https://azlove2021.github.io/meiosis-3d-courseware/>
- 自检结果：0 阻断 / 0 警告

## 版本

v1.0.0 · 2026-10-29
