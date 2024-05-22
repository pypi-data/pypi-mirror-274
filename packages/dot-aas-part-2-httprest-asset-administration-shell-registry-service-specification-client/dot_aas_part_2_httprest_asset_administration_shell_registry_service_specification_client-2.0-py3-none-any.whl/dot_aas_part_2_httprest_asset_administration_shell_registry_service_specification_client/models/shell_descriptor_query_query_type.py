from enum import Enum


class ShellDescriptorQueryQueryType(str, Enum):
    MATCH = "match"
    REGEX = "regex"

    def __str__(self) -> str:
        return str(self.value)
