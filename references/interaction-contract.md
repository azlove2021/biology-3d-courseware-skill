# 3D 交互与面板折叠契约（v1.3 起为硬门槛）

> 背景：v1.2 的样板课只做了「按步切机位」，学生**不能转、不能缩放、点结构没反应、讲解面板收不起来**——投影时没法全屏看实验，想追问「这是什么」也没入口。v1.3 把这三件事定成交付底线。

---

## 一、3D 场景必须可交互

| 动作 | 触发 | 行为 | 验收 |
|---|---|---|---|
| 旋转 | 左键拖拽 / 单指拖拽 | 绕目标点改变 θ、φ | 拖 100px，`camera.position` 必须变化 |
| 缩放 | 滚轮 / 双指捏合 / `−` `＋` 按钮 | 半径 r 在 `[minR, maxR]` 内变化 | 滚轮后 `distanceTo(target)` 必须变化 |
| 平移 | 右键拖拽 / `Shift`+拖拽 | 目标点沿相机右/上方向平移 | 目标点变化，且不越过场景边界 |
| 点选 | 单击结构 | 高亮 + 弹出信息卡 | `#pickCard` 激活，名称正确 |
| 聚焦 | 双击结构 / 右栏「结构速查」 | 目标点移到该结构、半径收紧 | 结构占画面 1/3–2/3 |
| 复位 | `R` / `⟲` 按钮 | 回到本步预设机位 | 1.2s 内平滑回位 |

### 1. 相机状态机（必须区分「自动取景」与「用户接管」）

```js
const view = { auto:true, spin:false };
const vDes = { theta:0, phi:1.15, r:12, tx:0, ty:0, tz:0 };  // 期望值
const vCur = { ...vDes };                                     // 当前值（阻尼跟随）
const LIM = { minR:2.2, maxR:28, minPhi:.20, maxPhi:Math.PI-.20 };

function syncView(){                    // 把当前相机反解成球坐标，接管时不跳帧
  const off = camera.position.clone().sub(camTgt);
  const len = off.length() || 1;
  vCur.r = vDes.r = Math.max(LIM.minR, Math.min(LIM.maxR, len));
  vCur.theta = vDes.theta = Math.atan2(off.x, off.z);
  vCur.phi = vDes.phi = Math.acos(Math.max(-1, Math.min(1, off.y / len)));
  vCur.tx = vDes.tx = camTgt.x; vCur.ty = vDes.ty = camTgt.y; vCur.tz = vDes.tz = camTgt.z;
}
function resumeAuto(){                  // 交还自动：从用户当前视角平滑飞回预设
  camPos.copy(camera.position);
  camTgt.set(vCur.tx, vCur.ty, vCur.tz);
  view.auto = true;
}
function updateViewCamera(dt){
  const k = 1 - Math.pow(.0015, dt);    // 帧率无关阻尼
  ['theta','phi','r','tx','ty','tz'].forEach(k2 => vCur[k2] += (vDes[k2] - vCur[k2]) * k);
  const sp = Math.sin(vCur.phi);
  camera.position.set(
    vCur.tx + vCur.r * sp * Math.sin(vCur.theta),
    vCur.ty + vCur.r * Math.cos(vCur.phi),
    vCur.tz + vCur.r * sp * Math.cos(vCur.theta)
  );
  camera.lookAt(vCur.tx, vCur.ty, vCur.tz);
}
```

**规则**：
- 每步 `goStep()` 里调用 `resumeAuto()` → **切步一定回预设**；
- 用户一旦 `pointerdown` / `wheel` → `view.auto = false`，**本步内不再抢镜**；
- `apply()` 里只有在 `view.auto` 时才写 `camera.position`，否则交给 `updateViewCamera()`；
- 主循环：`apply(t, now); if(!view.auto) updateViewCamera(dt);`

### 2. 拾取（Raycaster）

```js
const raycaster = new THREE.Raycaster();
raycaster.params.Line.threshold = .06;      // 线状对象（mRNA 示意线）要调小，否则误命中
raycaster.params.Points.threshold = .05;

function regPick(obj, id){                   // 把整棵子树打上 id
  obj.traverse(o => { o.userData.pickId = id; });
  obj.userData.pickId = id;
  PICK_ROOTS.push(obj);
}

function pickAt(x, y, select){
  const r = glCanvas.getBoundingClientRect();
  ndc.set(((x-r.left)/r.width)*2-1, -((y-r.top)/r.height)*2+1);
  raycaster.setFromCamera(ndc, camera);
  const hits = raycaster.intersectObjects(PICK_ROOTS, true);
  let fallback = null;
  for(const h of hits){
    let o = h.object, id = null;
    while(o){ if(o.userData.pickId){ id = o.userData.pickId; break; } o = o.parent; }
    if(!id || !chainVisible(h.object)) continue;
    if(id === 'nucleus'){ if(!fallback) fallback = id; continue; }  // 半透明容器不能挡内层
    if(select) selectPick(id);
    return id;
  }
  if(fallback){ if(select) selectPick(fallback); return fallback; }
  if(select) clearPick();
  return null;
}
```

