import argparse
from pathlib import Path
from .walker  import walk
from .scorer import score
from .display import print_results

def main():
    parser = argparse.ArgumentParser(
        prog="fzd",
        description="Fuzzy file finder with ranked results"
    )
    parser.add_argument("query", help="Search term")
    parser.add_argument("path", nargs="?", default=".", help="Root directory (default: .)")
    parser.add_argument("--type", choices=["file", "dir", "all"], default="all", dest="type_filter")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--hidden", action="store_true")
    parser.add_argument("--recent", type=int, default=0, metavar="DAYS")
    args = parser.parse_args()

    root = Path(args.path).expanduser().resolve()
    if not root.exists():
        print(f"fzd: path '{root}' does not exist")
        return
    
    results = []
    for path in walk(root, args.hidden, args.type_filter):
        s = score(args.query, path, args.recent)
        if s > 0:
            results.append((s, path))

    results.sort(key=lambda x: x[0], reverse=True)
    print_results(results[:args.limit], args.query, root)

if __name__ == "__main__":
    main()