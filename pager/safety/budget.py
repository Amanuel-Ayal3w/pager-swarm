"""Step, token, and wall-clock limits for one agent turn."""

import time


class BudgetExceeded(Exception):
    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__(reason)


class Budget:
    def __init__(self, max_steps: int = 6, max_tokens: int = 8_000, max_seconds: float = 45) -> None:
        self.max_steps = max_steps
        self.max_tokens = max_tokens
        self.max_seconds = max_seconds
        self.steps = 0
        self.tokens = 0
        self.started = time.monotonic()

    def charge(self, tokens: int) -> None:
        self.steps += 1
        self.tokens += tokens
        if self.steps > self.max_steps:
            raise BudgetExceeded("step budget")
        if self.tokens > self.max_tokens:
            raise BudgetExceeded("token budget")
        if time.monotonic() - self.started > self.max_seconds:
            raise BudgetExceeded("time budget")
