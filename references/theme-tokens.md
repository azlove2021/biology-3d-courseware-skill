# 主题与排版规范（玻璃拟态教学驾驶舱）

设计语言参考 **铜匠实验室**（<https://lab.tongjiang.app>，CC BY-NC 4.0）的公开课件。**只借鉴布局、配色与组件语言，不复制其课件代码、文案与素材。**

核心特征：**浅色 3D 场景 + 悬浮玻璃面板 + 顶部因果链 + 左侧本步脚本 + 右侧中控台 + 底部步骤条**。所有面板半透明白、带背景模糊与柔和蓝紫阴影，信息密度高但不拥挤。

## 1. 核心 token

```css
:root{
  --font:"PingFang SC","Microsoft YaHei","Noto Sans CJK SC","Source Han Sans SC","Hiragino Sans GB",system-ui,sans-serif;
  --num:"SF Pro Display","DIN Alternate","Helvetica Neue","PingFang SC",system-ui,sans-serif;

  /* 玻璃面板 */
  --glass:rgba(255,255,255,.84);
  --glass-bar:rgba(255,255,255,.72);
  --glass-2:rgba(255,255,255,.76);
  --glass-back:rgba(255,255,255,.95);
  --glass-solid:rgba(255,255,255,.92);
  --glass-blur:blur(12px) saturate(150%);
  --glass-edge:1px solid rgba(255,255,255,.75);
  --glass-glow:inset 0 1px 0 rgba(255,255,255,.9);

  /* 阴影与描边 */
  --shadow-1:0 2px 8px rgba(30,50,110,.08);
  --shadow-2:0 10px 32px rgba(30,50,110,.14);
  --tint:#F3F7FF;
  --line:rgba(14,26,43,.08);
  --line-2:rgba(14,26,43,.25);
  --line-soft:rgba(14,26,43,.06);

  /* 文字 */
  --ink:#0E1A2B; --ink2:#43526A; --ink3:#56627A;

  /* 主色 / 状态色（只做面、条、点、图标） */
  --sci:#2F6BFF; --cyan:#13B8C6; --violet:#7C5CFF;
  --grad:linear-gradient(100deg,#2F6BFF 0%,#13B8C6 100%);
  --grad-soft:linear-gradient(100deg,rgba(47,107,255,.12) 0%,rgba(19,184,198,.12) 100%);
  --ok:#10B981; --warn:#F59E0B; --bad:#EF4444;
  --heat:linear-gradient(90deg,#F59E0B,#EF4444);

  /* 主色透明度梯度 */
  --sci-30:rgba(47,107,255,.30); --sci-12:rgba(47,107,255,.12);
  --sci-8:rgba(47,107,255,.08);  --sci-4:rgba(47,107,255,.04);
  --ok-12:rgba(16,185,129,.12);  --warn-10:rgba(245,158,11,.10);
  --bad-12:rgba(239,68,68,.12);

  /* 形状 */
  --r-panel:16px; --r-card:12px; --r-ctrl:10px; --r-pill:999px;

  /* 尺寸 */
  --top-h:78px; --steps-h:46px; --foot-h:52px;
  --panelw-l:clamp(320px,22vw,404px);
  --panelw-r:clamp(300px,20.5vw,348px);
  --fs-main:34px; --fs-sub:20px; --fs-t:13px; --fs-b:13px; --fs-xs:12px;
}
```

## 2. 单元色系统

每门课 2–5 个「单元」，每个单元一组颜色。只改 `--uc / --ucs / --ucg / --ucsg / --uh` 五个变量，组件自动跟随。

