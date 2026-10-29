#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
校验脚本回归测试：正确样例必须通过，故障样例必须被拦住。

运行:
    python tests/test_checker.py
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CHECKER = Path(__file__).resolve().parents[1] / "scripts" / "check_courseware.py"

VALID_JSON = """{
  "meta": {"title": "测试", "textbook": "人教版 2019", "chapter": "必修2 第2章第1节", "type": "process"},
  "stages": [
    {"id": "a", "name": "A", "short": "A", "group": "G", "summary": "s", "narration": "n",
     "events": ["e"], "counts": {"chromosome": 4, "dna": 4, "chromatid": 0},
     "cells": 1, "scope": "每个细胞", "warning": "w", "question": "q", "source": "必修2 第2章第1节"},
    {"id": "b", "name": "B", "short": "B", "group": "G", "summary": "s", "narration": "n",
     "events": ["e"], "counts": {"chromosome": 4, "dna": 8, "chromatid": 8},
     "cells": 1, "scope": "每个细胞", "warning": "w", "question": "q", "source": "必修2 第2章第1节"},
    {"id": "c", "name": "C", "short": "C", "group": "G", "summary": "s", "narration": "n",
     "events": ["e"], "counts": {"chromosome": 2, "dna": 4, "chromatid": 4},
     "cells": 2, "scope": "每个子细胞", "warning": "w", "question": "q", "source": "必修2 第2章第1节"}
  ]
}"""

VALID_METRICS_JSON = """{
  "meta": {"title": "指标型测试", "textbook": "人教版 2019", "chapter": "必修2 第4章第1节", "type": "process"},
  "stages": [
    {"id": "m1", "name": "起始", "short": "起", "group": "转录", "summary": "s", "narration": "n",
     "events": ["e"], "metrics": [
       {"key": "progress", "label": "转录进度", "value": 0, "unit": "%"},
       {"key": "mrna", "label": "mRNA 长度", "value": 0, "unit": "nt"},
       {"key": "peptide", "label": "肽链长度", "value": 0, "unit": "aa"}],
     "scope": "每个细胞", "warning": "w", "question": "q", "source": "必修2 第4章第1节"},
    {"id": "m2", "name": "延伸", "short": "伸", "group": "转录", "summary": "s", "narration": "n",
     "events": ["e"], "metrics": [
       {"key": "progress", "label": "转录进度", "value": 50, "unit": "%"},
       {"key": "mrna", "label": "mRNA 长度", "value": 60, "unit": "nt"},
       {"key": "peptide", "label": "肽链长度", "value": 0, "unit": "aa"}],
     "scope": "每个细胞", "warning": "w", "question": "q", "source": "必修2 第4章第1节"},
    {"id": "m3", "name": "翻译", "short": "译", "group": "翻译", "summary": "s", "narration": "n",
     "events": ["e"], "metrics": [
       {"key": "progress", "label": "转录进度", "value": 100, "unit": "%"},
       {"key": "mrna", "label": "mRNA 长度", "value": 90, "unit": "nt"},
       {"key": "peptide", "label": "肽链长度", "value": 30, "unit": "aa"}],
     "scope": "每个细胞", "warning": "w", "question": "q", "source": "必修2 第4章第1节"}
  ]
}"""

