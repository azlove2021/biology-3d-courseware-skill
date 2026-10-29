#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高中生物 3D 课件交付自检

用法:
    python check_courseware.py <项目目录或 HTML 文件>

退出码:
    0 = 通过（可能有警告）
    1 = 存在阻断项（ERROR）
"""
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ERRORS, WARNS, OKS = [], [], []


def err(msg):
    ERRORS.append(msg)


def warn(msg):
    WARNS.append(msg)


def ok(msg):
    OKS.append(msg)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def find_html(root: Path):
    if root.is_file() and root.suffix.lower() in (".html", ".htm"):
        return root
    cands = [p for p in root.glob("*.html") if p.name.lower() != "index.html"]
    if not cands:
        cands = list(root.glob("*.html"))
    return max(cands, key=lambda p: p.stat().st_size) if cands else None


NEGATIONS = ("不是", "而非", "不能", "不应", "不得", "别把", "不要", "区别于", "而不是")


def term_hits(text: str, term: str):
    """返回未被否定的术语出现上下文。"""
    hits = []
    for m in re.finditer(re.escape(term), text):
        left = max(0, m.start() - 12)
        right = min(len(text), m.end() + 12)
        ctx = text[left:right].replace("\n", " ")
        if any(n in ctx for n in NEGATIONS):
            continue
        hits.append(ctx)
    return hits


def main():
    if len(sys.argv) < 2:
        print("用法: python check_courseware.py <项目目录或 HTML 文件>")
        return 1

    root = Path(sys.argv[1]).expanduser().resolve()
    if not root.exists():
        print(f"路径不存在: {root}")
        return 1

    base = root if root.is_dir() else root.parent
    html_path = find_html(root)
    if not html_path:
        err("未找到课件 HTML 文件")
        html = ""
    else:
        html = read(html_path)
        ok(f"主文件: {html_path.name}")

    # ---------- 文件齐备 ----------
    if not (base / "libs" / "three.min.js").exists():
        err("缺少 libs/three.min.js（离线双击将失败）")
    else:
        ok("libs/three.min.js 存在")

    for name, level in (("README.md", "error"), ("修改记录.md", "warn"),
                        ("preview.png", "warn"), ("index.html", "warn")):
        if not (base / name).exists():
            (err if level == "error" else warn)(f"缺少 {name}")

    # ---------- 技术基线 ----------
    if html:
        if not re.search(r"three(\.min)?\.js", html):
            err("HTML 未引用 three.js")
        if not re.search(r"THREE\.|new\s+THREE\.", html):
            err("HTML 未发现 THREE 场景代码，疑似不是 3D 课件")
        if "unpkg.com/three" not in html and "cdn" not in html.lower():
            warn("未发现 CDN 兜底（建议 unpkg → staticfile → jsdelivr）")

        # ---------- 主题 ----------
        for token in ("--accent", "--accent2", "--ink", "--muted", "--line",
                      "--red", "--blue", "--purple", "--cyan", "--orange"):
            if token not in html:
                warn(f"主题变量缺失: {token}")
        if not re.search(r"radial-gradient", html):
            warn("背景未见 radial-gradient 光斑，可能过于单调")
        if "简洁" not in html:
            warn("未见「简洁模式」")
        if not re.search(r"@media[^{]*980", html):
            warn("未见 ≤980px 响应式断点")

        # ---------- 语音 ----------
        if "speechSynthesis" not in html:
            err("未使用 speechSynthesis（语音为强制项）")
        if "SpeechSynthesisUtterance" not in html:
            err("未构造 SpeechSynthesisUtterance")
        if "zh-CN" not in html:
            err("未设置 zh-CN 语音")
        if "onend" not in html:
            warn("未见 onend 回调，语音结束可能无法驱动动画")
        if "morph" not in html or "hold" not in html:
            warn("未见 hold/morph 状态机标记（确认是否用了旧同步写法）")
        if re.search(r"stageIdx\s*\+\s*0\.999", html):
            err("发现旧同步写法 stageIdx+0.999：会显示下一阶段却朗读当前阶段")

        # ---------- 专业性 ----------
        if "示意" not in html and "非真实比例" not in html:
            err("缺少「示意 · 非真实比例」声明")
        if "人教版" not in html:
            err("缺少「人教版」教材标注")
        if not re.search(r"必修|选择性必修", html):
            warn("未见教材册次（必修/选择性必修）")
        if "URLSearchParams" not in html:
            warn("未见 URL 参数（课堂书签 ?t= / ?voice= 等）")

        # ---------- 术语 ----------
        for term, hint in (
            ("精原细胞", "减数分裂起点应为「初级精母细胞」"),
            ("着丝点", "人教版 2019 用「着丝粒」"),
            ("原生质体", "质壁分离语境应为「原生质层」"),
        ):
            hits = term_hits(html, term)
            if hits:
                warn(f"术语「{term}」出现 {len(hits)} 次：{hint}｜例: {hits[0][:40]}")

    # ---------- README ----------
    readme = base / "README.md"
    if readme.exists():
        md = read(readme)
        for kw in ("染色体", "DNA", "染色单体"):
            if kw not in md:
                warn(f"README 数量自检表缺少「{kw}」")
        if "统计口径" not in md:
            warn("README 未写「统计口径」")
        if "教材" not in md:
            warn("README 未写教材依据")
        if not re.search(r"\?t=|URL\s*参数|书签", md):
            warn("README 未写 URL 参数 / 课堂书签")

    # ---------- 输出 ----------
    print("\n=== 高中生物 3D 课件自检 ===")
    for m in OKS:
        print(f"[ OK ] {m}")
    for m in WARNS:
        print(f"[WARN] {m}")
    for m in ERRORS:
        print(f"[FAIL] {m}")
    print(f"\n结果: {len(ERRORS)} 阻断 / {len(WARNS)} 警告 / {len(OKS)} 通过")
    if ERRORS:
        print("未通过：先修阻断项，再处理警告。")
        return 1
    print("通过：可进入文档与发布环节。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
