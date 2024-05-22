from enum import Enum


class SortingPathItem(str, Enum):
    ADMINISTRATION_REVISION = "administration.revision"
    ADMINISTRATION_VERSION = "administration.version"
    ID = "id"
    IDSHORT = "idShort"

    def __str__(self) -> str:
        return str(self.value)
