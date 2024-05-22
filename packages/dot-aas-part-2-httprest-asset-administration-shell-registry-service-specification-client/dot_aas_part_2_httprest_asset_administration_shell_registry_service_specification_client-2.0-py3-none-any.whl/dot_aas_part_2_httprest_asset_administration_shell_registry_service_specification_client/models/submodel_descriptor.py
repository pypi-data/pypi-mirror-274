from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.administrative_information import AdministrativeInformation
    from ..models.endpoint import Endpoint
    from ..models.extension import Extension
    from ..models.lang_string_name_type import LangStringNameType
    from ..models.lang_string_text_type import LangStringTextType
    from ..models.reference import Reference


T = TypeVar("T", bound="SubmodelDescriptor")


@_attrs_define
class SubmodelDescriptor:
    """
    Attributes:
        id (str):
        endpoints (List['Endpoint']):
        description (Union[Unset, List['LangStringTextType']]):
        display_name (Union[Unset, List['LangStringNameType']]):
        extensions (Union[Unset, List['Extension']]):
        administration (Union[Unset, AdministrativeInformation]):
        id_short (Union[Unset, str]):
        semantic_id (Union[Unset, Reference]):
        supplemental_semantic_id (Union[Unset, List['Reference']]):
    """

    id: str
    endpoints: List["Endpoint"]
    description: Union[Unset, List["LangStringTextType"]] = UNSET
    display_name: Union[Unset, List["LangStringNameType"]] = UNSET
    extensions: Union[Unset, List["Extension"]] = UNSET
    administration: Union[Unset, "AdministrativeInformation"] = UNSET
    id_short: Union[Unset, str] = UNSET
    semantic_id: Union[Unset, "Reference"] = UNSET
    supplemental_semantic_id: Union[Unset, List["Reference"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        endpoints = []
        for endpoints_item_data in self.endpoints:
            endpoints_item = endpoints_item_data.to_dict()
            endpoints.append(endpoints_item)

        description: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.description, Unset):
            description = []
            for description_item_data in self.description:
                description_item = description_item_data.to_dict()
                description.append(description_item)

        display_name: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.display_name, Unset):
            display_name = []
            for display_name_item_data in self.display_name:
                display_name_item = display_name_item_data.to_dict()
                display_name.append(display_name_item)

        extensions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.extensions, Unset):
            extensions = []
            for extensions_item_data in self.extensions:
                extensions_item = extensions_item_data.to_dict()
                extensions.append(extensions_item)

        administration: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.administration, Unset):
            administration = self.administration.to_dict()

        id_short = self.id_short

        semantic_id: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.semantic_id, Unset):
            semantic_id = self.semantic_id.to_dict()

        supplemental_semantic_id: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.supplemental_semantic_id, Unset):
            supplemental_semantic_id = []
            for supplemental_semantic_id_item_data in self.supplemental_semantic_id:
                supplemental_semantic_id_item = supplemental_semantic_id_item_data.to_dict()
                supplemental_semantic_id.append(supplemental_semantic_id_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "endpoints": endpoints,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if extensions is not UNSET:
            field_dict["extensions"] = extensions
        if administration is not UNSET:
            field_dict["administration"] = administration
        if id_short is not UNSET:
            field_dict["idShort"] = id_short
        if semantic_id is not UNSET:
            field_dict["semanticId"] = semantic_id
        if supplemental_semantic_id is not UNSET:
            field_dict["supplementalSemanticId"] = supplemental_semantic_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.administrative_information import AdministrativeInformation
        from ..models.endpoint import Endpoint
        from ..models.extension import Extension
        from ..models.lang_string_name_type import LangStringNameType
        from ..models.lang_string_text_type import LangStringTextType
        from ..models.reference import Reference

        d = src_dict.copy()
        id = d.pop("id")

        endpoints = []
        _endpoints = d.pop("endpoints")
        for endpoints_item_data in _endpoints:
            endpoints_item = Endpoint.from_dict(endpoints_item_data)

            endpoints.append(endpoints_item)

        description = []
        _description = d.pop("description", UNSET)
        for description_item_data in _description or []:
            description_item = LangStringTextType.from_dict(description_item_data)

            description.append(description_item)

        display_name = []
        _display_name = d.pop("displayName", UNSET)
        for display_name_item_data in _display_name or []:
            display_name_item = LangStringNameType.from_dict(display_name_item_data)

            display_name.append(display_name_item)

        extensions = []
        _extensions = d.pop("extensions", UNSET)
        for extensions_item_data in _extensions or []:
            extensions_item = Extension.from_dict(extensions_item_data)

            extensions.append(extensions_item)

        _administration = d.pop("administration", UNSET)
        administration: Union[Unset, AdministrativeInformation]
        if isinstance(_administration, Unset):
            administration = UNSET
        else:
            administration = AdministrativeInformation.from_dict(_administration)

        id_short = d.pop("idShort", UNSET)

        _semantic_id = d.pop("semanticId", UNSET)
        semantic_id: Union[Unset, Reference]
        if isinstance(_semantic_id, Unset):
            semantic_id = UNSET
        else:
            semantic_id = Reference.from_dict(_semantic_id)

        supplemental_semantic_id = []
        _supplemental_semantic_id = d.pop("supplementalSemanticId", UNSET)
        for supplemental_semantic_id_item_data in _supplemental_semantic_id or []:
            supplemental_semantic_id_item = Reference.from_dict(supplemental_semantic_id_item_data)

            supplemental_semantic_id.append(supplemental_semantic_id_item)

        submodel_descriptor = cls(
            id=id,
            endpoints=endpoints,
            description=description,
            display_name=display_name,
            extensions=extensions,
            administration=administration,
            id_short=id_short,
            semantic_id=semantic_id,
            supplemental_semantic_id=supplemental_semantic_id,
        )

        submodel_descriptor.additional_properties = d
        return submodel_descriptor

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
