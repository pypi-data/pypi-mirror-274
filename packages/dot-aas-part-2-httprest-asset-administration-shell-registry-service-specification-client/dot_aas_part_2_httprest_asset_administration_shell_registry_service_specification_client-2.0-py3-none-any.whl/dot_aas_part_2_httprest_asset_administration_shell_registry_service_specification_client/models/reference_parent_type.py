from enum import Enum


class ReferenceParentType(str, Enum):
    EXTERNALREFERENCE = "ExternalReference"
    MODELREFERENCE = "ModelReference"

    def __str__(self) -> str:
        return str(self.value)
