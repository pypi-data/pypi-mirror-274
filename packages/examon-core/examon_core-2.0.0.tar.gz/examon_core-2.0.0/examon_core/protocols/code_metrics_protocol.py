from typing import Dict, Protocol


class CodeMetricsProtocol(Protocol):
    def run(self) -> Dict[str, float]: ...
