# service.py
from dataclasses import dataclass, field
from typing import List, Dict, Optional
import time

@dataclass
class Record:
    id: int
    name: str
    score: float = 0.0
    tags: List[str] = field(default_factory=list)

class InMemoryStore:
    def __init__(self):
        self._data: Dict[int, Record] = {}
        self._next_id = 1

    def add(self, name: str, score: float = 0.0) -> Record:
        record = Record(id=self._next_id, name=name, score=score)
        record.tags.append(f"created_at:{int(time.time())}")
        self._data[self._next_id] = record
        self._next_id += 1
        return record

    def all(self):
        return list(self._data.values())

    def top(self, n=3):
        return sorted(self._data.values(), key=lambda x: x.score, reverse=True)[:n]
