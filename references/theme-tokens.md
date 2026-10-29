# 主题与排版规范（锁定）

所有课件沿用同一套设计语言。**只允许改主强调色**，其余 token、背景、布局、圆角、阴影、断点一律不动。

## 1. 语义色板

```css
:root{
  /* 语义色：全系列通用，不要改 */
  --red:#ef4444;    /* 父源 / 阳性 / 警示 */
  --blue:#3b82f6;   /* 母源 / 对照 */
  --purple:#7c3aed; /* 结构 / 四分体 / 主结构 */
  --cyan:#06b6d4;   /* 纺锤丝 / 过程 / 辅助 */
  --orange:#f59e0b; /* 易错点 / 注意 */
  --ink:#1e293b;    /* 正文 */
  --muted:#64748b;  /* 次要文字 */
  --line:#e2e8f0;   /* 描边 */
  /* 主强调色：每课可换，见下表 */
  --accent:#7c3aed;
  --accent2:#06b6d4;
}
```

**颜色语义必须写进图例**，并注明「颜色仅用于区分来源/结构，非真实颜色」。

## 2. 每课主色映射（只改这两个变量）

| 主题域 | --accent | --accent2 | 适用 |
|---|---|---|---|
| 减数分裂 / 遗传规律 | `#7c3aed` 紫 | `#06b6d4` 青 | S-01、分离定律、自由组合 |
| 光合 / 呼吸 / 代谢 | `#16a34a` 绿 | `#06b6d4` 青 | 光合作用、细胞呼吸、酶 |
| 细胞结构 / 物质运输 | `#2563eb` 蓝 | `#7c3aed` 紫 | 细胞器、膜运输、细胞核 |
| 发酵 / 工程 / 技术 | `#ea580c` 橙 | `#0891b2` 深青 | 发酵工程、基因工程 |
| 稳态 / 调节 | `#9333ea` 紫红 | `#e11d48` 玫红 | 神经调节、体液调节、免疫 |
| 生态 / 种群 | `#059669` 绿 | `#0ea5e9` 天蓝 | 种群、群落、生态系统 |

> 换色后必须同步改 `.c1/.c2/.c3` 三张读数卡与曲线颜色，保持同域一致。

## 3. 背景配方（禁止纯白大平面）

```css
body{
  margin:0;color:var(--ink);overflow:hidden;
  font:14px/1.7 "Microsoft YaHei","PingFang SC",sans-serif;
  background:#f6f9ff;
}
.bg{position:fixed;inset:0;z-index:0;pointer-events:none;overflow:hidden}
.bg::before{
  content:'';position:absolute;inset:-20%;
  background:
    radial-gradient(38% 42% at 16% 12%, rgba(196,181,253,.55), transparent 70%),
    radial-gradient(42% 46% at 86% 18%, rgba(125,211,252,.55), transparent 72%),
    radial-gradient(46% 50% at 74% 88%, rgba(167,243,208,.42), transparent 72%),
    radial-gradient(40% 44% at 10% 84%, rgba(251,207,232,.40), transparent 72%),
    linear-gradient(135deg,#fbfdff 0%,#f2f7ff 45%,#f6fbff 100%);
}
.bg::after{
  content:'';position:absolute;inset:0;
  background-image:radial-gradient(rgba(99,102,241,.20) 1px, transparent 1px);
  background-size:22px 22px;
  mask-image:radial-gradient(ellipse 75% 65% at 50% 45%, #000 30%, transparent 78%);
  -webkit-mask-image:radial-gradient(ellipse 75% 65% at 50% 45%, #000 30%, transparent 78%);
  opacity:.55;
}
.blob{position:absolute;border-radius:50%;filter:blur(60px);opacity:.55;animation:float 18s ease-in-out infinite}
.blob.b1{width:420px;height:420px;left:-120px;top:-140px;background:#ddd6fe}
.blob.b2{width:360px;height:360px;right:-100px;top:6%;background:#bae6fd;animation-delay:-6s}
.blob.b3{width:320px;height:320px;left:38%;bottom:-160px;background:#bbf7d0;animation-delay:-11s}
@keyframes float{0%,100%{transform:translate3d(0,0,0) scale(1)}50%{transform:translate3d(18px,-22px,0) scale(1.06)}}
```

