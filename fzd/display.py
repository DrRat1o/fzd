from pathlib import Path

RESET = "\033[0m"
BOLD = "\033[1m"
YELLOW = "\033[33m"
DIM = "\033[2m"

def highlight(name: str, query: str) -> str:
    q_idx = 0
    result = ""
    for char in name:
        if q_idx < len(query) and char.lower() == query[q_idx].lower():
            result += f"{BOLD}{YELLOW}{char}{RESET}"
            q_idx += 1
        else:
            result += char
    return result

def print_results(results: list, query: str, root: Path):
    if not results: 
        print(f"{DIM}no matches for '{query}'{RESET}")
        return

    for score, path in results:
        rel = path.relative_to(root)
        parts = rel.parts
        if len(parts) > 1:
            prefix = DIM + "/".join(parts[:-1]) + "/" + RESET
        else:
            prefix = ""
        name = highlight(parts[-1], query)
        print(f" {prefix}{name}")