import time
from pathlib import Path

def is_subsequence(query: str, text: str) -> bool:
    q_idx = 0;
    for char in text:
        if q_idx < len(query) and char == query[q_idx]:
            q_idx += 1
    return q_idx == len(query)

def score(query: str, path: Path, recent_boost_days: int = 0) -> float:
    name = path.name.lower()
    q = query.lower()

    if not is_subsequence(q, name):
        return -1.0
    
    result = 0.0

    if q == name:
        result += 100.0
    elif name.startswith(q):
        result += 60.0
    elif q in name:
        result += 40.0
    else:
        result += 10.0
    
    idx = name.find(q[0])
    if idx != -1:
        result += max(0, 10 - idx)
    
    result += max(0, 20- len(name))
    
    if recent_boost_days > 0:
        try:
            mtime = path.stat().st_mtime
            age_days = (time.time() - mtime) / 86400
            if age_days <= recent_boost_days:
                result += 15.0 * (1 - age_days / recent_boost_days)
        except OSError:
            pass
    
    return result