VALID_HTML = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
:root{
  --font:"PingFang SC","Microsoft YaHei",system-ui,sans-serif;
  --sci:#2F6BFF;--cyan:#13B8C6;--violet:#7C5CFF;--ok:#10B981;--warn:#F59E0B;--bad:#EF4444;
  --ink:#0E1A2B;--glass:rgba(255,255,255,.84);--glass-blur:blur(12px) saturate(150%);
  --shadow-2:0 10px 32px rgba(30,50,110,.14);--line:rgba(14,26,43,.08);--tint:#F3F7FF;
  --r-panel:16px;--top-h:78px;--steps-h:46px;--foot-h:52px;
  --panelw-l:clamp(320px,22vw,404px);--panelw-r:clamp(300px,20.5vw,348px);
}
.panel{background:var(--glass);backdrop-filter:var(--glass-blur);border-radius:var(--r-panel)}
</style></head><body>
<header id="top">主线问题 · 因果链 · 下一步</header>
<nav class="steps">1 2 3</nav>
<aside class="left">本步</aside>
<aside class="right">中控台</aside>
<footer class="foot">上一步 下一步 考核 · 示意 · 非真实比例</footer>
<canvas></canvas>
<script type="application/json" id="courseware-data">__JSON__</script>
<script src="libs/three.min.js"></script>
<script>
document.write('<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.min.js"><\\/script>');
const DATA=JSON.parse(document.getElementById('courseware-data').textContent);
const STAGES=DATA.stages;
const SERIES=STAGES.map(s=>s.counts?s.counts.chromosome:(s.metrics||[]).length);
const synth=window.speechSynthesis;
const u=new SpeechSynthesisUtterance('x'); u.lang='zh-CN'; u.onend=()=>{};
let voiceState='pending', voiceToken=0;
const q=new URLSearchParams(location.search);
q.get('t'); q.get('voice'); q.get('simple');
let t=Math.min(2,Math.max(0,parseFloat(q.get('t'))||0));
const scene=new THREE.Scene();
</script></body></html>"""

VALID_README = """# 测试课件

