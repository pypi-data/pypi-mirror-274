from enum import Enum


class ProtocolInformationSecurityAttributesType(str, Enum):
    NONE = "NONE"
    RFC_TLSA = "RFC_TLSA"
    W3C_DID = "W3C_DID"

    def __str__(self) -> str:
        return str(self.value)
