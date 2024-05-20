from enum import Enum


class AnalystAction(str, Enum):
    DOWNGRADED = "downgraded"
    INITIATED = "initiated"
    MAINTAINED = "maintained"
    REITERATED = "reiterated"
    UPGRADED = "upgraded"

    def __str__(self) -> str:
        return str(self.value)