## 4. 布局骨架

```
#app (flex column, height 100%)
├─ header  高约 56px：mark + 标题/副标题 + badge + spacer + 语音/简洁/全屏/复位/重置
├─ main (flex:1, flex row, min-height:0)
│  ├─ #stage (flex:1, position:relative)
│  │   ├─ #labels（投影标签层）
│  │   ├─ .rail（顶部阶段导航，按大阶段分组，组间 .sep）
│  │   ├─ .hud.tl（左上：模型名 + 起点→终点 + 非真实比例）
│  │   ├─ .hud.tr（右上：示意 chip）
│  │   ├─ .hud.bl（左下：图例 + 颜色说明）
│  │   └─ .hud.br（右下：操作提示）
│  └─ aside 宽 372px：六张 .card
└─ footer：播放/暂停 + 上一/下一 + 时间轴 + 开关 + 速度
```

- `aside` 宽 **372px**（≤1180px 收窄到 330px）
- 卡片：`border-radius:14px`，`box-shadow:0 5px 18px rgba(30,41,59,.055)`
- 按钮：`border-radius:10px`；主按钮用 `linear-gradient(135deg,var(--accent),var(--accent2))`
- 圆角体系：卡片 14 / 按钮 10 / 标签 999 / 读数卡 11

## 5. 右侧面板六块（顺序固定）

| # | 卡片 | 内容 | 视觉标记 |
|---|---|---|---|
| 1 | 阶段标题 + 讲解 | 阶段名、副标题、旁白、朗读按钮 + 自动朗读 + 语速 | `.narration` 左侧 3px 紫色竖线 |
| 2 | 实时读数 | 染色体 / DNA / 染色单体 三色卡 + 口径说明 + 细胞数 | `.c1` 紫、`.c2` 青、`.c3` 橙 |
| 3 | 数量曲线 | 三条折线（染色体/DNA/染色单体），当前阶段游标 | 高 96px，图例在右上 |
| 4 | 本时期要点 | 折叠 `<details>`，避免一屏堆字 | 默认收起 |
| 5 | 易错点 | 橙底卡片 `#fffdf7 → #fffbeb`，左侧 4px 橙边 | `.warn` |
| 6 | 观察任务 | 绿底卡片 `#f7fffd → #effcf9`，左侧 4px 绿边 | `.task` |

## 6. 响应式

```css
@media(max-width:1180px){ aside{width:330px} .rail button{padding:5px 7px;font-size:11px} }
@media(max-width:980px){
  main{flex-direction:column;min-height:0}
  #stage{flex:1 1 auto;min-height:42vh}
  aside{display:block;position:static;width:auto;max-height:46vh;
    border-left:0;border-top:1px solid var(--line);box-shadow:none}
  .hud.br{display:none}
  .rail{max-width:calc(100% - 24px);overflow-x:auto}
}
```

**≤980px 必须上下堆叠**，不允许把讲解面板直接隐藏。

## 7. 简洁模式（投影必备）

```css
body.simple .blob{display:none}
body.simple .bg::after{display:none}
body.simple .bg::before{background:#f8fbff}
body.simple .card{box-shadow:none}
```

按钮文案：`◐ 简洁模式` ↔ `◑ 关闭简洁`。

## 8. 字体与动效

- 字体：`"Microsoft YaHei","PingFang SC",sans-serif`；正文 14px / 1.7
- 阶段名 21px / 800；副标题 12px；旁白 12.5px / 1.75
- 过渡统一 `.15s`；卡片不跳动；3D 相机缓动 `lerp(…, min(1, dt*3.2))`
- 禁止：大面积纯白、纯黑、荧光色、超过 3 种强调色同屏
