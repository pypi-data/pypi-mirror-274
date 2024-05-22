from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.reference import Reference


T = TypeVar("T", bound="SpecificAssetId")


@_attrs_define
class SpecificAssetId:
    """
    Attributes:
        name (str):
        value (str):
        semantic_id (Union[Unset, Reference]):
        supplemental_semantic_ids (Union[Unset, List['Reference']]):
        external_subject_id (Union[Unset, Reference]):
    """

    name: str
    value: str
    semantic_id: Union[Unset, "Reference"] = UNSET
    supplemental_semantic_ids: Union[Unset, List["Reference"]] = UNSET
    external_subject_id: Union[Unset, "Reference"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        value = self.value

        semantic_id: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.semantic_id, Unset):
            semantic_id = self.semantic_id.to_dict()

        supplemental_semantic_ids: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.supplemental_semantic_ids, Unset):
            supplemental_semantic_ids = []
            for supplemental_semantic_ids_item_data in self.supplemental_semantic_ids:
                supplemental_semantic_ids_item = supplemental_semantic_ids_item_data.to_dict()
                supplemental_semantic_ids.append(supplemental_semantic_ids_item)

        external_subject_id: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.external_subject_id, Unset):
            external_subject_id = self.external_subject_id.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "value": value,
            }
        )
        if semantic_id is not UNSET:
            field_dict["semanticId"] = semantic_id
        if supplemental_semantic_ids is not UNSET:
            field_dict["supplementalSemanticIds"] = supplemental_semantic_ids
        if external_subject_id is not UNSET:
            field_dict["externalSubjectId"] = external_subject_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.reference import Reference

        d = src_dict.copy()
        name = d.pop("name")

        value = d.pop("value")

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

        _external_subject_id = d.pop("externalSubjectId", UNSET)
        external_subject_id: Union[Unset, Reference]
        if isinstance(_external_subject_id, Unset):
            external_subject_id = UNSET
        else:
            external_subject_id = Reference.from_dict(_external_subject_id)

        specific_asset_id = cls(
            name=name,
            value=value,
            semantic_id=semantic_id,
            supplemental_semantic_ids=supplemental_semantic_ids,
            external_subject_id=external_subject_id,
        )

        specific_asset_id.additional_properties = d
        return specific_asset_id

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
