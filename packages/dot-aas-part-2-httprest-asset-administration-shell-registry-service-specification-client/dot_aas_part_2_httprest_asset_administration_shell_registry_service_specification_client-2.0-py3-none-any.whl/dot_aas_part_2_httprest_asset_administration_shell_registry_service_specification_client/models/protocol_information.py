from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.protocol_information_security_attributes import ProtocolInformationSecurityAttributes


T = TypeVar("T", bound="ProtocolInformation")


@_attrs_define
class ProtocolInformation:
    """
    Attributes:
        href (str):
        endpoint_protocol (Union[Unset, str]):
        endpoint_protocol_version (Union[Unset, List[str]]):
        subprotocol (Union[Unset, str]):
        subprotocol_body (Union[Unset, str]):
        subprotocol_body_encoding (Union[Unset, str]):
        security_attributes (Union[Unset, List['ProtocolInformationSecurityAttributes']]):
    """

    href: str
    endpoint_protocol: Union[Unset, str] = UNSET
    endpoint_protocol_version: Union[Unset, List[str]] = UNSET
    subprotocol: Union[Unset, str] = UNSET
    subprotocol_body: Union[Unset, str] = UNSET
    subprotocol_body_encoding: Union[Unset, str] = UNSET
    security_attributes: Union[Unset, List["ProtocolInformationSecurityAttributes"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        href = self.href

        endpoint_protocol = self.endpoint_protocol

        endpoint_protocol_version: Union[Unset, List[str]] = UNSET
        if not isinstance(self.endpoint_protocol_version, Unset):
            endpoint_protocol_version = self.endpoint_protocol_version

        subprotocol = self.subprotocol

        subprotocol_body = self.subprotocol_body

        subprotocol_body_encoding = self.subprotocol_body_encoding

        security_attributes: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.security_attributes, Unset):
            security_attributes = []
            for security_attributes_item_data in self.security_attributes:
                security_attributes_item = security_attributes_item_data.to_dict()
                security_attributes.append(security_attributes_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "href": href,
            }
        )
        if endpoint_protocol is not UNSET:
            field_dict["endpointProtocol"] = endpoint_protocol
        if endpoint_protocol_version is not UNSET:
            field_dict["endpointProtocolVersion"] = endpoint_protocol_version
        if subprotocol is not UNSET:
            field_dict["subprotocol"] = subprotocol
        if subprotocol_body is not UNSET:
            field_dict["subprotocolBody"] = subprotocol_body
        if subprotocol_body_encoding is not UNSET:
            field_dict["subprotocolBodyEncoding"] = subprotocol_body_encoding
        if security_attributes is not UNSET:
            field_dict["securityAttributes"] = security_attributes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.protocol_information_security_attributes import ProtocolInformationSecurityAttributes

        d = src_dict.copy()
        href = d.pop("href")

        endpoint_protocol = d.pop("endpointProtocol", UNSET)

        endpoint_protocol_version = cast(List[str], d.pop("endpointProtocolVersion", UNSET))

        subprotocol = d.pop("subprotocol", UNSET)

        subprotocol_body = d.pop("subprotocolBody", UNSET)

        subprotocol_body_encoding = d.pop("subprotocolBodyEncoding", UNSET)

        security_attributes = []
        _security_attributes = d.pop("securityAttributes", UNSET)
        for security_attributes_item_data in _security_attributes or []:
            security_attributes_item = ProtocolInformationSecurityAttributes.from_dict(security_attributes_item_data)

            security_attributes.append(security_attributes_item)

        protocol_information = cls(
            href=href,
            endpoint_protocol=endpoint_protocol,
            endpoint_protocol_version=endpoint_protocol_version,
            subprotocol=subprotocol,
            subprotocol_body=subprotocol_body,
            subprotocol_body_encoding=subprotocol_body_encoding,
            security_attributes=security_attributes,
        )

        protocol_information.additional_properties = d
        return protocol_information

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
