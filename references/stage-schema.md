# 阶段数据结构与数量自检

## 1. 原则

**数据先行，单一数据源**：先把阶段数据写完整、把数量表算通，再写 3D 与交互。数字不通，动画一定错。

图表曲线、右侧读数、时间轴刻度、README 数量表、校验脚本，全部从**同一份结构化数据**派生；不允许在 HTML、绘图函数、README 里各写一套数字。

> 旁白是自然语言，脚本无法可靠地从旁白里解析生物学含义。关键数字与机制必须落在结构化字段里，不要靠"旁白里出现了数字"来证明正确。

## 2. 结构化数据块（唯一数据源）

在 HTML 中内嵌一段 JSON，保持单文件离线：

```html
<script type="application/json" id="courseware-data">
{
  "meta": {
    "title": "减数分裂 · 全流程时间轴",
    "textbook": "人教版 2019",
    "chapter": "必修2 第2章第1节",
    "type": "process",
    "simplifications": ["非真实比例", "颜色仅用于区分亲本来源"]
  },
  "stages": [
    {
      "id": "interphase-before",
      "name": "间期 · 复制前",
      "short": "复制前",
      "group": "间期",
      "summary": "DNA 尚未复制",
      "narration": "本模型从一个初级精母细胞开始。间期复制前，细胞内有 4 条染色体，每条染色体只含 1 个 DNA 分子，没有姐妹染色单体。",
      "events": ["染色体呈细长的染色质丝", "每条染色体只含 1 个 DNA", "没有姐妹染色单体"],
      "counts": { "chromosome": 4, "dna": 4, "chromatid": 0 },
      "cells": 1,
      "scope": "每个细胞",
      "warning": "复制前没有姐妹染色单体，染色单体数为 0，不要与复制后混淆。",
      "question": "复制前，一条染色体含几个 DNA、几条染色单体？",
      "source": "必修2 第2章第1节",
      "visualState": "chromatin-thin"
    }
  ]
}
</script>
```

读取方式：

```js
const DATA = JSON.parse(document.getElementById('courseware-data').textContent);
const STAGES = DATA.stages.map(s => ({
  ...s,
  n: s.name, short: s.short, phase: s.group,
  s: s.summary,
  v: s.narration,
  f: s.events,
  c: [s.counts.chromosome, s.counts.dna, s.counts.chromatid],
  tb: s.source,
  w: s.warning,
  q: s.question
}));
```

## 3. 字段规范

| 字段 | 必填 | 类型 | 说明 |
|---|---|---|---|
| `id` | ✅ | string | 稳定标识，唯一，用于校验与书签 |
| `name` | ✅ | string | 阶段全名，与教材一致 |
| `short` | ✅ | string | ≤4 字，时间轴按钮用 |
| `group` | ✅ | string | 大阶段归类，用于分组与配色 |
| `summary` | ✅ | string | 一句话概括，≤30 字 |
| `narration` | ✅ | string | 旁白，60–120 字，口语化 |
| `events` | ✅ | string[] | 2–4 条核心事件 |
| `counts.chromosome` | ✅ | int ≥0 | 染色体数 |
| `counts.dna` | ✅ | int ≥0 | DNA 数 |
| `counts.chromatid` | ✅ | int ≥0 | 染色单体数 |
| `cells` | ✅ | int ≥1 | 当前统计的细胞数 |
| `scope` | ✅ | string | 统计口径，不能空 |
| `warning` | ✅ | string | 易错点，必须具体 |
| `question` | ✅ | string | 观察任务，能在画面上找到答案 |
| `source` | ✅ | string | 教材小节，如 `必修2 第2章第1节` |
| `visualState` | 建议 | string | 对应可视化状态，便于程序断言 |
| `simplifications` | 建议 | string[] | 该阶段采用的简化假设 |

## 4. 示例必须写清阶段与口径

下面三段是**减数分裂**示例，不要当成所有过程的通用答案：

| # | 阶段 | 染色体 | DNA | 染色单体 | 细胞数 | 统计口径 |
|---|---|---|---|---|---|---|
| 1 | 间期·复制前 | 4 | 4 | 0 | 1 | 每个细胞 |
| 2 | 间期·复制后 | 4 | 8 | 8 | 1 | 每个细胞 |
| 3 | 末期Ⅱ | 2 | 2 | 0 | **4** | **每个子细胞** |

