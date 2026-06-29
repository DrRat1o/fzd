import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pathlib import Path
from fzd.scorer import is_subsequence, score

# --- is_subsequence tests ---

def test_basic_subsequence():
    assert is_subsequence("cfg", "config.py") == True

def test_exact_is_subsequence():
    assert is_subsequence("config", "config") == True

def test_wrong_order_fails():
    assert is_subsequence("gfc", "config.py") == False

def test_empty_query_matches_anything():
    assert is_subsequence("", "anything.py") == True

def test_query_longer_than_text_fails():
    assert is_subsequence("toolong", "hi.py") == False

# --- score tests ---

def test_exact_match_scores_highest():
    p = Path("config")
    s = score("config", p)
    assert s >= 100.0

def test_prefix_scores_higher_than_substring():
    prefix_path = Path("config.py")      # "con" is a prefix
    substr_path = Path("myconfig.py")    # "con" is a substring, not prefix
    assert score("con", prefix_path) > score("con", substr_path)

def test_no_match_returns_negative():
    p = Path("readme.md")
    assert score("xyz", p) == -1.0

def test_subsequence_scores_lowest():
    exact   = score("cfg", Path("cfg"))
    prefix  = score("cfg", Path("cfg_loader.py"))
    subseq = score("cfg", Path("sacred_config_flag.py"))
    assert exact > prefix > subseq > 0

if __name__ == "__main__":
    tests = [
        test_basic_subsequence,
        test_exact_is_subsequence,
        test_wrong_order_fails,
        test_empty_query_matches_anything,
        test_query_longer_than_text_fails,
        test_exact_match_scores_highest,
        test_prefix_scores_higher_than_substring,
        test_no_match_returns_negative,
        test_subsequence_scores_lowest,
    ]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  FAIL  {t.__name__}")
    print(f"\n{passed}/{len(tests)} passed")