**三个必踩的坑**：
1. **透明容器挡一切**：核膜/细胞膜是大球，点 DNA 永远先命中它 → 用 `fallback` 降级，优先返回内层结构。
2. **`visible === false` 仍会被 raycast 命中**（r128 不检查可见性）→ 自己写 `chainVisible()` 逐级检查。
3. **拖拽误判为点击**：`pointerdown` 记录坐标，`pointerup` 时位移 < 6px 且 < 600ms 才算点击。

### 3. 选中反馈（必须三件套）

1. **高亮**：遍历材质设 `emissive`（记原值，取消时恢复）；
2. **选中框**：`EdgesGeometry(BoxGeometry)` + `LineSegments`，每帧按 bbox 更新；
3. **信息卡**：名称 + 类别 chip + 2–3 句教材口径说明 + 一条考点/易错提示。

```js
selBox.position.copy(bbox.getCenter(new THREE.Vector3()));
const s = bbox.getSize(new THREE.Vector3());
selBox.scale.set(Math.max(.14,s.x)*1.14, Math.max(.14,s.y)*1.14, Math.max(.14,s.z)*1.14);
```

### 4. 聚焦距离（别贴脸）

```js
vDes.r = Math.max(4.5, Math.min(LIM.maxR, Math.max(vCur.r * .62, s * 1.7)));
```
> 直接用 `s * 1.05` 会贴到结构表面：相邻结构被放大成巨大色块，还会透过玻璃面板染色。取「当前距离的 62%」+「包围盒的 1.7 倍」的较大值。

---

## 二、讲解面板必须可隐藏（三档）

| 档位 | 快捷键 | 行为 | 适用 |
|---|---|---|---|
| 左栏 | `H` | 讲解卡片滑出，3D 左边界释放 | 想多看一眼中间 |
| 右栏 | `J` | 中控台滑出，读数让位 | 讲解优先 |
| 影院 | `F` | 顶栏/步骤条/左右栏/底栏/方程式卡全隐，只留顶部胶囊 + 底部视角条 | 投影、全屏看实验 |
| 浏览器全屏 | `Shift+F` | `requestFullscreen()` | 接投影仪 |

```css
.left,.right{transition:transform .24s ease,opacity .2s ease}
body.hide-l .left{transform:translateX(calc(-100% - 14px));opacity:0;pointer-events:none}
body.hide-r .right{transform:translateX(calc(100% + 14px));opacity:0;pointer-events:none}
body.cinema #top,body.cinema .steps,body.cinema .left,body.cinema .right,
body.cinema .foot,body.cinema .eqb{display:none!important}
```

**窄屏不能直接 `display:none`**（v1.2 的错）：改成抽屉，按钮仍可唤出。

```css
@media(max-width:1100px){
  .left{transform:translateX(calc(-100% - 14px))}
  .right{transform:translateX(calc(100% + 14px))}
  body.show-l .left,body.show-r .right{transform:none}
}
```
```js
function togglePanel(side){
  const b = document.body;
  if(matchMedia('(max-width:1100px)').matches){
    b.classList.toggle('show-' + side);
    b.classList.remove('show-' + (side === 'l' ? 'r' : 'l'));   // 抽屉互斥
  } else {
    b.classList.toggle('hide-' + side);
  }
  syncPanelBtns();
}
```

**恢复入口**：顶栏三个 toggle 按钮常驻（影院模式除外），影院胶囊里必须有「退出影院」；`Esc` 优先退出影院，其次关弹窗。

---

## 三、右栏「结构速查」（推荐）

点选若只能靠"盲点"，学生找不到入口。在右栏底部放 8 格结构列表：既是图例（色块），也是点选/聚焦入口，还顺手填满了中控台下方的空白。

```js
STRUCT_LIST.forEach(([id, color]) => {
  const b = document.createElement('button');
  b.className = 'st'; b.dataset.pick = id;
  b.innerHTML = `<i style="background:${color}"></i>${PICK_INFO[id].name}`;
  b.onclick = () => { selectPick(id); focusPick(id); };
});
```

---

## 四、验收（脚本 + 真实浏览器）

`smoke_test.py` 会自动断言：拖拽后相机变化、滚轮后距离变化、点选后 `#pickCard` 激活、`#tgLeft` 折叠生效、`F` 进影院。但这只证明"代码路径通"，**视觉与手感必须用 Tabbit 真机跑一遍**，见 `references/browser-testing.md`。
