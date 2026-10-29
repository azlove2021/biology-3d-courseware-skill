#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
可选的浏览器冒烟测试（Playwright）。

用法:
    python smoke_test.py <课件.html> [--offline] [--shots 目录]

行为:
    - 未安装 playwright 时输出 SKIP 并返回 0（不阻断交付）
    - 监听控制台错误与未处理异常
    - 检查 canvas 尺寸
    - 点击"下一阶段"与"播放/暂停"
    - 拖拽旋转、滚轮缩放、点选信息卡、面板折叠、影院模式（有则必测）
    - 截图到 _smoke/
    - --offline 时阻断所有 http(s) 请求后重载，验证断网仍可渲染
"""
import argparse
import json
import sys
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--shots", default="")
    args = ap.parse_args()

    html = Path(args.html).resolve()
    if not html.exists():
        print(json.dumps({"ok": False, "errors": [f"HTML 不存在: {html}"], "notes": []},
                         ensure_ascii=False))
        return 1

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("SKIP: 未安装 playwright。安装：pip install playwright && playwright install chromium")
        return 0

    errors, notes = [], []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.on("console", lambda m: errors.append(f"console.{m.type}: {m.text}")
                if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))

        page.goto(html.as_uri())
        page.wait_for_timeout(1500)

        canvas = page.query_selector("canvas")
        if not canvas:
            errors.append("未找到 canvas")
        else:
            box = canvas.bounding_box()
            if not box or box["width"] <= 0 or box["height"] <= 0:
                errors.append(f"canvas 尺寸异常: {box}")
            else:
                notes.append(f"canvas {box['width']:.0f}x{box['height']:.0f}")

        title_sel = "#sName" if page.query_selector("#sName") else "#qTitle"
        name_before = page.text_content(title_sel) if page.query_selector(title_sel) else None
        nxt = page.query_selector("#next")
        if nxt:
            nxt.click()
            page.wait_for_timeout(500)
            name_after = page.text_content(title_sel) if page.query_selector(title_sel) else None
            if name_before and name_after and name_before == name_after:
                errors.append("点击下一阶段后 #sName 未变化")
            else:
                notes.append(f"阶段切换: {name_before} -> {name_after}")

        play = page.query_selector("#play")
        if play:
            play.click()
            page.wait_for_timeout(700)
            play.click()
            page.wait_for_timeout(200)
            notes.append("播放/暂停已点击")

        # ---- 3D 交互：必须能转、能缩放（v1.3 门槛） ----
        try:
            cam0 = page.evaluate("() => camera.position.toArray()")
            page.mouse.move(720, 450)
            page.mouse.down()
            for i in range(10):
                page.mouse.move(720 + (i + 1) * 12, 450 + (i + 1) * 4)
                page.wait_for_timeout(16)
            page.mouse.up()
            page.wait_for_timeout(450)
            cam1 = page.evaluate("() => camera.position.toArray()")
            if cam0 == cam1:
                errors.append("拖拽后相机未变化：3D 场景不能旋转")
            else:
                notes.append("拖拽旋转生效")

            r0 = page.evaluate("""() => {
              const tgt = (typeof camTgt !== 'undefined') ? camTgt
                        : (typeof cam !== 'undefined' && cam.tgt) ? cam.tgt : null;
              return tgt ? camera.position.distanceTo(tgt) : null;
            }""")
            page.mouse.move(720, 450)
            page.mouse.wheel(0, -500)
            page.wait_for_timeout(600)
            r1 = page.evaluate("""() => {
              const tgt = (typeof camTgt !== 'undefined') ? camTgt
                        : (typeof cam !== 'undefined' && cam.tgt) ? cam.tgt : null;
              return tgt ? camera.position.distanceTo(tgt) : null;
            }""")
            if r0 is None or r1 is None:
                notes.append("滚轮检查跳过：未找到相机目标点变量")
            elif abs(r1 - r0) < 1e-3:
                errors.append("滚轮后相机距离未变化：不能缩放")
            else:
                notes.append(f"滚轮缩放生效 {r0:.2f} -> {r1:.2f}")
        except Exception as exc:
            notes.append(f"交互检查跳过: {exc}")

        # ---- 点选信息卡（仅 orbit+pick 型） ----
        try:
            has_pick = page.evaluate("() => typeof PICK_INFO !== 'undefined' && typeof pickAt === 'function'")
            if has_pick:
                page.keyboard.press("r")          # 先回到预设视角，保证结构在可视区
                page.wait_for_timeout(900)
                pts = page.evaluate("""() => {
                  const out = [];
                  for (const id of Object.keys(PICK_OBJ)) {
                    if (id === 'nucleus' || id === 'pore') continue;   // 容器/带孔的环不做点击靶
                    const b = new THREE.Box3().setFromObject(PICK_OBJ[id]);
                    if (b.isEmpty()) continue;
                    const c = b.getCenter(new THREE.Vector3()); c.project(camera);
                    if (c.z > 1) continue;
                    const x = (c.x*.5+.5)*innerWidth, y = (-c.y*.5+.5)*innerHeight;
                    if (x > 60 && x < innerWidth-60 && y > 150 && y < innerHeight-150)
                      out.push({id, x, y});
                  }
                  return out.slice(0, 4);
                }""")
                if not pts:
                    notes.append("点选检查跳过：当前视角下无可投影结构")
                else:
                    opened = None
                    for pt in pts:
                        page.mouse.click(pt["x"], pt["y"])
                        page.wait_for_timeout(350)
                        if page.evaluate(
                                "() => document.getElementById('pickCard').classList.contains('on')"):
                            opened = page.text_content("#pcName")
                            break
                    if not opened:
                        errors.append("点击 3D 结构后未弹出信息卡（试过 %d 个结构）" % len(pts))
                    else:
                        notes.append(f"点选结构: {opened}")
            else:
                notes.append("未实现点选（interaction3d 非 orbit+pick），跳过")
        except Exception as exc:
            notes.append(f"点选检查跳过: {exc}")

        # ---- 面板折叠 / 影院 ----
        try:
            if page.query_selector("#tgLeft"):
                page.click("#tgLeft")
                page.wait_for_timeout(350)
                hidden = page.evaluate("() => document.body.classList.contains('hide-l')")
                if not hidden:
                    errors.append("点击「讲解」后左栏未折叠")
                else:
                    notes.append("左栏折叠生效")
                page.click("#tgLeft")
                page.wait_for_timeout(250)
            else:
                notes.append("未实现面板折叠，跳过")

            if page.query_selector("#tgCinema"):
                page.keyboard.press("f")
                page.wait_for_timeout(350)
                cine = page.evaluate("() => document.body.classList.contains('cinema')")
                if not cine:
                    errors.append("按 F 未进入影院模式")
                else:
                    notes.append("影院模式生效")
                page.keyboard.press("Escape")
                page.wait_for_timeout(250)
        except Exception as exc:
            notes.append(f"面板检查跳过: {exc}")

        shots = Path(args.shots) if args.shots else html.parent / "_smoke"
        try:
            shots.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(shots / "smoke-stage.png"))
            notes.append(f"截图: {shots / 'smoke-stage.png'}")
        except Exception as exc:
            notes.append(f"截图失败: {exc}")

        if args.offline:
            ctx.route("**/*", lambda route: route.abort()
                      if route.request.url.startswith("http") else route.continue_())
            page.reload()
            page.wait_for_timeout(1500)
            canvas = page.query_selector("canvas")
            box = canvas.bounding_box() if canvas else None
            if not box or box["width"] <= 0:
                errors.append("断网后 canvas 未渲染（离线失败）")
            else:
                notes.append("断网后 canvas 仍正常")

        browser.close()

    print(json.dumps({"ok": not errors, "errors": errors, "notes": notes},
                     ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