| # | 阶段 | 染色体 | DNA | 染色单体 | 细胞数 | 统计口径 | 教材依据 |
|---|---|---|---|---|---|---|---|
| 1 | A | 4 | 4 | 0 | 1 | 每个细胞 | 必修2 第2章第1节 |
| 2 | B | 4 | 8 | 8 | 1 | 每个细胞 | 必修2 第2章第1节 |
| 3 | C | 2 | 4 | 4 | 2 | 每个子细胞 | 必修2 第2章第1节 |
"""


def make_project(tmp: Path, html: str = None, readme: str = None, libs: bool = True):
    (tmp / "libs").mkdir(parents=True, exist_ok=True)
    if libs:
        (tmp / "libs" / "three.min.js").write_text("// stub", encoding="utf-8")
    (tmp / "README.md").write_text(readme or VALID_README, encoding="utf-8")
    (tmp / "修改记录.md").write_text("# 修改记录", encoding="utf-8")
    (tmp / "preview.png").write_bytes(b"")
    (tmp / "index.html").write_text("<!doctype html>", encoding="utf-8")
    (tmp / "S-01_test.html").write_text(html or VALID_HTML.replace("__JSON__", VALID_JSON),
                                        encoding="utf-8")


def run_checker(tmp: Path):
    proc = subprocess.run([sys.executable, str(CHECKER), str(tmp), "--json"],
                          capture_output=True, text=True, encoding="utf-8")
    try:
        data = json.loads(proc.stdout)
    except Exception:
        raise AssertionError(f"输出不是 JSON:\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")
    return proc.returncode, data


def has_error(data, needle):
    return any(needle in e["message"] or needle in e.get("hint", "") for e in data["errors"])


def has_warn(data, needle):
    return any(needle in w["message"] or needle in w.get("hint", "") for w in data["warnings"])


class CheckerTests(unittest.TestCase):
    def test_valid_project_passes(self):
        with tempfile.TemporaryDirectory() as d:
            make_project(Path(d))
            code, data = run_checker(Path(d))
            self.assertEqual(code, 0, data["errors"])
            self.assertEqual(data["summary"]["errors"], 0)

    def test_metrics_project_passes(self):
        with tempfile.TemporaryDirectory() as d:
            html = VALID_HTML.replace("__JSON__", VALID_METRICS_JSON)
            make_project(Path(d), html=html)
            code, data = run_checker(Path(d))
            self.assertEqual(code, 0, data["errors"])
            self.assertTrue(any("metrics" in i["message"] for i in data["infos"]))

    def test_missing_local_libs_is_blocking(self):
        with tempfile.TemporaryDirectory() as d:
            make_project(Path(d), libs=False)
            code, data = run_checker(Path(d))
            self.assertEqual(code, 1)
            self.assertTrue(has_error(data, "libs/three.min.js"))

    def test_duplicate_stage_id_is_blocking(self):
        with tempfile.TemporaryDirectory() as d:
            html = VALID_HTML.replace("__JSON__", VALID_JSON).replace('"id": "b"', '"id": "a"')
            make_project(Path(d), html=html)
            code, data = run_checker(Path(d))
            self.assertEqual(code, 1)
            self.assertTrue(has_error(data, "id 重复"))

    def test_readme_count_mismatch_is_blocking(self):
        with tempfile.TemporaryDirectory() as d:
            readme = VALID_README.replace("| 2 | B | 4 | 8 | 8 |", "| 2 | B | 4 | 4 | 8 |")
            make_project(Path(d), readme=readme)
            code, data = run_checker(Path(d))
            self.assertEqual(code, 1)
            self.assertTrue(has_error(data, "不一致"))

    def test_missing_voice_is_blocking_when_required(self):
        with tempfile.TemporaryDirectory() as d:
            html = VALID_HTML.replace("__JSON__", VALID_JSON).replace(
                "const synth=window.speechSynthesis;", "const synth=null;")
            make_project(Path(d), html=html)
            code, data = run_checker(Path(d))
            self.assertEqual(code, 1)
            self.assertTrue(has_error(data, "speechSynthesis"))

    def test_external_resource_is_blocking_when_offline(self):
        with tempfile.TemporaryDirectory() as d:
            html = VALID_HTML.replace("__JSON__", VALID_JSON).replace(
                "</head>", '<link href="https://example.com/a.css" rel="stylesheet"></head>')
            make_project(Path(d), html=html)
            code, data = run_checker(Path(d))
            self.assertEqual(code, 1)
            self.assertTrue(has_error(data, "外链"))

    def test_js_cdn_fallback_not_flagged_as_html_resource(self):
        # document.write 里的 <script src> 是 JS 字符串，不应被当作 HTML 外链
        with tempfile.TemporaryDirectory() as d:
            make_project(Path(d))
            code, data = run_checker(Path(d))
            self.assertEqual(code, 0)
            self.assertFalse(has_error(data, "外链"))

    def test_bad_counts_type_is_blocking(self):
        with tempfile.TemporaryDirectory() as d:
            html = VALID_HTML.replace("__JSON__", VALID_JSON).replace(
                '"chromatid": 8', '"chromatid": "x"')
            make_project(Path(d), html=html)
            code, data = run_checker(Path(d))
            self.assertEqual(code, 1)
            self.assertTrue(has_error(data, "counts"))

    def test_hardcoded_chart_is_warning(self):
        with tempfile.TemporaryDirectory() as d:
            html = VALID_HTML.replace("__JSON__", VALID_JSON).replace(
                "const SERIES=STAGES.map(s=>s.counts?s.counts.chromosome:(s.metrics||[]).length);",
                "const SERIES=[4,4,2];")
            make_project(Path(d), html=html)
            code, data = run_checker(Path(d))
            self.assertEqual(code, 0)
            self.assertTrue(has_warn(data, "图表"))

    def test_missing_param_handling_is_warning(self):
        with tempfile.TemporaryDirectory() as d:
            html = VALID_HTML.replace("__JSON__", VALID_JSON).replace("q.get('voice');", "")
            make_project(Path(d), html=html)
            code, data = run_checker(Path(d))
            self.assertEqual(code, 0)
            self.assertTrue(has_warn(data, "?voice"))

    def test_missing_backdrop_filter_is_blocking_for_glass(self):
        with tempfile.TemporaryDirectory() as d:
            html = VALID_HTML.replace("__JSON__", VALID_JSON).replace(
                "backdrop-filter:var(--glass-blur);", "")
            make_project(Path(d), html=html)
            code, data = run_checker(Path(d))
            self.assertEqual(code, 1)
            self.assertTrue(has_error(data, "backdrop-filter"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
