# 交付前检查清单

逐条勾选，不跳项。阻断项不过，不得交付。

## A. 立项与配置

- [ ] 目录为 `NNN_project_项目名/`，自包含，未散放
- [ ] 已查点子计划表，确认编号 / 类型 / 优先级
- [ ] `courseware-profile.json` 存在，`type` 与课件类型一致
- [ ] `voiceMode` / `quantityChart` / `interactionLevel` 合理
- [ ] 任何豁免（如 `voiceMode: disabled`）都写明了理由
- [ ] `publishMode` 明确（默认 `local`）

## B. 取材与专业性

- [ ] 按 `local-config.md` 的优先级取材，未硬编码本机路径
- [ ] 教材依据到**小节级**；不确定的已标"待核实"
- [ ] 未编造页码、显微尺寸、实验数据
- [ ] 术语符合 `terms.md`，无禁用表述
- [ ] 页面有「示意 · 非真实比例」
- [ ] 颜色注明「仅用于区分来源/结构」
- [ ] 顶部标「人教版 2019 + 章节」

## C. 数据（单一数据源）

- [ ] 有 `<script type="application/json" id="courseware-data">`
- [ ] `stages` 字段齐全：`id/name/short/group/summary/narration/events/counts/cells/scope/warning/question/source`
- [ ] `id` 不重复
- [ ] `counts` 为 3 个非负整数；染色单体为 0 或 2×染色体
- [ ] `cells` ≥ 1；`scope` / `source` 非空
- [ ] README 数量表行数 = 阶段数，逐行数字一致
- [ ] 图表由 `STAGES` / `DATA.stages` 派生，x/y 轴未写死
- [ ] 末期Ⅰ与末期Ⅱ分开，未混成一个示例

## D. 主题与布局

- [ ] 使用锁定色板；只改了 `--accent` / `--accent2`
- [ ] 背景为渐变 + 光斑 + 点阵 + blob，非纯白大平面
- [ ] 六块面板顺序正确（讲解→读数→曲线→要点→易错点→观察任务）
- [ ] 顶部/底部控制齐全（语音、简洁、全屏、复位、重置、播放、单步、时间轴）
- [ ] ≤980px 上下堆叠，讲解未被隐藏
- [ ] 简洁模式可一键降噪

## E. 3D 与交互

- [ ] 程序化建模，不依赖外部模型文件
- [ ] 对象命名并挂 `userData`
- [ ] 自写轨道相机，拖拽/缩放正常
- [ ] 点击结构有高亮/说明
- [ ] 课件特有交互（交叉互换/排列/剖切/参数滑杆）可用
- [ ] 像素比上限 2；移动端帧率可接受

## F. 语音（五态）

- [ ] 使用 `voiceState`：`pending / speaking / ended / cancelled / error`
- [ ] 每条语音有 `voiceToken`，过期回调被忽略
- [ ] 只有 `ended && voiceStage === stageIdx` 才进入 morph
- [ ] 没有用 `if(!speaking)` 判断结束
- [ ] 切段/拖时间轴/关闭语音/重置都调用 `cancelVoice()`
- [ ] `onerror` 有 800ms 兜底；另有 `estVoiceDur+3s` 总超时
- [ ] 首次点击页面后才发声
- [ ] 无中文语音时有提示，不静默失败
- [ ] 语速估算与 `utterance.rate` 同源
- [ ] `?voice=0` 可关闭

## G. 离线与运行

- [ ] 单 HTML + `libs/three.min.js` 本地副本
- [ ] HTML/CSS 无外链（CDN 只作为 JS 兜底）
- [ ] **断网后**双击仍可完整运行
- [ ] 本地资源缺失时有清晰错误提示
- [ ] `node --check` 内联脚本通过
- [ ] `check_courseware.py` 阻断项为 0
- [ ] 改了模板/脚本后跑过 `tests/test_checker.py`
- [ ] 可选：`smoke_test.py --offline` 通过，截图已抽查
- [ ] README 区分「离线验证通过」与「联网预览通过」

## H. 文档

- [ ] `README.md`：打开方式、模型口径、阶段表、操作表、URL 参数、文件树
- [ ] `修改记录.md`：改了什么、为什么、验证记录、已知简化
- [ ] `preview.png`：首屏截图，清晰可辨
- [ ] README 与课件实际行为一致（尤其语音播放规则、参数列表）

## I. 发布

- [ ] 按 `publishMode` 执行；`local` 时不擅自建远程仓库
- [ ] 发布前扫描密钥、个人信息、内部文件、未授权素材
- [ ] 用户已授权公开；私有仓库未被擅自改公开
- [ ] 已告知哪些内容上传、哪些留在本地
- [ ] Pages 验证 root / 课件 / `libs/three.min.js` 均 200

## J. 人工验收（五层）

- [ ] 数据：数值、阶段顺序、统计口径正确
- [ ] 结构：对象数量、层级、身份正确
- [ ] 过程：各阶段运动符合生物学过程
- [ ] 界面：画面、旁白、数据指向同一阶段
- [ ] 教学：学生能从画面看出要理解的机制
