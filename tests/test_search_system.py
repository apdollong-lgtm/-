import json
import unittest
from unittest.mock import patch

import search_system


class FakeResponse:
    def __init__(self, body: str):
        self._body = body.encode("utf-8")

    def read(self):
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class SearchSystemTests(unittest.TestCase):
    def test_search_online_success(self):
        payload = json.dumps(
            [
                "แมว",
                ["แมวบ้าน"],
                ["สัตว์เลี้ยงลูกด้วยนม"],
                ["https://th.wikipedia.org/wiki/แมว"],
            ]
        )

        with patch.object(search_system, "urlopen", return_value=FakeResponse(payload)):
            results = search_system.search_online("แมว", max_results=1)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "แมวบ้าน")

    def test_search_online_rejects_empty_query(self):
        with self.assertRaises(ValueError):
            search_system.search_online("   ")

    def test_format_results_when_empty(self):
        self.assertEqual(search_system.format_results([]), "ไม่พบผลลัพธ์")


if __name__ == "__main__":
    unittest.main()
