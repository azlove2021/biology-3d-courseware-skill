#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高中生物 3D 课件交付自检（三层）

  1) static  静态结构：文件齐备、离线依赖、主题、语音代码、文档
  2) data    数据一致性：阶段数据字段、图表同源、README 数量表逐行比对
  3) runtime 浏览器运行：可选，--browser 时调用 smoke_test.py

用法:
    python check_courseware.py <项目目录或 HTML 文件> [--profile profile.json] [--browser] [--json]

退出码:
    0 = 通过（可能有警告）
    1 = 存在阻断项（FAIL）
"""
import argparse
import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

DEFAULTS = {
    "type": "process",
    "voiceMode": "required",
    "quantityChart": "required",
    "interactionLevel": "standard",
    "offlineRequired": True,
    "params": ["t", "voice", "simple"],
    "publishMode": "local",
    "knowledgeBase": "",
}
ALLOWED = {
    "type": {"process", "anatomy", "experiment", "comparison"},
    "voiceMode": {"required", "optional", "disabled"},
    "quantityChart": {"required", "optional", "disabled"},
    "interactionLevel": {"basic", "standard", "advanced"},
    "publishMode": {"local", "ask", "auto"},
}

NODE_EXTRACT = r"""
const fs = require('fs'), vm = require('vm');
const html = fs.readFileSync(process.argv[1], 'utf8');
const m = html.match(/const\s+STAGES\s*=\s*(\[[\s\S]*?\n\];)/);
if (!m) process.exit(3);
const src = m[1].replace(/;\s*$/, '');
let arr;
try { arr = vm.runInNewContext('(' + src + ')', Object.create(null), { timeout: 1000 }); }
catch (e) { process.exit(4); }
process.stdout.write(JSON.stringify(arr));
"""


class Report:
    def __init__(self):
        self.items = []

    def add(self, level, layer, msg, hint=""):
        self.items.append({"level": level, "layer": layer,
                           "message": msg, "hint": hint})

    def ok(self, layer, msg):
        self.add("ok", layer, msg)

    def info(self, layer, msg):
        self.add("info", layer, msg)

    def warn(self, layer, msg, hint=""):
        self.add("warn", layer, msg, hint)

    def fail(self, layer, msg, hint=""):
        self.add("fail", layer, msg, hint)

    def count(self, level):
        return sum(1 for i in self.items if i["level"] == level)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def find_html(root: Path):
    if root.is_file() and root.suffix.lower() in (".html", ".htm"):
        return root
    cands = [p for p in root.glob("*.html") if p.name.lower() != "index.html"]
    if not cands:
        cands = list(root.glob("*.html"))
    return max(cands, key=lambda p: p.stat().st_size) if cands else None


def load_profile(base: Path, override: str):
    profile = dict(DEFAULTS)
    path = Path(override) if override else base / "courseware-profile.json"
    if path.exists():
        try:
            data = json.loads(read_text(path))
            if isinstance(data, dict):
                profile.update(data)
        except Exception as exc:
            print(f"[WARN] 配置文件解析失败，使用默认值: {exc}", file=sys.stderr)
    return profile, path


def validate_profile(report: Report, profile: dict):
    for key, allowed in ALLOWED.items():
        if profile.get(key) not in allowed:
            report.warn("static", f"配置项 {key}={profile.get(key)!r} 不合法，可选 {sorted(allowed)}")
    if not isinstance(profile.get("offlineRequired"), bool):
        report.warn("static", "配置项 offlineRequired 必须是布尔值")
    if not isinstance(profile.get("params"), list):
        report.warn("static", "配置项 params 必须是数组")


def as_int(value):
    try:
        if isinstance(value, bool):
            return None
        return int(value)
    except (TypeError, ValueError):
        return None


def normalize_stage(stage: dict, index: int):
    counts = stage.get("counts")
    if isinstance(counts, dict):
        c = [as_int(counts.get("chromosome")), as_int(counts.get("dna")),
             as_int(counts.get("chromatid"))]
    elif isinstance(stage.get("c"), list) and len(stage["c"]) == 3:
        c = [as_int(x) for x in stage["c"]]
    else:
        c = [None, None, None]
    return {
        "id": str(stage.get("id") or f"stage-{index + 1}"),
        "name": stage.get("name") or stage.get("n") or "",
        "group": stage.get("group") or stage.get("phase") or "",
        "summary": stage.get("summary") or stage.get("s") or "",
        "narration": stage.get("narration") or stage.get("v") or "",
        "events": stage.get("events") or stage.get("f") or [],
        "counts": c,
        "cells": as_int(stage.get("cells")),
        "scope": stage.get("scope") or "",
        "warning": stage.get("warning") or stage.get("w") or "",
        "question": stage.get("question") or stage.get("q") or "",
        "source": stage.get("source") or stage.get("tb") or "",
        "visualState": stage.get("visualState") or "",
    }


def extract_json_block(html: str):
    for m in re.finditer(r"<script\b([^>]*)>([\s\S]*?)</script>", html, re.I):
        attrs, body = m.group(1), m.group(2)
        if re.search(r'type\s*=\s*["\']application/json["\']', attrs, re.I) and \
           re.search(r'id\s*=\s*["\']courseware-data["\']', attrs, re.I):
            return body.strip()
    return None


def extract_stages_via_node(html_path: Path):
    try:
        proc = subprocess.run(["node", "-e", NODE_EXTRACT, str(html_path)],
                              capture_output=True, text=True, encoding="utf-8",
                              timeout=15)
    except FileNotFoundError:
        return None, "未安装 Node，无法解析 const STAGES"
    except Exception as exc:
        return None, f"Node 解析失败: {exc}"
    if proc.returncode != 0:
        return None, f"未能从 const STAGES 提取数据（node 退出码 {proc.returncode}）"
    try:
        return json.loads(proc.stdout), ""
    except Exception as exc:
        return None, f"Node 输出不是合法 JSON: {exc}"


def parse_readme_table(md: str):
    lines = md.splitlines()
    header_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith("|") and all(k in line for k in ("染色体", "DNA", "染色单体")):
            header_idx = i
            break
    if header_idx is None:
        return None
    header = [c.strip() for c in lines[header_idx].strip().strip("|").split("|")]

    def col(name):
        for j, h in enumerate(header):
            if name in h:
                return j
        return None

    ci, di, ti = col("染色体"), col("DNA"), col("染色单体")
    cei, sci = col("细胞数"), col("统计口径")
    if None in (ci, di, ti):
        return None

    rows = []
    for line in lines[header_idx + 2:]:
        if not line.strip().startswith("|"):
            if rows:
                break
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) <= max(ci, di, ti):
            continue

        def num(idx):
            if idx is None or idx >= len(cells):
                return None
            m = re.search(r"-?\d+", cells[idx])
            return int(m.group()) if m else None

        rows.append({
            "chromosome": num(ci), "dna": num(di), "chromatid": num(ti),
            "cells": num(cei),
            "scope": cells[sci] if sci is not None and sci < len(cells) else "",
        })
    return rows


class ExternalResourceParser(HTMLParser):
    """只收集真正的 HTML 外链标签；<script> 内容会被当作 data，不会误判 JS 字符串。"""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.urls = []
        self._in_style = False

    def handle_starttag(self, tag, attrs):
        if tag == "style":
            self._in_style = True
        d = dict(attrs)
        for key in ("src", "href"):
            v = d.get(key)
            if v and re.match(r"https?://", v, re.I):
                self.urls.append(f"<{tag} {key}={v}>")

    def handle_endtag(self, tag):
        if tag == "style":
            self._in_style = False

    def handle_data(self, data):
        if self._in_style:
            for m in re.finditer(r"url\(\s*['\"]?(https?://[^)'\"]+)", data, re.I):
                self.urls.append(f"<style url={m.group(1)}>")


def check_static(report: Report, html: str, base: Path, profile: dict, html_path: Path):
    # 文件
    if not (base / "libs" / "three.min.js").exists():
        (report.fail if profile["offlineRequired"] else report.warn)(
            "static", "缺少 libs/three.min.js（离线双击将失败）")
    else:
        report.ok("static", "libs/three.min.js 存在")

    for name, level in (("README.md", "fail"), ("修改记录.md", "warn"),
                        ("preview.png", "warn"), ("index.html", "warn")):
        if not (base / name).exists():
            getattr(report, level)("static", f"缺少 {name}")

    # 基础
    if not re.search(r"three(\.min)?\.js", html):
        report.fail("static", "HTML 未引用 three.js")
    if not re.search(r"THREE\.", html):
        report.fail("static", "HTML 未发现 THREE 场景代码，疑似不是 3D 课件")

    # 主题
    for token in ("--accent", "--accent2", "--ink", "--muted", "--line",
                  "--red", "--blue", "--purple", "--cyan", "--orange"):
        if token not in html:
            report.warn("static", f"主题变量缺失: {token}")
    if "radial-gradient" not in html:
        report.warn("static", "背景未见 radial-gradient 光斑，可能过于单调")
    if "简洁" not in html:
        report.warn("static", "未见「简洁模式」")
    if not re.search(r"@media[^{]*980", html):
        report.warn("static", "未见 ≤980px 响应式断点")

    # 专业性
    if "示意" not in html and "非真实比例" not in html:
        report.fail("static", "缺少「示意 · 非真实比例」声明")
    if "人教版" not in html:
        report.fail("static", "缺少「人教版」教材标注")
    if not re.search(r"必修|选择性必修", html):
        report.warn("static", "未见教材册次（必修/选择性必修）")

    # 语音
    mode = profile["voiceMode"]
    if mode != "disabled":
        lvl = report.fail if mode == "required" else report.warn
        if "speechSynthesis" not in html:
            lvl("static", "未使用 speechSynthesis（语音要求为 %s）" % mode)
        if "SpeechSynthesisUtterance" not in html:
            lvl("static", "未构造 SpeechSynthesisUtterance")
        if "zh-CN" not in html:
            lvl("static", "未设置 zh-CN 语音")
        if "onend" not in html:
            report.warn("static", "未见 onend 回调，语音结束可能无法驱动动画")
        if not re.search(r"voiceState|voiceToken", html):
            report.warn("static", "未见显式语音状态机（voiceState/voiceToken），确认是否仍用布尔值判断")
        if re.search(r"if\s*\(\s*!\s*speaking\s*\)", html):
            report.warn("static", "发现 if(!speaking)：布尔值无法区分 pending/ended/error，建议改用五态状态机")
        if re.search(r"stageIdx\s*\+\s*0\.999", html):
            report.fail("static", "发现旧同步写法 stageIdx+0.999：会显示下一阶段却朗读当前阶段")

    # URL 参数
    if "URLSearchParams" not in html and "t" in profile.get("params", []):
        report.fail("static", "未使用 URLSearchParams，课堂书签 ?t= 不可用")
    for param in profile.get("params", []):
        if param not in ("t", "voice", "simple", "xo", "arr", "panel"):
            continue
        handled = (f"q.get('{param}')" in html) or (f'q.get("{param}")' in html)
        if not handled:
            (report.fail if param == "t" else report.warn)(
                "static", f"配置声明支持 ?{param}=，但 HTML 未见解析")
    if "t" in profile.get("params", []):
        if not re.search(r"Math\.(min|max)[\s\S]{0,120}q\.get\(['\"]t", html) and "clamp" not in html:
            report.warn("static", "?t= 未见夹紧处理（Math.min/Math.max 或 clamp）")

    # 离线：用 HTMLParser 识别真正的标签，避免把 JS 字符串里的 CDN 兜底误判
    if profile["offlineRequired"]:
        parser = ExternalResourceParser()
        try:
            parser.feed(html)
        except Exception:
            pass
        if parser.urls:
            report.fail("static", f"离线要求下发现 {len(parser.urls)} 个外链资源",
                        "示例: " + ", ".join(parser.urls[:3]))
        else:
            report.ok("static", "未发现 HTML/CSS 外链资源（离线可用）")

    if "unpkg.com/three" not in html and "cdn" not in html.lower():
        report.warn("static", "未发现 CDN 兜底（建议 unpkg → staticfile → jsdelivr）")


def check_data(report: Report, html: str, base: Path, profile: dict, html_path: Path):
    raw = extract_json_block(html)
    stages_raw = None
    source = ""

    if raw:
        source = "JSON 数据块"
        try:
            data = json.loads(raw)
            stages_raw = data.get("stages") if isinstance(data, dict) else data
        except Exception as exc:
            report.fail("data", f"courseware-data JSON 解析失败: {exc}")
            return
    else:
        stages_raw, err = extract_stages_via_node(html_path)
        if stages_raw is None:
            report.warn("data", "未找到结构化数据块，跳过数据一致性检查", err)
            return
        source = "const STAGES（Node 提取）"

    if not isinstance(stages_raw, list) or not stages_raw:
        report.fail("data", "阶段数据不是非空数组")
        return
    report.info("data", f"数据源: {source}，{len(stages_raw)} 个阶段")

    stages = [normalize_stage(s, i) for i, s in enumerate(stages_raw)]
    if len(stages) < 2:
        report.fail("data", "阶段数少于 2，无法构成过程")

    ids = {}
    for i, s in enumerate(stages):
        tag = f"阶段 {i + 1}"
        if not s["name"]:
            report.fail("data", f"{tag} 缺少 name")
        if not s["scope"]:
            report.fail("data", f"{tag} 缺少 scope（统计口径）")
        if not s["source"]:
            report.fail("data", f"{tag} 缺少 source（教材依据）")
        if profile["voiceMode"] != "disabled" and not s["narration"]:
            report.fail("data", f"{tag} 缺少 narration（旁白）")
        if not s["events"]:
            report.warn("data", f"{tag} 缺少 events（核心事件）")
        if s["id"] in ids:
            report.fail("data", f"阶段 id 重复：{s['id']}")
        ids[s["id"]] = True

        c = s["counts"]
        if any(x is None or x < 0 for x in c):
            report.fail("data", f"{tag} counts 必须是 3 个非负整数")
        else:
            chr_, dna, chromatid = c
            if chromatid not in (0, 2 * chr_):
                report.warn("data", f"{tag} 染色单体={chromatid}，通常应为 0 或 2×染色体({2 * chr_})")
            if dna < chr_:
                report.warn("data", f"{tag} DNA={dna} 小于染色体={chr_}，请核对")
        if s["cells"] is None or s["cells"] < 1:
            report.fail("data", f"{tag} cells 必须是 ≥1 的整数")

    # 图表同源
    if profile["quantityChart"] != "disabled":
        if not re.search(r"(STAGES|DATA\.stages)[\s\S]{0,120}\.map\s*\(", html):
            report.warn("data", "图表可能未从阶段数据派生（未发现 STAGES/DATA.stages 的 .map）")
        if re.search(r"data\s*:\s*\[\s*\d+\s*,", html):
            report.warn("data", "图表里可能有字面量数字数组，确认是否与阶段数据同源")

        readme = base / "README.md"
        if readme.exists():
            rows = parse_readme_table(read_text(readme))
            if rows is None:
                report.warn("data", "README 未找到数量自检表")
            elif len(rows) != len(stages):
                report.fail("data", f"README 数量表 {len(rows)} 行，阶段数据 {len(stages)} 个，行数不一致")
            else:
                for i, (row, s) in enumerate(zip(rows, stages)):
                    got = [row["chromosome"], row["dna"], row["chromatid"]]
                    if got != s["counts"]:
                        report.fail("data", f"README 第 {i + 1} 行数字 {got} 与阶段数据 {s['counts']} 不一致")
                    if row["cells"] is not None and s["cells"] is not None and row["cells"] != s["cells"]:
                        report.fail("data", f"README 第 {i + 1} 行细胞数 {row['cells']} 与阶段数据 {s['cells']} 不一致")
                report.ok("data", "README 数量表与阶段数据逐行一致")


def check_runtime(report: Report, html_path: Path, profile: dict):
    if not profile.get("_browser"):
        report.info("runtime", "未启用浏览器冒烟测试（加 --browser）")
        return
    smoke = Path(__file__).with_name("smoke_test.py")
    if not smoke.exists():
        report.warn("runtime", "未找到 scripts/smoke_test.py")
        return
    cmd = [sys.executable, str(smoke), str(html_path)]
    if profile["offlineRequired"]:
        cmd.append("--offline")
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True,
                              encoding="utf-8", timeout=120)
    except Exception as exc:
        report.warn("runtime", f"冒烟测试执行失败: {exc}")
        return
    out = (proc.stdout or "").strip()
    if out.startswith("SKIP"):
        report.info("runtime", out)
        return
    if proc.returncode == 0:
        report.ok("runtime", "浏览器冒烟测试通过")
        report.info("runtime", out[-800:] if out else "")
    else:
        report.fail("runtime", "浏览器冒烟测试未通过", out[-800:] if out else "")


def main():
    parser = argparse.ArgumentParser(description="高中生物 3D 课件交付自检")
    parser.add_argument("path", help="项目目录或 HTML 文件")
    parser.add_argument("--profile", default="", help="courseware-profile.json 路径")
    parser.add_argument("--browser", action="store_true", help="启用浏览器冒烟测试")
    parser.add_argument("--json", action="store_true", help="输出 JSON 报告")
    args = parser.parse_args()

    root = Path(args.path).expanduser().resolve()
    if not root.exists():
        print(f"路径不存在: {root}")
        return 1

    base = root if root.is_dir() else root.parent
    html_path = find_html(root)
    html = read_text(html_path) if html_path else ""

    profile, profile_path = load_profile(base, args.profile)
    profile["_browser"] = args.browser

    report = Report()
    validate_profile(report, profile)
    if html_path:
        report.ok("static", f"主文件: {html_path.name}")
        check_static(report, html, base, profile, html_path)
        check_data(report, html, base, profile, html_path)
        check_runtime(report, html_path, profile)
    else:
        report.fail("static", "未找到课件 HTML 文件")

    errors = report.count("fail")
    warnings = report.count("warn")
    oks = report.count("ok")

    if args.json:
        print(json.dumps({
            "ok": errors == 0,
            "profile": {k: v for k, v in profile.items() if not k.startswith("_")},
            "profilePath": str(profile_path),
            "errors": [i for i in report.items if i["level"] == "fail"],
            "warnings": [i for i in report.items if i["level"] == "warn"],
            "infos": [i for i in report.items if i["level"] in ("ok", "info")],
            "summary": {"errors": errors, "warnings": warnings, "passed": oks},
        }, ensure_ascii=False, indent=2))
    else:
        layers = [("static", "静态结构"), ("data", "数据一致性"), ("runtime", "浏览器运行")]
        print("\n=== 高中生物 3D 课件自检 ===")
        for key, label in layers:
            items = [i for i in report.items if i["layer"] == key]
            if not items:
                continue
            print(f"\n-- {label} --")
            for i in items:
                prefix = {"ok": "[ OK ]", "info": "[INFO]", "warn": "[WARN]", "fail": "[FAIL]"}[i["level"]]
                print(f"{prefix} {i['message']}")
                if i["hint"]:
                    print(f"       {i['hint']}")
        print(f"\n结果: {errors} 阻断 / {warnings} 警告 / {oks} 通过")
        print("未通过：先修阻断项，再处理警告。" if errors else "通过：可进入文档与发布环节。")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
