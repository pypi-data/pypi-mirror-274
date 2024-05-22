from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PutSubmodelDescriptorByIdThroughSuperpathSubmodelIdentifier")


@_attrs_define
class PutSubmodelDescriptorByIdThroughSuperpathSubmodelIdentifier:
    """
    Attributes:
        short (Union[Unset, int]):
        char (Union[Unset, str]):
        int_ (Union[Unset, int]):
        long (Union[Unset, int]):
        float_ (Union[Unset, float]):
        double (Union[Unset, float]):
        direct (Union[Unset, bool]):
        read_only (Union[Unset, bool]):
    """

    short: Union[Unset, int] = UNSET
    char: Union[Unset, str] = UNSET
    int_: Union[Unset, int] = UNSET
    long: Union[Unset, int] = UNSET
    float_: Union[Unset, float] = UNSET
    double: Union[Unset, float] = UNSET
    direct: Union[Unset, bool] = UNSET
    read_only: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        short = self.short

        char = self.char

        int_ = self.int_

        long = self.long

        float_ = self.float_

        double = self.double

        direct = self.direct

        read_only = self.read_only

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if short is not UNSET:
            field_dict["short"] = short
        if char is not UNSET:
            field_dict["char"] = char
        if int_ is not UNSET:
            field_dict["int"] = int_
        if long is not UNSET:
            field_dict["long"] = long
        if float_ is not UNSET:
            field_dict["float"] = float_
        if double is not UNSET:
            field_dict["double"] = double
        if direct is not UNSET:
            field_dict["direct"] = direct
        if read_only is not UNSET:
            field_dict["readOnly"] = read_only

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        short = d.pop("short", UNSET)

        char = d.pop("char", UNSET)

        int_ = d.pop("int", UNSET)

        long = d.pop("long", UNSET)

        float_ = d.pop("float", UNSET)

        double = d.pop("double", UNSET)

        direct = d.pop("direct", UNSET)

        read_only = d.pop("readOnly", UNSET)

        put_submodel_descriptor_by_id_through_superpath_submodel_identifier = cls(
            short=short,
            char=char,
            int_=int_,
            long=long,
            float_=float_,
            double=double,
            direct=direct,
            read_only=read_only,
        )

        put_submodel_descriptor_by_id_through_superpath_submodel_identifier.additional_properties = d
        return put_submodel_descriptor_by_id_through_superpath_submodel_identifier

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
