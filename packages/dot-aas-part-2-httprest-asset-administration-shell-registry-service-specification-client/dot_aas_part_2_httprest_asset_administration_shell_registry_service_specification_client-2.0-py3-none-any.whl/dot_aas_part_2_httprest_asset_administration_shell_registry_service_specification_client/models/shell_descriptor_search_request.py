from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.page import Page
    from ..models.shell_descriptor_query import ShellDescriptorQuery
    from ..models.sorting import Sorting


T = TypeVar("T", bound="ShellDescriptorSearchRequest")


@_attrs_define
class ShellDescriptorSearchRequest:
    """
    Attributes:
        page (Union[Unset, Page]):
        sort_by (Union[Unset, Sorting]):
        query (Union[Unset, ShellDescriptorQuery]):
    """

    page: Union[Unset, "Page"] = UNSET
    sort_by: Union[Unset, "Sorting"] = UNSET
    query: Union[Unset, "ShellDescriptorQuery"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        page: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.page, Unset):
            page = self.page.to_dict()

        sort_by: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.sort_by, Unset):
            sort_by = self.sort_by.to_dict()

        query: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.query, Unset):
            query = self.query.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if page is not UNSET:
            field_dict["page"] = page
        if sort_by is not UNSET:
            field_dict["sortBy"] = sort_by
        if query is not UNSET:
            field_dict["query"] = query

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.page import Page
        from ..models.shell_descriptor_query import ShellDescriptorQuery
        from ..models.sorting import Sorting

        d = src_dict.copy()
        _page = d.pop("page", UNSET)
        page: Union[Unset, Page]
        if isinstance(_page, Unset):
            page = UNSET
        else:
            page = Page.from_dict(_page)

        _sort_by = d.pop("sortBy", UNSET)
        sort_by: Union[Unset, Sorting]
        if isinstance(_sort_by, Unset):
            sort_by = UNSET
        else:
            sort_by = Sorting.from_dict(_sort_by)

        _query = d.pop("query", UNSET)
        query: Union[Unset, ShellDescriptorQuery]
        if isinstance(_query, Unset):
            query = UNSET
        else:
            query = ShellDescriptorQuery.from_dict(_query)

        shell_descriptor_search_request = cls(
            page=page,
            sort_by=sort_by,
            query=query,
        )

        shell_descriptor_search_request.additional_properties = d
        return shell_descriptor_search_request

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
