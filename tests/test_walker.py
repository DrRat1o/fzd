import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import tempfile
from pathlib import Path
from fzd.walker import walk


def make_tree(tmp):
    """Create a small fake directory tree for testing."""
    (tmp / "file1.py").touch()
    (tmp / "file2.txt").touch()
    (tmp / ".hidden").touch()
    sub = tmp / "subdir"
    sub.mkdir()
    (sub / "nested.py").touch()


def test_finds_files():
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        make_tree(tmp)
        results = list(walk(tmp))
        names = [p.name for p in results]
        assert "file1.py" in names
        assert "nested.py" in names


def test_excludes_hidden_by_default():
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        make_tree(tmp)
        results = list(walk(tmp))
        names = [p.name for p in results]
        assert ".hidden" not in names


def test_includes_hidden_when_asked():
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        make_tree(tmp)
        results = list(walk(tmp, include_hidden=True))
        names = [p.name for p in results]
        assert ".hidden" in names


def test_type_filter_file():
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        make_tree(tmp)
        results = list(walk(tmp, type_filter="file"))
        assert all(p.is_file() for p in results)


def test_type_filter_dir():
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        make_tree(tmp)
        results = list(walk(tmp, type_filter="dir"))
        assert all(p.is_dir() for p in results)


if __name__ == "__main__":
    tests = [
        test_finds_files,
        test_excludes_hidden_by_default,
        test_includes_hidden_when_asked,
        test_type_filter_file,
        test_type_filter_dir,
    ]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
            passed += 1
        except AssertionError:
            print(f"  FAIL  {t.__name__}")
    print(f"\n{passed}/{len(tests)} passed")