from typing import List, Protocol


class MultiChoiceProtocol(Protocol):
    def build(self) -> List[str]: ...