| 单元 | `--uc` 主色 | `--ucs` 深色 | `--uh` 光晕 |
|---|---|---|---|
| 青（细胞核/转录） | `#0D7A8C` | `#0B6979` | `rgba(13,122,140,.10)` |
| 蓝（细胞质/翻译） | `#2F6BFF` | `#1E4FD6` | `rgba(47,107,255,.08)` |
| 紫（分子细节） | `#9333EA` | `#7C2BC4` | `rgba(147,51,234,.10)` |
| 橙（实验/操作） | `#D97706` | `#B45309` | `rgba(217,119,6,.10)` |
| 绿（结论/生态） | `#057A55` | `#046A4A` | `rgba(5,122,85,.10)` |

```css
.unit-1{--uc:#0D7A8C;--ucs:#0B6979;--ucg:linear-gradient(100deg,#0D7A8C,#13B8C6);--uh:rgba(13,122,140,.10)}
.unit-2{--uc:#2F6BFF;--ucs:#1E4FD6;--ucg:var(--grad);--uh:var(--sci-8)}
.unit-3{--uc:#9333EA;--ucs:#7C2BC4;--ucg:linear-gradient(100deg,#9333EA,#7C5CFF);--uh:rgba(147,51,234,.10)}
```

## 3. 玻璃面板配方

```css
.panel{
  background:var(--glass);
  border:var(--glass-edge);
  border-radius:var(--r-panel);
  box-shadow:var(--shadow-2),var(--glass-glow);
  backdrop-filter:var(--glass-blur);
  -webkit-backdrop-filter:var(--glass-blur);
}
```

- 顶部栏/底部栏用 `--glass-bar`（更透，72%）
- 浮层/弹窗用 `--glass-back`（95%，保证可读）
- **低帧率降级**：`body.lowfps .panel{background:var(--glass-solid);backdrop-filter:none}`

## 4. 字体与字号

- 正文 13px / 1.5；辅助 12px；极小 11px
- 主标题 34px / 800（`--fs-main`）；副标题 20px（`--fs-sub`）
- 面板标题 13px / 700；读数数字 20–28px，用 `--num` + `font-variant-numeric:tabular-nums`
- 步骤号 20px / 800；因果链标签 12px / 650
- 不用衬线体；不写超长段落，单行 ≤ 28 个汉字

## 5. 组件

### 按钮

```css
.btn{
  appearance:none;border:1px solid var(--line);background:var(--glass);
  border-radius:var(--r-ctrl);padding:5px 9px;line-height:1.1;color:var(--ink);
  display:inline-flex;align-items:center;gap:5px;white-space:nowrap;
  backdrop-filter:var(--glass-blur);
}
.btn:hover{border-color:var(--sci);background:var(--sci-4)}
.btn.pri{background:var(--grad);border-color:transparent;color:#fff;box-shadow:0 2px 10px var(--sci-30)}
.btn.on{background:var(--grad);border-color:transparent;color:#fff}
.btn.done{background:var(--ok-12);border-color:rgba(16,185,129,.35);color:#047857}
.btn.warn{background:var(--warn-10);border-color:rgba(245,158,11,.40);color:#9A4507}
.btn.danger{background:var(--bad-12);border-color:rgba(239,68,68,.30);color:#B91C1C}
```

### 标签 / 因果链

```css
.chip{
  display:inline-flex;align-items:center;gap:6px;
  padding:3px 9px;border-radius:var(--r-pill);
  border:1px solid var(--line);background:var(--glass);
  font-size:12px;font-weight:650;color:var(--ink2);
}
.chip .dot{width:6px;height:6px;border-radius:50%;background:var(--uc)}
.chip.on{background:var(--uh);border-color:var(--uc);color:var(--ucs)}
```

### 步骤条

```css
.steps{display:flex;align-items:center;gap:4px;padding:0 10px;height:var(--steps-h)}
.step{
  display:inline-flex;align-items:center;gap:6px;padding:4px 10px;border-radius:var(--r-pill);
  font-size:12px;color:var(--ink3);border:1px solid transparent;background:transparent;
}
.step .n{width:18px;height:18px;border-radius:50%;display:grid;place-items:center;
  font-size:11px;font-weight:800;background:var(--line-soft);color:var(--ink3)}
.step.done .n{background:var(--ok-12);color:#047857}
.step.on{background:var(--grad);color:#fff;box-shadow:0 2px 10px var(--sci-30)}
.step.on .n{background:rgba(255,255,255,.22);color:#fff}
.step .line{width:18px;height:1px;background:var(--line)}
```