- 第 3 段是"末期Ⅱ 结束"，已形成 **4 个精细胞**，每个含 **2 条染色体**；`cells` 必须是 4，不是 2。
- 如果只想表达"减数第一次分裂结束"，应写"末期Ⅰ"：每个子细胞 2 条染色体、4 个 DNA、4 条染色单体，`cells:2`。
- 不要把"末期Ⅰ"和"末期Ⅱ"混成一个示例。

## 5. 校验规则（脚本会执行）

- `stages` ≥ 2；`id` 不重复
- `name` / `scope` / `source` / `narration` 非空
- `counts` 三项均为非负整数
- `cells` 为正整数
- `counts.chromatid` 只能是 `0` 或 `2 × counts.chromosome`（否则警告）
- `counts.dna` 不应小于 `counts.chromosome`（否则警告）
- README 数量表行数 = 阶段数，且逐行数字一致（不一致为阻断）
- 图表必须从 `STAGES` / `DATA.stages` 派生，不能出现独立的字面量数组

## 6. 主题不变量与例外

不要用一条公式套所有过程。开工前先写下该主题的不变量：

| 主题 | 不变量 | 例外 / 易错 |
|---|---|---|
| 减数分裂 | 染色体数在后期Ⅱ着丝粒分裂时**暂时加倍**；DNA 在复制后加倍；染色单体为 0 或 2×染色体 | 末期Ⅰ减半是"同源染色体分到两个细胞"，不是着丝粒分裂 |
| 有丝分裂 | 后期着丝粒分裂，染色体暂时加倍；末期恢复 | 不要与减数第二次分裂混淆 |
| 光合 / 呼吸 | 速率类指标（总光合、净光合、呼吸速率）不是"个数"，用 `rate` 字段而非 `counts` | 净光合 = 总光合 − 呼吸 |
| 结构 / 解剖 | 部件数量与层级固定，`counts` 可省略 | 用部件树而非阶段数组 |
| 实验 / 模拟 | 自变量、因变量、对照组 | 结论必须随数据变化，不能写死 |

`counts` 只适用于"有时间轴、可计数"的过程型课件；解剖型、实验型用各自的 `parts` / `variables` 数据结构（见 `courseware-types.md`）。

## 7. README 数量自检表（必附）

```markdown
| # | 阶段 | 染色体 | DNA | 染色单体 | 细胞数 | 统计口径 | 教材依据 |
|---|---|---|---|---|---|---|---|
| 1 | 间期·复制前 | 4 | 4 | 0 | 1 | 每个细胞 | 必修2 第2章第1节 |
| 2 | 间期·复制后 | 4 | 8 | 8 | 1 | 每个细胞 | 必修2 第2章第1节 |
```

- 行数 = 阶段数，一行不漏
- 数字必须与 `stages[i].counts` 完全一致
- 「后期」着丝粒分裂后单独成行；「末期」胞质分裂后 `scope` 与 `cells` 必须跟着改

## 8. 图表数据

```js
const SERIES = [
  { name:'染色体', color:'#7c3aed', data: STAGES.map(s => s.c[0]) },
  { name:'DNA',    color:'#06b6d4', data: STAGES.map(s => s.c[1]) },
  { name:'染色单体', color:'#f59e0b', data: STAGES.map(s => s.c[2]) }
];
// x 轴：i / (data.length - 1)，不要写死 /8
```

## 9. 相机帧位

```js
const FRAME = [9.1, 9.1, 8.6, 8.4, 9.3, 10.4, 10.4, 10.2, 11.0, 11.9]; // 每阶段镜头半径
cam.rGoal = FRAME[idx];
```

## 10. URL 参数（课堂书签）

| 参数 | 含义 | 取值 / 默认 | 非法值处理 | 适用范围 |
|---|---|---|---|---|
| `t` | 定位阶段 | `0 .. N-1`，默认 `0` | `NaN`→0；负数/超界→夹紧 | 所有过程型 |
| `voice` | 语音开关 | `1` / `0`，默认 `1` | 其他值按 `1` | 有语音的课件 |
| `simple` | 简洁模式 | `1` / `0`，默认 `0` | 其他值按 `0` | 所有 |
| `xo` | 交叉互换演示 | `1` / `0`，默认 `0` | 其他值按 `0` | 仅相关课件 |
| `arr` | 排列方式 | `0` / `1`，默认 `0` | 其他值按 `0` | 仅支持切换的课件 |
| `panel` | 移动端面板 | `1` / `0`，默认 `0` | 未实现时**不要写进文档** | 仅实现后 |

解析时必须夹紧：

```js
t = Math.min(N-1, Math.max(0, parseFloat(q.get('t')) || 0));
```

未实现的参数不要写进 README，避免"文档说有、代码没有"。
