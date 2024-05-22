from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.asset_administration_shell_descriptor import AssetAdministrationShellDescriptor


T = TypeVar("T", bound="ShellDescriptorSearchResponse")


@_attrs_define
class ShellDescriptorSearchResponse:
    """
    Attributes:
        total (int):
        hits (List['AssetAdministrationShellDescriptor']):
    """

    total: int
    hits: List["AssetAdministrationShellDescriptor"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        total = self.total

        hits = []
        for hits_item_data in self.hits:
            hits_item = hits_item_data.to_dict()
            hits.append(hits_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total": total,
                "hits": hits,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.asset_administration_shell_descriptor import AssetAdministrationShellDescriptor

        d = src_dict.copy()
        total = d.pop("total")

        hits = []
        _hits = d.pop("hits")
        for hits_item_data in _hits:
            hits_item = AssetAdministrationShellDescriptor.from_dict(hits_item_data)

            hits.append(hits_item)

        shell_descriptor_search_response = cls(
            total=total,
            hits=hits,
        )

        shell_descriptor_search_response.additional_properties = d
        return shell_descriptor_search_response

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
