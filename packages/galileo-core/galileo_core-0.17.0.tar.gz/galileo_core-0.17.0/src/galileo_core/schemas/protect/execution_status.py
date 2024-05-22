from enum import Enum


class ExecutionStatus(str, Enum):
    """Status of the execution."""

    triggered = "triggered"
    failed = "failed"
    error = "error"
    timeout = "timeout"
    paused = "paused"
    not_triggered = "not_triggered"
