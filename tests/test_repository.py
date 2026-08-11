import json
import pathlib
import re
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class RepositoryQualityTests(unittest.TestCase):
    def test_examples_are_valid_json(self):
        for path in sorted((ROOT / "examples").glob("*.json")):
            with self.subTest(path=path.name):
                with path.open(encoding="utf-8") as file:
                    payload = json.load(file)
                self.assertIsInstance(payload, dict)
                self.assertTrue(payload)

    def test_task_example_has_portable_fields(self):
        with (ROOT / "examples" / "task_cmd.json").open(encoding="utf-8") as file:
            payload = json.load(file)
        self.assertEqual(payload["action"], "move")
        self.assertIn("target", payload)
        self.assertNotIn("password", payload)

    def test_no_likely_committed_secrets(self):
        risky_assignment = re.compile(
            r"(?i)(password|passwd|secret|api[_-]?key|access[_-]?token)"
            r"\s*[:=]\s*['\"](?!(?:your-|example-|change-me|<))[^'\"]{8,}['\"]"
        )
        checked_suffixes = {".cpp", ".h", ".md", ".yaml", ".yml", ".xml", ".json"}
        for path in ROOT.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in checked_suffixes:
                continue
            if path == pathlib.Path(__file__).resolve():
                continue
            with self.subTest(path=str(path.relative_to(ROOT))):
                text = path.read_text(encoding="utf-8")
                self.assertIsNone(risky_assignment.search(text))

    def test_no_large_files(self):
        oversized = [
            str(path.relative_to(ROOT))
            for path in ROOT.rglob("*")
            if path.is_file() and path.stat().st_size > 5 * 1024 * 1024
        ]
        self.assertEqual(oversized, [])


if __name__ == "__main__":
    unittest.main()
