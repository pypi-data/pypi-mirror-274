from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.reference_type import ReferenceType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.key import Key
    from ..models.reference_parent import ReferenceParent


T = TypeVar("T", bound="Reference")


@_attrs_define
class Reference:
    """
    Attributes:
        type (ReferenceType):
        keys (List['Key']):
        referred_semantic_id (Union[Unset, ReferenceParent]):
    """

    type: ReferenceType
    keys: List["Key"]
    referred_semantic_id: Union[Unset, "ReferenceParent"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        keys = []
        for keys_item_data in self.keys:
            keys_item = keys_item_data.to_dict()
            keys.append(keys_item)

        referred_semantic_id: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.referred_semantic_id, Unset):
            referred_semantic_id = self.referred_semantic_id.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "keys": keys,
            }
        )
        if referred_semantic_id is not UNSET:
            field_dict["referredSemanticId"] = referred_semantic_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.key import Key
        from ..models.reference_parent import ReferenceParent

        d = src_dict.copy()
        type = ReferenceType(d.pop("type"))

        keys = []
        _keys = d.pop("keys")
        for keys_item_data in _keys:
            keys_item = Key.from_dict(keys_item_data)

            keys.append(keys_item)

        _referred_semantic_id = d.pop("referredSemanticId", UNSET)
        referred_semantic_id: Union[Unset, ReferenceParent]
        if isinstance(_referred_semantic_id, Unset):
            referred_semantic_id = UNSET
        else:
            referred_semantic_id = ReferenceParent.from_dict(_referred_semantic_id)

        reference = cls(
            type=type,
            keys=keys,
            referred_semantic_id=referred_semantic_id,
        )

        reference.additional_properties = d
        return reference

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
