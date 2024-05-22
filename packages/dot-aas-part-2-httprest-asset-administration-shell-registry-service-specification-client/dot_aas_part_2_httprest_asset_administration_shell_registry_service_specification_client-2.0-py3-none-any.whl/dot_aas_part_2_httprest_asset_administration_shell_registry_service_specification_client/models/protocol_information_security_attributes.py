from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.protocol_information_security_attributes_type import ProtocolInformationSecurityAttributesType

T = TypeVar("T", bound="ProtocolInformationSecurityAttributes")


@_attrs_define
class ProtocolInformationSecurityAttributes:
    """
    Attributes:
        type (ProtocolInformationSecurityAttributesType):
        key (str):
        value (str):
    """

    type: ProtocolInformationSecurityAttributesType
    key: str
    value: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        key = self.key

        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "key": key,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = ProtocolInformationSecurityAttributesType(d.pop("type"))

        key = d.pop("key")

        value = d.pop("value")

        protocol_information_security_attributes = cls(
            type=type,
            key=key,
            value=value,
        )

        protocol_information_security_attributes.additional_properties = d
        return protocol_information_security_attributes

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
