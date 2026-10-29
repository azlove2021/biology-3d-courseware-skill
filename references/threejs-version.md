# 依赖记录：Three.js 与运行时

## 1. 版本

| 项 | 值 |
|---|---|
| 库 | three.js |
| 版本 | **r128**（UMD 构建） |
| 文件 | `libs/three.min.js`（约 590 KB） |
| 来源 | `https://unpkg.com/three@0.128.0/build/three.min.js` |
| 许可证 | MIT（three.js 官方仓库） |
| 加载方式 | 本地 `<script src="libs/three.min.js">`，CDN 仅 JS 兜底 |

## 2. 为什么锁 r128

- UMD 构建可直接 `<script>` 引入，不需要 importmap / 构建工具
- 单 HTML + 本地 libs 即可双击离线运行，符合交付硬要求
- 自定义轨道相机控制器不依赖 addons，避免额外文件
- 教学课件用到的 API（Scene / Mesh / ShaderMaterial / CanvasTexture 等）在 r128 已稳定

r128 不是最新版，这是**有意识的兼容性决策**，不要为了追新而升级。

## 3. 已测试环境

| 浏览器 | 结果 |
|---|---|
| Chrome / Edge（Windows，近两年版本） | 通过 |
| Firefox（桌面） | 预期通过，未逐版本回归 |
| Safari（macOS / iOS） | 预期通过，未逐版本回归 |

移动端：`devicePixelRatio` 上限 2，粒子/实例数量需控制。

## 4. 升级前的回归清单

升级 three.js 前，至少用 4 类课件各跑一遍：

1. 时间轴/过程型（S-01 减数分裂）
2. 结构/解剖型
3. 实验/模拟型
4. 对比型

并检查：

- [ ] 离线双击可打开
- [ ] 材质、光照、阴影无异常
- [ ] 自定义相机拖拽/缩放正常
- [ ] CanvasTexture / CSS2D 标签定位正常
- [ ] 移动端帧率可接受
- [ ] `check_courseware.py` 与 `smoke_test.py` 均通过

## 5. 第三方依赖清单

| 依赖 | 用途 | 许可证 | 是否随包 |
|---|---|---|---|
| three.js r128 | 3D 渲染 | MIT | 是（`libs/three.min.js`） |
| 浏览器 `speechSynthesis` | 语音朗读 | 平台能力 | 否（浏览器内置） |
| Playwright（可选） | 冒烟测试 | Apache-2.0 | 否（仅开发环境） |

除上述外，课件不应引入其他第三方库；字体使用系统字体（Microsoft YaHei / PingFang SC）。
