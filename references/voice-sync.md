# 语音讲解与动画同步（强制）

## 1. 为什么必须这样做

固定时长推进时间轴 + 独立朗读，两者必然漂移：动画跑完了旁白还在讲，或旁白早结束了画面还停着。

**唯一正确的做法**：让动画被语音节奏驱动——画面定格在当前阶段，讲完这一段，才形变到下一阶段。

## 2. 禁止的写法

```js
// ❌ 禁止：用布尔值同时表达"未开始 / 正在读 / 已结束"
if (!speaking) { /* 进入下一阶段 */ }

// ❌ 禁止：用"下一阶段 99%"假装等待
if (t > stageIdx + 0.999) t = stageIdx + 0.999;
```

`speaking` 在 `onstart` 之前是 `false`，播放刚开始时动画会误以为"已读完"而直接推进；`onerror` 时它也可能永远不变成 `true`，导致卡死。必须用显式状态。

## 3. 五态状态机

```
pending   已请求朗读，等待 onstart
speaking  正在朗读
ended     当前语音正常结束  ← 只有这个状态允许进入 morph
cancelled 用户切段 / 关闭语音 / 重置
error     朗读失败（800ms 后兜底为 ended，避免卡死）
```

每条语音分配一个 `token`。所有回调先比对 `token`，过期回调直接忽略。

```
hold ──speakStage()──> pending ──onstart──> speaking ──onend──> ended ──> morph
  │                        │                    │
  │                        └──onerror──> error ──800ms──> ended
  └──cancelVoice()──> cancelled（token++，旧回调全部失效）
```

## 4. 完整代码

```js
/* ---------- 语音状态 ---------- */
const synth = window.speechSynthesis;
const autoVoice = $('autoVoice'), rateSel = $('rate'), speakBtn = $('speakBtn');

let voiceState = 'ended';     // pending | speaking | ended | cancelled | error
let voiceToken = 0;           // 每条语音一个 token
let voiceStage = -1;          // 当前语音对应的阶段索引
let fallbackTimer = 0;
let zhVoice = null, voiceReady = false;

function effectiveRate(){
  const base = parseFloat(rateSel.value) || 1;
  return Math.min(1.4, Math.max(0.6, base * (speed / 0.85)));
}
function estVoiceDur(text){
  return Math.max(3.2, text.length / (4.8 * effectiveRate()) + 0.6);
}
function loadVoices(){
  if(!synth) return;
  const vs = synth.getVoices();
  zhVoice = vs.find(v => /zh[-_]?CN|Chinese|中文|普通话/i.test(v.lang + ' ' + v.name))
         || vs.find(v => /^zh/i.test(v.lang)) || null;
}
if(synth){ loadVoices(); synth.onvoiceschanged = loadVoices; }

/* 取消：token++ 让所有旧回调失效 */
function cancelVoice(){
  voiceToken++;
  voiceStage = -1;
  clearTimeout(fallbackTimer);
  if(synth) synth.cancel();
  voiceState = 'cancelled';
}

/* 朗读某一阶段；同步把状态置为 pending，避免动画抢跑 */
function speakStage(idx){
  if(!synth){ voiceState = 'error'; return; }
  const my = ++voiceToken;
  voiceStage = idx;
  voiceState = 'pending';
  synth.cancel();
  clearTimeout(fallbackTimer);

  const u = new SpeechSynthesisUtterance(STAGES[idx].v);
  u.lang = 'zh-CN';
  u.rate = effectiveRate();
  u.pitch = 1;
  if(zhVoice) u.voice = zhVoice;

  u.onstart = () => { if(my !== voiceToken) return; voiceState = 'speaking'; };
  u.onend   = () => { if(my !== voiceToken) return; voiceState = 'ended'; };
  u.onerror = () => {
    if(my !== voiceToken) return;
    voiceState = 'error';
    setTimeout(() => { if(my === voiceToken) voiceState = 'ended'; }, 800);
  };

  synth.speak(u);

  // 兜底：个别浏览器不触发 onstart/onend，超时视为结束
  fallbackTimer = setTimeout(() => {
    if(my !== voiceToken) return;
    if(voiceState === 'pending' || voiceState === 'speaking') voiceState = 'ended';
  }, (estVoiceDur(STAGES[idx].v) + 3) * 1000);
}
```

