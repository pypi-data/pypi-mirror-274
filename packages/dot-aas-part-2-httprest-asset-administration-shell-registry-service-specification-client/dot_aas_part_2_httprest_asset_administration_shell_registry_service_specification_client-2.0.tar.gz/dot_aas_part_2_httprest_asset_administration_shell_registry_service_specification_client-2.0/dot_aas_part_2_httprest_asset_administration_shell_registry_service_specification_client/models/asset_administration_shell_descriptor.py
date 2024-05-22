from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.asset_administration_shell_descriptor_asset_kind import AssetAdministrationShellDescriptorAssetKind
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.administrative_information import AdministrativeInformation
    from ..models.endpoint import Endpoint
    from ..models.extension import Extension
    from ..models.lang_string_name_type import LangStringNameType
    from ..models.lang_string_text_type import LangStringTextType
    from ..models.specific_asset_id import SpecificAssetId
    from ..models.submodel_descriptor import SubmodelDescriptor


T = TypeVar("T", bound="AssetAdministrationShellDescriptor")


@_attrs_define
class AssetAdministrationShellDescriptor:
    """
    Attributes:
        id (str):
        description (Union[Unset, List['LangStringTextType']]):
        display_name (Union[Unset, List['LangStringNameType']]):
        extensions (Union[Unset, List['Extension']]):
        administration (Union[Unset, AdministrativeInformation]):
        asset_kind (Union[Unset, AssetAdministrationShellDescriptorAssetKind]):
        asset_type (Union[Unset, str]):
        endpoints (Union[Unset, List['Endpoint']]):
        global_asset_id (Union[Unset, str]):
        id_short (Union[Unset, str]):
        specific_asset_ids (Union[Unset, List['SpecificAssetId']]):
        submodel_descriptors (Union[Unset, List['SubmodelDescriptor']]):
    """

    id: str
    description: Union[Unset, List["LangStringTextType"]] = UNSET
    display_name: Union[Unset, List["LangStringNameType"]] = UNSET
    extensions: Union[Unset, List["Extension"]] = UNSET
    administration: Union[Unset, "AdministrativeInformation"] = UNSET
    asset_kind: Union[Unset, AssetAdministrationShellDescriptorAssetKind] = UNSET
    asset_type: Union[Unset, str] = UNSET
    endpoints: Union[Unset, List["Endpoint"]] = UNSET
    global_asset_id: Union[Unset, str] = UNSET
    id_short: Union[Unset, str] = UNSET
    specific_asset_ids: Union[Unset, List["SpecificAssetId"]] = UNSET
    submodel_descriptors: Union[Unset, List["SubmodelDescriptor"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

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

        asset_kind: Union[Unset, str] = UNSET
        if not isinstance(self.asset_kind, Unset):
            asset_kind = self.asset_kind.value

        asset_type = self.asset_type

        endpoints: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.endpoints, Unset):
            endpoints = []
            for endpoints_item_data in self.endpoints:
                endpoints_item = endpoints_item_data.to_dict()
                endpoints.append(endpoints_item)

        global_asset_id = self.global_asset_id

        id_short = self.id_short

        specific_asset_ids: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.specific_asset_ids, Unset):
            specific_asset_ids = []
            for specific_asset_ids_item_data in self.specific_asset_ids:
                specific_asset_ids_item = specific_asset_ids_item_data.to_dict()
                specific_asset_ids.append(specific_asset_ids_item)

        submodel_descriptors: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.submodel_descriptors, Unset):
            submodel_descriptors = []
            for submodel_descriptors_item_data in self.submodel_descriptors:
                submodel_descriptors_item = submodel_descriptors_item_data.to_dict()
                submodel_descriptors.append(submodel_descriptors_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
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
        if asset_kind is not UNSET:
            field_dict["assetKind"] = asset_kind
        if asset_type is not UNSET:
            field_dict["assetType"] = asset_type
        if endpoints is not UNSET:
            field_dict["endpoints"] = endpoints
        if global_asset_id is not UNSET:
            field_dict["globalAssetId"] = global_asset_id
        if id_short is not UNSET:
            field_dict["idShort"] = id_short
        if specific_asset_ids is not UNSET:
            field_dict["specificAssetIds"] = specific_asset_ids
        if submodel_descriptors is not UNSET:
            field_dict["submodelDescriptors"] = submodel_descriptors

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.administrative_information import AdministrativeInformation
        from ..models.endpoint import Endpoint
        from ..models.extension import Extension
        from ..models.lang_string_name_type import LangStringNameType
        from ..models.lang_string_text_type import LangStringTextType
        from ..models.specific_asset_id import SpecificAssetId
        from ..models.submodel_descriptor import SubmodelDescriptor

        d = src_dict.copy()
        id = d.pop("id")

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

        _asset_kind = d.pop("assetKind", UNSET)
        asset_kind: Union[Unset, AssetAdministrationShellDescriptorAssetKind]
        if isinstance(_asset_kind, Unset):
            asset_kind = UNSET
        else:
            asset_kind = AssetAdministrationShellDescriptorAssetKind(_asset_kind)

        asset_type = d.pop("assetType", UNSET)

        endpoints = []
        _endpoints = d.pop("endpoints", UNSET)
        for endpoints_item_data in _endpoints or []:
            endpoints_item = Endpoint.from_dict(endpoints_item_data)

            endpoints.append(endpoints_item)

        global_asset_id = d.pop("globalAssetId", UNSET)

        id_short = d.pop("idShort", UNSET)

        specific_asset_ids = []
        _specific_asset_ids = d.pop("specificAssetIds", UNSET)
        for specific_asset_ids_item_data in _specific_asset_ids or []:
            specific_asset_ids_item = SpecificAssetId.from_dict(specific_asset_ids_item_data)

            specific_asset_ids.append(specific_asset_ids_item)

        submodel_descriptors = []
        _submodel_descriptors = d.pop("submodelDescriptors", UNSET)
        for submodel_descriptors_item_data in _submodel_descriptors or []:
            submodel_descriptors_item = SubmodelDescriptor.from_dict(submodel_descriptors_item_data)

            submodel_descriptors.append(submodel_descriptors_item)

        asset_administration_shell_descriptor = cls(
            id=id,
            description=description,
            display_name=display_name,
            extensions=extensions,
            administration=administration,
            asset_kind=asset_kind,
            asset_type=asset_type,
            endpoints=endpoints,
            global_asset_id=global_asset_id,
            id_short=id_short,
            specific_asset_ids=specific_asset_ids,
            submodel_descriptors=submodel_descriptors,
        )

        asset_administration_shell_descriptor.additional_properties = d
        return asset_administration_shell_descriptor

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
