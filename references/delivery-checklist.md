# 交付前检查清单

逐条勾选，不跳项。阻断项不过，不得交付。

## A. 立项与取材

- [ ] 目录为 `NNN_project_项目名/`，自包含，未散放
- [ ] 已查点子计划表，确认编号 / 类型 / 优先级
- [ ] 已读知识库梳理文档，提取教材依据、数量关系、术语、易错点
- [ ] 教材依据到**小节级**；不确定的已问用户，未臆造页码

## B. 数据

- [ ] `STAGES` 字段齐全（`n/short/phase/s/v/f/c/cells/scope/cn/w/q/tb`）
- [ ] 数量自检表逐行算通，与 `c` 完全一致
- [ ] 图表数据由 `STAGES` 派生，x 轴未写死
- [ ] 统计口径逐阶段标注，无空白

## C. 外壳与主题

- [ ] 使用锁定色板；只改了 `--accent` / `--accent2`
- [ ] 背景为渐变 + 光斑 + 点阵 + blob，非纯白大平面
- [ ] 六块面板顺序正确（讲解→读数→曲线→要点→易错点→观察任务）
- [ ] 顶部/底部控制齐全（语音、简洁、全屏、复位、重置、播放、单步、时间轴）
- [ ] ≤980px 上下堆叠，讲解未被隐藏
- [ ] 简洁模式可一键降噪

## D. 专业性

- [ ] 顶部标「人教版 2019 + 章节」
- [ ] 每阶段标教材小节
- [ ] 页面有「示意 · 非真实比例」
- [ ] 颜色注明「仅用于区分来源/结构」
- [ ] 术语符合 `terms.md`，无禁用表述
- [ ] 未编造显微尺寸 / 实验数据 / 页码

## E. 语音

- [ ] `speechSynthesis` + `zh-CN`
- [ ] hold→朗读→morph 状态机（非固定时长硬推）
- [ ] 语速估算与 `utterance.rate` 同源
- [ ] 切段 `cancel()`，有 token 守卫
- [ ] 首次点击后解锁发声
- [ ] `?voice=0` 可关闭
- [ ] 无中文语音时有提示

## F. 技术

- [ ] 单 HTML + `libs/three.min.js` 本地副本
- [ ] 双击离线可打开（断网测试）
- [ ] CDN 仅兜底，顺序 unpkg → staticfile → jsdelivr
- [ ] 无构建工具、无 ESM/importmap、无 addons
- [ ] 自写轨道相机，拖拽/缩放正常
- [ ] `node --check` 内联脚本通过
- [ ] `python scripts/check_courseware.py "<目录>"` 阻断项为 0

## G. 文档

- [ ] `README.md`：打开方式、模型口径、阶段表、操作表、URL 参数、文件树
- [ ] `修改记录.md`：改了什么、为什么、验证记录、已知简化
- [ ] `preview.png`：首屏截图，清晰可辨
- [ ] README 与课件实际行为一致（尤其语音播放规则）

## H. 发布

- [ ] `git init` + `commit`
- [ ] `gh repo create <英文仓库名> --public --source . --remote origin --push`
- [ ] 启用 Pages：`gh api repos/<owner>/<repo>/pages -X POST -f source[branch]=main -f source[path]=/`
- [ ] 补 `index.html` 门户页，根地址直达课件
- [ ] 验证 root / 课件 / `libs/three.min.js` 均返回 200
- [ ] README 顶部补在线地址与仓库地址

## I. 交付说明（回复用户时）

- [ ] 一句话说清做了什么、在哪
- [ ] 给出本地路径 + 在线地址
- [ ] 说明如何验证（点播放、开语音）
- [ ] 列出已知简化 / 待确认项
