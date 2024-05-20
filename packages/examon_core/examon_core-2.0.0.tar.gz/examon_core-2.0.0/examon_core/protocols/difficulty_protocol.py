from typing import Protocol


class DifficultyProtocol(Protocol):
    def run(self) -> str: ...
