from enum import Enum


class ReferenceType(str, Enum):
    EXTERNALREFERENCE = "ExternalReference"
    MODELREFERENCE = "ModelReference"

    def __str__(self) -> str:
        return str(self.value)