```js
/* ---------- 播放循环：hold → morph ---------- */
let phase = 'hold', morphT = 0, morphFrom = 0, morphTo = 0;
const easeIO = x => x < .5 ? 2*x*x : 1 - Math.pow(-2*x + 2, 2) / 2;

function enterStage(i){
  if(i !== stageIdx) setStageUI(i);   // setStageUI 内会 speakStage(i)，同步置 pending
  phase = 'hold';
}

(function loop(now){
  const dt = Math.min(0.05, (now - last) / 1000); last = now;
  if(playing){
    const voiceMode = autoVoice.checked && voiceReady && synth;
    if(voiceMode){
      if(phase === 'hold'){
        t = stageIdx; apply(t);
        // 只有"当前阶段的语音正常结束"才允许形变
        if(voiceState === 'ended' && voiceStage === stageIdx){
          if(stageIdx < STAGES.length - 1){
            phase = 'morph'; morphFrom = stageIdx; morphTo = stageIdx + 1;
            morphT = 0; cam.rGoal = FRAME[morphTo];
          } else { playing = false; setPlay(); }
        }
      } else {
        const md = Math.max(0.7, 1.7 / Math.max(0.4, effectiveRate()));
        morphT += dt / md;
        const k = Math.min(1, morphT);
        t = morphFrom + (morphTo - morphFrom) * easeIO(k);
        apply(t);
        if(k >= 1) enterStage(morphTo);
      }
    } else {
      t += dt * (speed * 0.22);
      if(t >= STAGES.length - 1){ t = STAGES.length - 1; playing = false; setPlay(); }
      apply(t);
    }
  }
  /* ...渲染... */
})(performance.now());
```

```js
/* ---------- setStageUI 内的朗读 ---------- */
if(autoVoice.checked && voiceReady && synth){
  if(playing){
    speakStage(idx);                 // 同步置 pending，动画不会抢跑
  }else{
    clearTimeout(speakTimer);        // 手动切阶段：延迟 420ms，避免拖时间轴狂读
    speakTimer = setTimeout(() => { if(!playing) speakStage(idx); }, 420);
  }
}
```

```js
/* ---------- 播放按钮 ---------- */
playBtn.onclick = () => {
  if(t >= STAGES.length - 1){ t = 0; stageIdx = -1; apply(0); }
  playing = !playing;
  voiceReady = true;
  phase = 'hold'; morphT = 0; clearTimeout(speakTimer);
  if(playing){
    if(stageIdx < 0) stageIdx = Math.round(t);
    if(autoVoice.checked && synth) speakStage(stageIdx);
  } else {
    cancelVoice();
  }
  setPlay();
};
```

切段、拖时间轴、关闭语音、重置时，统一调用 `cancelVoice()`，不要只写 `synth.cancel()`。

## 5. 边界情况

| 情况 | 处理 |
|---|---|
| 浏览器没有 `speechSynthesis` | `voiceState='error'`；循环走无语音路径，不阻塞 |
| 没有中文语音 | 仍尝试朗读；失败走 error → ended；面板提示"未找到中文语音" |
| 快速点上一/下一阶段 | 每次 `cancelVoice()` 使 token 失效，旧回调不生效 |
| 暂停后继续 | `phase='hold'` 重置；若当前阶段已读完，立即进入 morph |
| 关闭自动朗读 | `cancelVoice()`；循环切到无语音连续播放 |
| 最后一阶段结束 | `playing=false`，不越界 |
| 语音加载慢 | `pending` 期间画面保持不动，不会误推进 |
| `onerror` / 无 onend | 800ms 兜底为 `ended`；另有 `estVoiceDur+3s` 总超时 |

## 6. 验收清单

- [ ] 点播放后，画面**停在第 1 阶段**，旁白读完才动
- [ ] 每段旁白与画面阶段严格对应
- [ ] 快速点"下一阶段"不叠音、不残留旧回调
- [ ] 暂停/继续不会跳过或重复朗读
- [ ] 关闭自动朗读后，播放恢复连续推进
- [ ] 语速滑块调快，旁白与形变都变快（同源）
- [ ] 页面首次点击前不出声；点击后正常
- [ ] 没有中文语音 / `onerror` 时不会卡死
- [ ] `?voice=0` 可关闭语音
- [ ] 最后一阶段结束后正确停止
