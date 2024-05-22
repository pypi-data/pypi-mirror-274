from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.shell_descriptor_query_query_type import ShellDescriptorQueryQueryType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ShellDescriptorQuery")


@_attrs_define
class ShellDescriptorQuery:
    """
    Attributes:
        path (str):
        value (str):
        extension_name (Union[Unset, str]): If this property is set, the query applies only to the extension of this
            name. In this case, the path must reference the value property of the extension object.
        query_type (Union[Unset, ShellDescriptorQueryQueryType]):
        combined_with (Union[Unset, ShellDescriptorQuery]):
    """

    path: str
    value: str
    extension_name: Union[Unset, str] = UNSET
    query_type: Union[Unset, ShellDescriptorQueryQueryType] = UNSET
    combined_with: Union[Unset, "ShellDescriptorQuery"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path

        value = self.value

        extension_name = self.extension_name

        query_type: Union[Unset, str] = UNSET
        if not isinstance(self.query_type, Unset):
            query_type = self.query_type.value

        combined_with: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.combined_with, Unset):
            combined_with = self.combined_with.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "value": value,
            }
        )
        if extension_name is not UNSET:
            field_dict["extensionName"] = extension_name
        if query_type is not UNSET:
            field_dict["queryType"] = query_type
        if combined_with is not UNSET:
            field_dict["combinedWith"] = combined_with

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        path = d.pop("path")

        value = d.pop("value")

        extension_name = d.pop("extensionName", UNSET)

        _query_type = d.pop("queryType", UNSET)
        query_type: Union[Unset, ShellDescriptorQueryQueryType]
        if isinstance(_query_type, Unset):
            query_type = UNSET
        else:
            query_type = ShellDescriptorQueryQueryType(_query_type)

        _combined_with = d.pop("combinedWith", UNSET)
        combined_with: Union[Unset, ShellDescriptorQuery]
        if isinstance(_combined_with, Unset):
            combined_with = UNSET
        else:
            combined_with = ShellDescriptorQuery.from_dict(_combined_with)

        shell_descriptor_query = cls(
            path=path,
            value=value,
            extension_name=extension_name,
            query_type=query_type,
            combined_with=combined_with,
        )

        shell_descriptor_query.additional_properties = d
        return shell_descriptor_query

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
