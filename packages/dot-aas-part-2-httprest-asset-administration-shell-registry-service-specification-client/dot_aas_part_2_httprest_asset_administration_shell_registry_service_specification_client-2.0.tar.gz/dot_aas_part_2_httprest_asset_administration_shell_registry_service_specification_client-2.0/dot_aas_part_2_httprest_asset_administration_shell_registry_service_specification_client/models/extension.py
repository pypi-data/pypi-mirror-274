from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.extension_value_type import ExtensionValueType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.reference import Reference


T = TypeVar("T", bound="Extension")


@_attrs_define
class Extension:
    """
    Attributes:
        name (str):
        semantic_id (Union[Unset, Reference]):
        supplemental_semantic_ids (Union[Unset, List['Reference']]):
        value_type (Union[Unset, ExtensionValueType]):
        value (Union[Unset, str]):
        refers_to (Union[Unset, List['Reference']]):
    """

    name: str
    semantic_id: Union[Unset, "Reference"] = UNSET
    supplemental_semantic_ids: Union[Unset, List["Reference"]] = UNSET
    value_type: Union[Unset, ExtensionValueType] = UNSET
    value: Union[Unset, str] = UNSET
    refers_to: Union[Unset, List["Reference"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        semantic_id: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.semantic_id, Unset):
            semantic_id = self.semantic_id.to_dict()

        supplemental_semantic_ids: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.supplemental_semantic_ids, Unset):
            supplemental_semantic_ids = []
            for supplemental_semantic_ids_item_data in self.supplemental_semantic_ids:
                supplemental_semantic_ids_item = supplemental_semantic_ids_item_data.to_dict()
                supplemental_semantic_ids.append(supplemental_semantic_ids_item)

        value_type: Union[Unset, str] = UNSET
        if not isinstance(self.value_type, Unset):
            value_type = self.value_type.value

        value = self.value

        refers_to: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.refers_to, Unset):
            refers_to = []
            for refers_to_item_data in self.refers_to:
                refers_to_item = refers_to_item_data.to_dict()
                refers_to.append(refers_to_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if semantic_id is not UNSET:
            field_dict["semanticId"] = semantic_id
        if supplemental_semantic_ids is not UNSET:
            field_dict["supplementalSemanticIds"] = supplemental_semantic_ids
        if value_type is not UNSET:
            field_dict["valueType"] = value_type
        if value is not UNSET:
            field_dict["value"] = value
        if refers_to is not UNSET:
            field_dict["refersTo"] = refers_to

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.reference import Reference

        d = src_dict.copy()
        name = d.pop("name")

        _semantic_id = d.pop("semanticId", UNSET)
        semantic_id: Union[Unset, Reference]
        if isinstance(_semantic_id, Unset):
            semantic_id = UNSET
        else:
            semantic_id = Reference.from_dict(_semantic_id)

        supplemental_semantic_ids = []
        _supplemental_semantic_ids = d.pop("supplementalSemanticIds", UNSET)
        for supplemental_semantic_ids_item_data in _supplemental_semantic_ids or []:
            supplemental_semantic_ids_item = Reference.from_dict(supplemental_semantic_ids_item_data)

            supplemental_semantic_ids.append(supplemental_semantic_ids_item)

        _value_type = d.pop("valueType", UNSET)
        value_type: Union[Unset, ExtensionValueType]
        if isinstance(_value_type, Unset):
            value_type = UNSET
        else:
            value_type = ExtensionValueType(_value_type)

        value = d.pop("value", UNSET)

        refers_to = []
        _refers_to = d.pop("refersTo", UNSET)
        for refers_to_item_data in _refers_to or []:
            refers_to_item = Reference.from_dict(refers_to_item_data)

            refers_to.append(refers_to_item)

        extension = cls(
            name=name,
            semantic_id=semantic_id,
            supplemental_semantic_ids=supplemental_semantic_ids,
            value_type=value_type,
            value=value,
            refers_to=refers_to,
        )

        extension.additional_properties = d
        return extension

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
