import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("translate_plugin", ROOT / "main.py")
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)


class Handler(BaseHTTPRequestHandler):
    records = []

    def log_message(self, *args):
        pass

    def do_POST(self):
        raw = self.rfile.read(int(self.headers["Content-Length"]))
        self.records.append((self.path, self.headers.get("Authorization"), json.loads(raw)))
        if self.path == "/redirect":
            self.send_response(302)
            self.send_header("Location", "/v1/chat/completions")
            self.end_headers()
            return
        if self.path == "/denied":
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b'{"error":"secret-token"}')
            return
        if self.path == "/invalid":
            raw = b"<html>not an API</html>"
        else:
            analysis = {"translation": "Please confirm the meeting time.\n请确认会议时间。", "terms": [
                {"term": "meeting time", "meaning": "会议时间", "context": "在这句话中指请对方确认会议安排的具体时间。",
                 "example": "Please confirm the meeting time."}]}
            raw = json.dumps({"choices": [{"message": {
                "content": json.dumps(analysis, ensure_ascii=False)},
                "finish_reason": "stop"}]}, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(raw)


class PluginTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = "http://127.0.0.1:%s" % cls.server.server_port

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        patcher = patch.object(p, "state_file", return_value=Path(self.temp.name) / "pending")
        patcher.start()
        self.addCleanup(patcher.stop)
        self.settings = {"endpoint": self.url + "/v1/chat/completions", "model": "mock-model",
                         "api_key": "test-key", "debounce_ms": "0", "timeout": "3"}

    def test_http_end_to_end(self):
        rows = p.query("en 请确认会议时间", self.settings)
        path, auth, body = Handler.records[-1]
        self.assertEqual(auth, "Bearer test-key")
        self.assertEqual(body["model"], "mock-model")
        self.assertFalse(body["stream"])
        self.assertEqual(body["messages"][1], {"role": "user", "content": "请确认会议时间"})
        self.assertIn("英语", body["messages"][0]["content"])
        self.assertEqual(rows[0]["Title"], "Please confirm the meeting time. 请确认会议时间。")
        self.assertEqual(len(rows), 2)
        self.assertIn("请确认会议时间", rows[0]["JsonRPCAction"]["parameters"][0])
        self.assertEqual(rows[1]["Title"], "meeting time — 会议时间")
        self.assertIn("在这句话中", rows[1]["SubTitle"])
        self.assertIn('"translation"', body["messages"][0]["content"])

    def test_real_entrypoint_protocol(self):
        rpc = {"method": "query", "parameters": ["zh Hello"], "settings": self.settings}
        result = subprocess.run([sys.executable, str(ROOT / "main.py"), json.dumps(rpc)],
                                capture_output=True, check=True, encoding="utf-8")
        self.assertFalse(result.stderr)
        self.assertIn("result", json.loads(result.stdout))
        self.assertEqual(json.loads(result.stdout)["result"][0]["JsonRPCAction"]["method"], "copy")

    def test_query_prefix(self):
        self.assertEqual(p.parse_query("enough time", "英语"), ("enough time", "英语"))
        self.assertEqual(p.parse_query("en\thello", "简体中文"), ("hello", "英语"))
        self.assertEqual(p.parse_query("en", "简体中文"), ("", "英语"))

    def test_manual_mode(self):
        self.settings["manual"] = True
        with patch.object(p, "translate", return_value="Hello") as call:
            self.assertIn(";;", p.query("en 你好", self.settings)[0]["Title"])
            call.assert_not_called()
            self.assertEqual(p.query("en 你好;;", self.settings)[0]["Title"], "Hello")
            self.assertEqual(call.call_args.args[0], "你好")

    def test_empty_missing_configuration(self):
        self.assertIn("输入", p.query("", {})[0]["Title"])
        with self.assertRaisesRegex(p.UserError, "URL"):
            p.query("Hello", {})

    def test_endpoint_validation(self):
        for url in ["http://example.com/v1/chat/completions", "file:///tmp/foo",
                    "https://user:password@example.com", "https://example.com/?key=secret",
                    "https://example.com:wrong/api"]:
            with self.subTest(url=url), self.assertRaises(p.UserError):
                p.build_request("Hi", "英语", dict(self.settings, endpoint=url))

    def test_custom_prompt_and_environment_key(self):
        with patch.dict(os.environ, {"LEO_TRANSLATE_API_KEY": "environment-key"}):
            req = p.build_request("hi", "简体中文", dict(self.settings, api_key="", prompt="My prompt"))
            self.assertEqual(req.get_header("Authorization"), "Bearer environment-key")
            body = json.loads(req.data)
            self.assertIn("My prompt\n", body["messages"][0]["content"])
            self.assertIn("简体中文", body["messages"][0]["content"])

    def test_error_response_redacts_service_body(self):
        with self.assertRaises(p.UserError) as cm:
            p.translate("Hi", "英语", dict(self.settings, endpoint=self.url + "/denied"))
        self.assertIn("401", str(cm.exception))
        self.assertNotIn("secret-token", str(cm.exception))

    def test_redirect_is_not_followed(self):
        before = len(Handler.records)
        with self.assertRaisesRegex(p.UserError, "302"):
            p.translate("Hi", "英语", dict(self.settings, endpoint=self.url + "/redirect"))
        self.assertEqual(len(Handler.records) - before, 1)

    def test_non_json(self):
        with self.assertRaisesRegex(p.UserError, "JSON"):
            p.translate("Hi", "英语", dict(self.settings, endpoint=self.url + "/invalid"))

    def test_response_formats(self):
        value = {"choices": [{"message": {"content": [{"type": "text", "text": "你好"}]}}]}
        self.assertEqual(p.extract_translation(value), "你好")
        for data in [{}, {"choices": []}, {"choices": [{"message": {"content": None}}]},
                     {"choices": [{"finish_reason": "length", "message": {"content": "partial"}}]}]:
            with self.subTest(data=data), self.assertRaises(p.UserError):
                p.extract_translation(data)

    def test_multiline_and_long_copy(self):
        original = "中文🙂\n'Quotes'; $(Get-Process)\n" + "a" * 6500
        rows = p.result_rows(original)
        self.assertEqual(len(rows), 1)
        for row in rows:
            self.assertEqual(row["JsonRPCAction"]["parameters"], [original])
            self.assertEqual(row["CopyText"], original)
            self.assertEqual(row["Preview"]["Description"], original)
            self.assertEqual(row["TitleToolTip"], original)
            self.assertFalse(row["AddSelectedCount"])
        self.assertNotIn("\n", rows[0]["Title"])

    def test_translation_always_first_and_terms_copy_own_explanation(self):
        text = "Uplink capacity improves assured experience."
        terms = [{"term": "uplink capacity", "meaning": "上行容量", "context": "本句指网络承载上行业务的能力。", "example": text},
                 {"term": "assured experience", "meaning": "有保障的体验", "context": "本句指容量提升带来的体验保障。", "example": text}]
        rows = p.result_rows({"translation": "上行容量改善有保障的体验。", "terms": terms})
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0]["CopyText"], "上行容量改善有保障的体验。")
        self.assertIn("本句语境", rows[1]["CopyText"])
        self.assertIn("上行容量", rows[1]["CopyText"])
        self.assertNotEqual(rows[0]["CopyText"], rows[1]["CopyText"])
        self.assertGreater(rows[0]["Score"], rows[1]["Score"])
        self.assertGreater(rows[1]["Score"], rows[2]["Score"])
        self.assertTrue(all(r["AddSelectedCount"] is False for r in rows))

    def test_structured_output_filters_hallucinations_duplicates_and_bad_entries(self):
        terms = [None, {"term": 2},
                 {"term": "unknown term", "meaning": "不存在", "context": "词组不在原文中", "example": ""},
                 {"term": "uplink capacity", "meaning": "上行容量", "context": "结合该句解释", "example": "invented example"},
                 {"term": "UPLINK CAPACITY", "meaning": "上行容量", "context": "重复项", "example": ""},
                 {"term": "capacity", "meaning": "容量", "context": "", "example": ""}]
        content = json.dumps({"translation": "上行容量提升。", "terms": terms})
        parsed = p.parse_analysis(content, "Uplink capacity improves.", self.settings)
        self.assertEqual(parsed["translation"], "上行容量提升。")
        self.assertEqual(len(parsed["terms"]), 1)
        self.assertEqual(parsed["terms"][0]["example"], "")

    def test_fenced_json_plain_text_and_bad_json(self):
        valid = '{"translation":"你好", "terms":[]}'
        self.assertEqual(p.parse_analysis('```json\n' + valid + '\n```', "hello", self.settings)["translation"], "你好")
        self.assertEqual(p.parse_analysis("你好", "hello", self.settings), {"translation": "你好", "terms": []})
        for bad in ['{"translation":', '{"terms": []}', '["wrong"]']:
            with self.subTest(bad=bad), self.assertRaises(p.UserError):
                p.parse_analysis(bad, "hello", self.settings)

    def test_glossary_limit_and_disable(self):
        terms = [{"term": "term%s" % i, "meaning": "释义", "context": "本句含义", "example": ""} for i in range(10)]
        original = " ".join(t["term"] for t in terms)
        content = json.dumps({"translation": "译文", "terms": terms})
        self.assertEqual(len(p.parse_analysis(content, original, self.settings)["terms"]), 5)
        parsed = p.parse_analysis(content, original, dict(self.settings, glossary_count="8"))
        self.assertEqual(len(p.result_rows(parsed)), 9)
        self.assertEqual(p.parse_analysis(content, original, dict(self.settings, glossary_count="0"))["terms"], [])

    def test_debounce_suppresses_superseded_request(self):
        self.settings["debounce_ms"] = "100"
        output = []
        with patch.object(p, "translate", return_value="latest") as call:
            thread = threading.Thread(target=lambda: output.append(p.query("old", self.settings)))
            thread.start()
            for _ in range(100):
                if p.state_file().exists():
                    break
                time.sleep(0.001)
            p.query("", self.settings)
            thread.join()
            self.assertEqual(output, [[]])
            call.assert_not_called()

    def test_stale_inflight_response_not_shown(self):
        def api(*args):
            p.mark_latest()
            return "stale"
        with patch.object(p, "translate", side_effect=api):
            self.assertEqual(p.query("old", self.settings), [])

    def test_clipboard_passes_text_as_data(self):
        text = '你好🙂\n"; Write-Host dangerous; $env:PATH'
        with patch.object(p.os, "name", "nt"), patch.object(p.subprocess, "run") as run:
            p.copy_text(text)
            self.assertNotIn(text, " ".join(run.call_args.args[0]))
            self.assertEqual(run.call_args.kwargs["input"], text.encode("utf-8"))
            self.assertNotIn("shell", run.call_args.kwargs)

    def test_manifest(self):
        manifest = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["Language"], "python")
        self.assertTrue((ROOT / manifest["ExecuteFileName"]).is_file())
        self.assertTrue((ROOT / manifest["IcoPath"]).is_file())


if __name__ == "__main__":
    unittest.main(verbosity=2)
