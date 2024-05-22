from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.sorting_direction import SortingDirection
from ..models.sorting_path_item import SortingPathItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="Sorting")


@_attrs_define
class Sorting:
    """
    Attributes:
        path (List[SortingPathItem]):
        direction (Union[Unset, SortingDirection]):
    """

    path: List[SortingPathItem]
    direction: Union[Unset, SortingDirection] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = []
        for path_item_data in self.path:
            path_item = path_item_data.value
            path.append(path_item)

        direction: Union[Unset, str] = UNSET
        if not isinstance(self.direction, Unset):
            direction = self.direction.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
            }
        )
        if direction is not UNSET:
            field_dict["direction"] = direction

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        path = []
        _path = d.pop("path")
        for path_item_data in _path:
            path_item = SortingPathItem(path_item_data)

            path.append(path_item)

        _direction = d.pop("direction", UNSET)
        direction: Union[Unset, SortingDirection]
        if isinstance(_direction, Unset):
            direction = UNSET
        else:
            direction = SortingDirection(_direction)

        sorting = cls(
            path=path,
            direction=direction,
        )

        sorting.additional_properties = d
        return sorting

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
