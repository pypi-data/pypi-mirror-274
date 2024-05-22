from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.reference_parent_type import ReferenceParentType

if TYPE_CHECKING:
    from ..models.key import Key


T = TypeVar("T", bound="ReferenceParent")


@_attrs_define
class ReferenceParent:
    """
    Attributes:
        type (ReferenceParentType):
        keys (List['Key']):
    """

    type: ReferenceParentType
    keys: List["Key"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        keys = []
        for keys_item_data in self.keys:
            keys_item = keys_item_data.to_dict()
            keys.append(keys_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "keys": keys,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.key import Key

        d = src_dict.copy()
        type = ReferenceParentType(d.pop("type"))

        keys = []
        _keys = d.pop("keys")
        for keys_item_data in _keys:
            keys_item = Key.from_dict(keys_item_data)

            keys.append(keys_item)

        reference_parent = cls(
            type=type,
            keys=keys,
        )

        reference_parent.additional_properties = d
        return reference_parent

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
