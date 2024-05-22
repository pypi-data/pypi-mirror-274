from enum import Enum


class AssetAdministrationShellDescriptorAssetKind(str, Enum):
    INSTANCE = "Instance"
    NOTAPPLICABLE = "NotApplicable"
    TYPE = "Type"

    def __str__(self) -> str:
        return str(self.value)
