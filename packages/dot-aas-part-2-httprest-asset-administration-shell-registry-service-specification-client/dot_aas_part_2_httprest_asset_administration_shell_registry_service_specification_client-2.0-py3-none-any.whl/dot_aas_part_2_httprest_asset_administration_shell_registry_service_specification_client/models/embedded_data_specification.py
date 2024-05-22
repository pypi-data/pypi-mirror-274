from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.data_specification_content import DataSpecificationContent
    from ..models.reference import Reference


T = TypeVar("T", bound="EmbeddedDataSpecification")


@_attrs_define
class EmbeddedDataSpecification:
    """
    Attributes:
        data_specification (Reference):
        data_specification_content (DataSpecificationContent):
    """

    data_specification: "Reference"
    data_specification_content: "DataSpecificationContent"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data_specification = self.data_specification.to_dict()

        data_specification_content = self.data_specification_content.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "dataSpecification": data_specification,
                "dataSpecificationContent": data_specification_content,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.data_specification_content import DataSpecificationContent
        from ..models.reference import Reference

        d = src_dict.copy()
        data_specification = Reference.from_dict(d.pop("dataSpecification"))

        data_specification_content = DataSpecificationContent.from_dict(d.pop("dataSpecificationContent"))

        embedded_data_specification = cls(
            data_specification=data_specification,
            data_specification_content=data_specification_content,
        )

        embedded_data_specification.additional_properties = d
        return embedded_data_specification

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
