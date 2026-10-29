# 真实浏览器全流程验收（Tabbit，v1.3 起必做）

> 无头 Playwright 只能证明「代码路径没报错」。v1.2 的样板课就是在这道关里漏掉的：脚本全绿，但学生转不动、点不中、收不起面板。**交付前必须在用户已登录的真实浏览器里跑一遍完整流程并逐步截图。**

---

## 为什么用 Tabbit 而不是只用 Playwright

| 维度 | Playwright 无头 | Tabbit（登录态真机） |
|---|---|---|
| 证明「能渲染」 | ✅ | ✅ |
| 证明「手感对」 | ❌ | ✅ 真实滚轮/拖拽/双击 |
| 字体与玻璃模糊 | 可能降级 | 真实渲染 |
| 语音（speechSynthesis） | 常静音 | 有系统中文语音 |
| 投影分辨率 | 固定 viewport | 可切 1080p / 4K |
| 截图可信度 | 中 | 高（可直接放进 README） |

两者不是替代关系：`smoke_test.py` 做**回归**（每次改动都跑），Tabbit 做**验收**（交付前跑一次）。

---

## 一、准备

```bash
# Windows（Git Bash）
TB="$LOCALAPPDATA/Tabbit/LocalAgent/bin/tabbit-cli.exe"
"$TB" diagnose                     # 确认 runtime 正常
```

课件路径用绝对路径；`file://` 打不开时改用本地静态服务：

```bash
cd "<课件目录>" && python -m http.server 8765
# 浏览器访问 http://127.0.0.1:8765/index.html
```

---

## 二、逐步操作（一个 task 跑完，按需拆多个 request）

```bash
"$TB" nodejs --task "课件验收" --request-id open --timeout-ms 120000 <<'JS'
await page.goto("file:///C:/path/to/index.html", { waitUntil:"load" });
await page.waitForTimeout(1500);
return {
  title: await page.title(),
  canvas: await page.evaluate(() => {
    const c = document.querySelector('canvas');
    return c ? [c.width, c.height] : null;
  }),
  errors: await page.evaluate(() => window.__errs || [])
};
JS
```

### 1. 3D 旋转 / 缩放（必须有数值证据）

```bash
"$TB" nodejs --task "课件验收" --request-id orbit --timeout-ms 120000 <<'JS'
const box = await page.evaluate(() => {
  const c = document.querySelector('canvas').getBoundingClientRect();
  return { x: c.x + c.width/2, y: c.y + c.height/2 };
});
const before = await page.evaluate(() => camera.position.toArray());
await page.mouse.move(box.x, box.y);
await page.mouse.down();
for (let i = 1; i <= 12; i++) await page.mouse.move(box.x + i*10, box.y + i*3);
await page.mouse.up();
await page.waitForTimeout(500);
const after = await page.evaluate(() => camera.position.toArray());

const r0 = await page.evaluate(() => camera.position.distanceTo(camTgt));
await page.mouse.wheel(0, -400);
await page.waitForTimeout(600);
const r1 = await page.evaluate(() => camera.position.distanceTo(camTgt));

await page.screenshot({ path: "C:/path/shots/01-orbit.png" });
return { rotated: before.join() !== after.join(), zoomed: Math.abs(r1-r0) > .01, r0, r1 };
JS
```

### 2. 点选每个结构（逐个点，核对名称）

```bash
"$TB" nodejs --task "课件验收" --request-id pick --timeout-ms 120000 <<'JS'
const out = [];
for (const id of await page.evaluate(() => Object.keys(PICK_INFO))) {
  const pt = await page.evaluate((id) => {
    const b = new THREE.Box3().setFromObject(PICK_OBJ[id]);
    const c = b.getCenter(new THREE.Vector3()); c.project(camera);
    return { x:(c.x*.5+.5)*innerWidth, y:(-c.y*.5+.5)*innerHeight };
  }, id);
  await page.mouse.click(pt.x, pt.y);
  await page.waitForTimeout(300);
  const name = await page.evaluate(() =>
    document.getElementById('pickCard').classList.contains('on')
      ? document.getElementById('pcName').textContent : null);
  out.push({ id, name });
}
return out;
JS
```
> 有「结构速查」按钮的课件，直接点按钮更快：`page.click('#structs button[data-pick="mrna"]')`。

### 3. 面板三档 + 影院

```bash
"$TB" nodejs --task "课件验收" --request-id panels --timeout-ms 120000 <<'JS'
const r = {};
await page.click('#tgLeft');  await page.waitForTimeout(350);
r.leftHidden = await page.evaluate(() => document.body.classList.contains('hide-l'));
await page.screenshot({ path: "C:/path/shots/02-hide-left.png" });
await page.click('#tgLeft');  await page.waitForTimeout(250);

await page.click('#tgRight'); await page.waitForTimeout(350);
r.rightHidden = await page.evaluate(() => document.body.classList.contains('hide-r'));
await page.click('#tgRight'); await page.waitForTimeout(250);

await page.keyboard.press('f'); await page.waitForTimeout(500);
r.cinema = await page.evaluate(() => ({
  on: document.body.classList.contains('cinema'),
  top: getComputedStyle(document.getElementById('top')).display
}));
await page.screenshot({ path: "C:/path/shots/03-cinema.png" });
await page.keyboard.press('Escape'); await page.waitForTimeout(300);
r.exited = await page.evaluate(() => !document.body.classList.contains('cinema'));
return r;
JS
```

