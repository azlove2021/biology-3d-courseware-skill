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

        name_before = page.text_content("#sName") if page.query_selector("#sName") else None
        nxt = page.query_selector("#next")
        if nxt:
            nxt.click()
            page.wait_for_timeout(500)
            name_after = page.text_content("#sName") if page.query_selector("#sName") else None
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
