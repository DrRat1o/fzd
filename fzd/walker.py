from pathlib import Path
from typing import Iterator

def walk(root: Path, include_hidden: bool = False, type_filter: str = "all") -> Iterator[Path]:
    try:
        for entry in root.iterdir():
            if not include_hidden and entry.name.startswith("."):
                continue
            if entry.name == "__pycache__":
                continue
            if entry.is_dir():
                if type_filter in ("dir", "all"):
                    yield entry 
                yield from walk(entry, include_hidden, type_filter)
            elif entry.is_file():
                if type_filter in ("file", "all"):
                    yield entry
    except PermissionError:
        pass