### 4. 语音（真机才有声）

```bash
"$TB" nodejs --task "课件验收" --request-id voice --timeout-ms 120000 <<'JS'
await page.click('#voiceBtn');            // 关掉再开，触发一次朗读
await page.waitForTimeout(200);
await page.click('#voiceBtn');
await page.waitForTimeout(1200);
return await page.evaluate(() => ({
  speaking: window.speechSynthesis.speaking,
  voiceState,                              // 五态：pending/speaking/ended/cancelled/error
  zhVoice: !!speechSynthesis.getVoices().find(v => /zh/i.test(v.lang))
}));
JS
```
> 无头浏览器常年 `speaking=false`，**只有这一步必须真机**。

### 5. 考核闭环

```bash
"$TB" nodejs --task "课件验收" --request-id quiz --timeout-ms 120000 <<'JS'
await page.click('#quizBtn');
await page.waitForTimeout(300);
const qs = await page.locator('#quizBody .q').count();
// 全选第一个选项后提交，验证判分与解析
for (let i = 0; i < qs; i++) await page.locator(`input[name="q${i}"]`).first().check();
await page.click('#quizSubmit');
await page.waitForTimeout(300);
const score = await page.textContent('#quizScore');
await page.screenshot({ path: "C:/path/shots/04-quiz.png" });
return { qs, score };
JS
```

### 6. 断网 / 离线

```bash
"$TB" nodejs --task "课件验收" --request-id offline --timeout-ms 120000 <<'JS'
await page.route('**/*', r => r.request().url().startsWith('http') ? r.abort() : r.continue());
await page.reload({ waitUntil: 'load' });
await page.waitForTimeout(1500);
const ok = await page.evaluate(() => {
  const c = document.querySelector('canvas');
  return !!c && c.width > 0 && !!document.querySelector('#qTitle')?.textContent;
});
await page.screenshot({ path: "C:/path/shots/05-offline.png" });
return { offlineOk: ok };
JS
```

### 7. 分辨率抽查

```bash
"$TB" nodejs --task "课件验收" --request-id sizes --timeout-ms 120000 <<'JS'
const out = {};
for (const [w,h] of [[1920,1080],[1440,900],[1280,720],[1024,768]]) {
  await page.setViewportSize({ width:w, height:h });
  await page.waitForTimeout(500);
  out[`${w}x${h}`] = await page.evaluate(() => ({
    overflowX: document.documentElement.scrollWidth > innerWidth + 1,
    panelVisible: getComputedStyle(document.querySelector('.left')).opacity !== '0'
  }));
  await page.screenshot({ path: `C:/path/shots/06-${w}x${h}.png` });
}
return out;
JS
```

### 8. 收尾

```bash
"$TB" finish --task "课件验收"
```

---

## 三、判定标准（缺一不可）

| 项 | 通过条件 |
|---|---|
| 旋转 | 拖拽后 `camera.position` 变化，画面无撕裂 |
| 缩放 | 滚轮后距离变化，且不会穿模/翻转（φ 有夹紧） |
| 点选 | **每个**结构都能选中，信息卡名称与结构一致 |
| 聚焦 | 双击后结构占画面 1/3–2/3，不贴脸、不把邻件放大成色块 |
| 左栏 | 折叠后 3D 左边界释放，无残留可点区域 |
| 右栏 | 折叠后信息卡自动贴边（`body.hide-r #pickCard{right:22px}`） |
| 影院 | 顶栏/步骤条/左右栏/底栏全隐，胶囊可退出 |
| 窄屏 | 抽屉可开可关，不是 `display:none` 后再也打不开 |
| 语音 | 真机 `speaking=true`，且 `voiceState` 能走到 `ended` |
| 考核 | 3 题能答能判分，解析展开 |
| 断网 | canvas 有像素、文案仍在 |
| 截图 | 上述每步留 1 张，存 `<项目>/shots/`，挑 2–3 张进 README |

---

## 四、把证据带回交付物

- `shots/` 归档原始截图（命名 `01-orbit.png` … `06-1920x1080.png`）
- `README.md` 放 2–3 张最能说明问题的（点选信息卡、影院模式）
- `修改记录.md` 写清「Tabbit 实测：通过 / 未通过项 + 修复动作」
- 技能主页/仓库 README 用这些截图做门面，比文字有说服力

---

## 五、常见失败与处置

| 现象 | 原因 | 处置 |
|---|---|---|
| `file://` 白屏 | 浏览器禁止本地跨域 | 起 `python -m http.server`，用 127.0.0.1 |
| 拖拽没反应 | 事件绑在 `window` 但被面板拦截 | 绑到 `canvas` 本身，`touch-action:none` |
| 滚轮缩放无效 | 监听用了默认 passive | `{ passive:false }` + `preventDefault()` |
| 点不中内层结构 | 半透明外壳先命中 | `fallback` 降级（见 interaction-contract.md） |
| 点选后卡片闪一下就没 | `pointerup` 后又被 `click` 清空 | 只用一套事件，别同时绑 `click` 和 `pointerup` |
| 影院模式后回不去 | 胶囊被 `z-index` 压住 | 胶囊 `z-index` 高于所有面板 |
| 语音无声 | 未先点击页面解锁 | 首次 `pointerdown` 置 `voiceReady=true` |
