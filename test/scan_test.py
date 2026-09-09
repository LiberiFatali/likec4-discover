#!/usr/bin/env python3
"""Unit tests for scan.py pure helpers. Stdlib only: `python3 -m unittest test.scan_test -v`."""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "skills", "likec4-discover", "scripts"))

from scan import (  # noqa: E402
    call_map,
    called_names,
    ignore_match,
    is_test,
    module_of,
    resolve_relative,
    route_of,
    scan_file,
)


class TestIsTest(unittest.TestCase):
    def test_basename_patterns(self):
        self.assertTrue(is_test("srv/test_app.py"))
        self.assertTrue(is_test("srv/app_test.py"))
        self.assertTrue(is_test("srv/app_tests.py"))

    def test_path_patterns(self):
        self.assertTrue(is_test("srv/__tests__/x.py"))
        self.assertTrue(is_test("srv/tests/x.py"))
        self.assertTrue(is_test("a.spec.py"))

    def test_no_false_positives(self):
        self.assertFalse(is_test("srv/latest.py"))  # contains 'test' but is not a test
        self.assertFalse(is_test("srv/app.py"))
        self.assertFalse(is_test("srv/contest.py"))


class TestIgnoreMatch(unittest.TestCase):
    def test_dir_pattern_never_matches_file_substring(self):
        pats = ["data/", "env/", ".venv", "dist", "*.log"]
        # the dogfood bug: `data/` killed `database.py`, `env/` killed `alembic/env.py`
        self.assertFalse(ignore_match("backend/api/database.py", False, pats))
        self.assertFalse(ignore_match("backend/api/alembic/env.py", False, pats))
        self.assertTrue(ignore_match("backend/data/dump.json", False, pats))
        self.assertTrue(ignore_match("backend/data", True, pats))
        self.assertTrue(ignore_match("a/.venv/lib/x.py", False, pats))
        self.assertTrue(ignore_match("a/dist/b.js", False, pats))
        self.assertTrue(ignore_match("debug.log", False, pats))
        self.assertFalse(ignore_match("catalog.py", False, pats))

    def test_slashed_and_bare_patterns(self):
        self.assertTrue(ignore_match("build/output/x", False, ["build/output/"]))
        self.assertTrue(ignore_match("src/app/test_helper.py", False, ["test_*.py"]))
        self.assertFalse(ignore_match("src/latest.py", False, ["test_*.py"]))


class TestModuleOf(unittest.TestCase):
    def test_file_and_package(self):
        with tempfile.TemporaryDirectory() as root:
            full = os.path.join(root, "a", "b.py")
            self.assertEqual(module_of(root, full), "a.b")
            init = os.path.join(root, "pkg", "__init__.py")
            self.assertEqual(module_of(root, init), "pkg")


class TestResolveRelative(unittest.TestCase):
    def test_up_levels(self):
        self.assertEqual(resolve_relative("a.b.c", False, 1, "d"), "a.b.d")
        self.assertEqual(resolve_relative("a.b.c", False, 2, None), "a")
        self.assertEqual(resolve_relative("a", False, 5, "x"), "x")


class TestRoutesAndCalls(unittest.TestCase):
    def test_fastapi_route_detected(self):
        import ast
        tree = ast.parse("@app.post('/predict')\ndef predict(): ...\n")
        self.assertEqual(route_of(tree.body[0]), "POST /predict")
        tree2 = ast.parse("def plain(): ...\n")
        self.assertIsNone(route_of(tree2.body[0]))

    def test_called_names(self):
        import ast
        tree = ast.parse("def f():\n    foo()\n    x.bar()\n    return 1\n")
        names = called_names(tree.body[0])
        self.assertIn("foo", names)
        self.assertIn("bar", names)

    def test_nested_scopes_excluded(self):
        import ast
        tree = ast.parse("def outer():\n    helper()\n    def inner():\n        deep()\n")
        self.assertEqual(called_names(tree.body[0]), ["helper"])
        self.assertEqual(call_map(tree), {"outer": ["helper"]})


class TestScanFile(unittest.TestCase):
    SRC = (
        "import os\n"
        "from .sibling import helper\n"
        "\n"
        "class Store:\n"
        "    pass\n"
        "\n"
        "@app.get('/health')\n"
        "def health():\n"
        "    return Store()\n"
    )

    def test_parent_plus_symbols(self):
        with tempfile.TemporaryDirectory() as root:
            full = os.path.join(root, "app.py")
            with open(full, "w") as f:
                f.write(self.SRC)
            recs = scan_file(root, full)
            by_sym = {r.get("symbol"): r for r in recs}
            self.assertIn(None, by_sym)  # file parent
            parent = by_sym[None]
            self.assertEqual(parent["title"], "app")
            self.assertIn("os", parent["rawImports"])
            self.assertIn("sibling", parent["rawImports"])  # relative resolved
            self.assertEqual(by_sym["Store"]["symbolKind"], "class")
            route = by_sym["health"]
            self.assertEqual(route["symbolKind"], "route")
            self.assertEqual(route["route"], "GET /health")
            self.assertEqual(route["parent"], "app.py")
            self.assertGreater(route["line"], 1)

    def test_syntax_error_returns_none(self):
        with tempfile.TemporaryDirectory() as root:
            full = os.path.join(root, "bad.py")
            with open(full, "w") as f:
                f.write("def broken(:\n")
            self.assertIsNone(scan_file(root, full))


if __name__ == "__main__":
    unittest.main()