### 读数卡 / 滑块

```css
.readout{background:var(--glass-2);border:1px solid var(--line);border-radius:var(--r-card);padding:8px 10px}
.readout b{display:block;font:800 22px/1.1 var(--num);color:var(--uc);font-variant-numeric:tabular-nums}
.readout span{font-size:11px;color:var(--ink3)}

.sl{display:flex;flex-direction:column;gap:5px}
.sl .top{display:flex;justify-content:space-between;font-size:12px;color:var(--ink2)}
.sl input[type=range]{appearance:none;height:6px;border-radius:3px;background:var(--line)}
.sl input[type=range]::-webkit-slider-thumb{
  appearance:none;width:18px;height:18px;border-radius:50%;
  background:var(--glass-back);border:2px solid var(--sci);box-shadow:var(--shadow-1);
}
```

### 浮动标签（3D 场景内）

```css
.tag{
  position:absolute;transform:translate(-50%,-50%);
  padding:4px 9px;border-radius:var(--r-pill);
  background:var(--glass-back);border:1px solid var(--glass-edge);
  box-shadow:var(--shadow-1);font-size:11.5px;font-weight:650;color:var(--ink2);
  white-space:nowrap;pointer-events:none;
}
```

## 6. 布局尺寸（1600×900 参考）

| 区域 | 尺寸 / 位置 |
|---|---|
| 外边距 | 四周 10px |
| 顶栏 `#top` | 左右 10px，top 6px，高 **78px**，玻璃条 |
| 因果链 | 顶栏内第二行，高约 30px |
| 步骤条 `.steps` | 左右 10px，top 90px，高 **46px** |
| 左栏 `aside.left` | left 10px，top 144px，宽 `clamp(320px,22vw,404px)`，高至底栏上方 |
| 右栏 `aside.right` | right 10px，top 144px，宽 `clamp(300px,20.5vw,348px)` |
| 中央 3D | 左栏右缘到右栏左缘，顶部步骤条下缘到底栏上缘 |
| 底栏 `.foot` | 左右 10px，bottom 10px，高 **52px** |

- 面板间距 10px；卡片内边距 10–12px
- 中央 3D 必须留出至少 **560px** 宽的可视区；小于 1100px 时左栏可折叠为抽屉
- 不出现页面滚动条；所有内容在一屏内

## 7. 背景

- 页面底色 `--tint:#F3F7FF`
- 3D 场景背景用浅色径向渐变：`radial-gradient(1200px 700px at 60% 20%, #FFFFFF, #EDF4FF 60%, #E6F0FB)`
- 可叠加极淡点阵（`radial-gradient(rgba(47,107,255,.10) 1px, transparent 1px)`，22px 网格，opacity .35）
- 禁止大面积深色、纯白、荧光色；玻璃面板后面必须有内容/渐变，否则 blur 无意义

## 8. 禁止项

- 不要复制铜匠实验室的 logo、插图、文案、课程数据
- 不要把所有面板做成不透明纯白（失去玻璃层次）
- 不要超过 3 个强调色同屏；单元色只用于该单元相关元素
- 不要用 14px 以上正文；驾驶舱信息密度高，字号过大会溢出
- 不要让 3D 场景被面板完全遮住；中央可视区是主角

## 9. 出处

- 设计语言参考：铜匠实验室 <https://lab.tongjiang.app>（CC BY-NC 4.0）
- 仅借鉴布局、配色、组件语言；代码、素材、文案均为自研
- 若对外发布，请在 README 注明「设计语言参考铜匠实验室」
