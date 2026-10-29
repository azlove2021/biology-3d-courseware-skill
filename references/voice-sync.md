# 语音讲解与动画同步（强制）

## 1. 为什么必须这样做

固定时长推进时间轴 + 独立朗读，两者必然漂移：动画跑完了旁白还在讲，或旁白早结束了画面还停着。

**唯一正确的做法**：让动画被语音节奏驱动——画面定格在当前阶段，讲完这一段，才形变到下一阶段。这样无论 TTS 引擎快慢，画面永远和正在朗读的内容一一对应。

## 2. 状态机

```
hold  : t 锁定在整数阶段 i，画面显示第 i 阶段；同时朗读第 i 段旁白。
        语音 onend → phase = 'morph'
morph : 用缓动在 ~1.7s（随语速缩放）内完成 i → i+1 的形变。
        到达后 enterStage(i+1)：设置 UI、朗读第 i+1 段、phase = 'hold'
```

禁止用 `clamp(t, stageIdx + 0.999)` 这种"等语音"写法——它会让画面停在"下一阶段 99%"，正在讲第 i 段却显示第 i+1 阶段，内容错位。

## 3. 完整代码

```js
/* ---------- 语音 ---------- */
const synth = window.speechSynthesis;
const autoVoice = $('autoVoice'), rateSel = $('rate'), speakBtn = $('speakBtn');
let voiceReady = false, zhVoice = null, speaking = false, speakTimer = 0, speakToken = 0;

/* 语速：滑块 + 播放倍速同源，保证"估算时长"和"实际朗读"一致 */
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

/* token 守卫：快速切段时，旧 utterance 的 onend 不能改新状态 */
function speak(text){
  if(!synth) return;
  const my = ++speakToken;
  synth.cancel();
  const u = new SpeechSynthesisUtterance(text);
  u.lang = 'zh-CN';
  u.rate = effectiveRate();
  u.pitch = 1;
  if(zhVoice) u.voice = zhVoice;
  u.onstart = () => { if(my !== speakToken) return; speaking = true;  speakBtn.classList.add('playing'); };
  u.onend   = u.onerror = () => { if(my !== speakToken) return; speaking = false; speakBtn.classList.remove('playing'); };
  synth.speak(u);
}

/* 首次点击页面后才允许发声（浏览器策略） */
document.addEventListener('pointerdown', () => { voiceReady = true; }, { once: true });
```

```js
/* ---------- 播放循环：hold → morph ---------- */
let phase = 'hold', morphT = 0, morphFrom = 0, morphTo = 0;
const easeIO = x => x < .5 ? 2*x*x : 1 - Math.pow(-2*x + 2, 2) / 2;

function enterStage(i){
  if(i !== stageIdx) setStageUI(i);   // 设置 UI；playing 时自动朗读本段
  phase = 'hold';
}

(function loop(now){
  const dt = Math.min(0.05, (now - last) / 1000); last = now;
  if(playing){
    const voiceMode = autoVoice.checked && voiceReady && synth;
    if(voiceMode){
      if(phase === 'hold'){
        t = stageIdx; apply(t);                 // 冻结在当前阶段
        if(!speaking){                          // 本段讲完 → 形变
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
        if(k >= 1) enterStage(morphTo);         // 进入下一阶段并朗读
      }
    } else {
      t += dt * (speed * 0.22);                 // 无语音：连续播放
      if(t >= STAGES.length - 1){ t = STAGES.length - 1; playing = false; setPlay(); }
      apply(t);
    }
  }
  /* ...渲染... */
})(performance.now());
```

```js
/* ---------- 播放按钮：重置状态机 ---------- */
playBtn.onclick = () => {
  if(t >= STAGES.length - 1){ t = 0; stageIdx = -1; apply(0); }
  playing = !playing;
  voiceReady = true;
  phase = 'hold'; morphT = 0; clearTimeout(speakTimer);
  if(playing){
    if(stageIdx < 0) stageIdx = Math.round(t);
    if(autoVoice.checked && synth) speak(STAGES[stageIdx].v);
  } else if(synth){
    synth.cancel();
  }
  setPlay();
};
```

## 4. setStageUI 里的朗读规则

```js
if(autoVoice.checked && voiceReady && synth){
  if(playing){
    speak(st.v);                       // 播放中：立即读本段
  }else{
    clearTimeout(speakTimer);          // 手动切阶段：延迟 420ms，避免拖时间轴时狂读
    speakTimer = setTimeout(() => { if(!playing) speak(st.v); }, 420);
  }
}
```

切换阶段第一行必须 `synth.cancel()`，避免上一段继续读。

## 5. 验收清单

- [ ] 点播放后，画面**停在第 1 阶段**，旁白读完才动
- [ ] 每段旁白与画面阶段严格对应（不是下一阶段）
- [ ] 快速点"下一阶段"不会叠音、不会残留旧回调
- [ ] 关闭自动朗读后，播放恢复连续推进
- [ ] 语速滑块调快，旁白与形变都变快（同源）
- [ ] 页面首次点击前不出声；点击后正常
- [ ] 没有中文语音时给出提示，不静默失败
- [ ] `?voice=0` 可关闭语音
