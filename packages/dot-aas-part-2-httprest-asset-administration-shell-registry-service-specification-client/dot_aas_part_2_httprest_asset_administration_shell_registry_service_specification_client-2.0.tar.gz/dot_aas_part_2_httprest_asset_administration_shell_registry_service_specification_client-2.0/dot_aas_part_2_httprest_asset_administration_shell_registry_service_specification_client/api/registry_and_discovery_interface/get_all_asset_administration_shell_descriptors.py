from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_all_asset_administration_shell_descriptors_asset_kind import (
    GetAllAssetAdministrationShellDescriptorsAssetKind,
)
from ...models.get_asset_administration_shell_descriptors_result import GetAssetAdministrationShellDescriptorsResult
from ...models.result import Result
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: Union[Unset, int] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    asset_kind: Union[Unset, GetAllAssetAdministrationShellDescriptorsAssetKind] = UNSET,
    asset_type: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["limit"] = limit

    params["cursor"] = cursor

    json_asset_kind: Union[Unset, str] = UNSET
    if not isinstance(asset_kind, Unset):
        json_asset_kind = asset_kind.value

    params["assetKind"] = json_asset_kind

    params["assetType"] = asset_type

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/shell-descriptors",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GetAssetAdministrationShellDescriptorsResult, Result]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetAssetAdministrationShellDescriptorsResult.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = Result.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = Result.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = Result.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[GetAssetAdministrationShellDescriptorsResult, Result]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    asset_kind: Union[Unset, GetAllAssetAdministrationShellDescriptorsAssetKind] = UNSET,
    asset_type: Union[Unset, str] = UNSET,
) -> Response[Union[GetAssetAdministrationShellDescriptorsResult, Result]]:
    """Returns all Asset Administration Shell Descriptors

    Args:
        limit (Union[Unset, int]):
        cursor (Union[Unset, str]):
        asset_kind (Union[Unset, GetAllAssetAdministrationShellDescriptorsAssetKind]):
        asset_type (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetAssetAdministrationShellDescriptorsResult, Result]]
    """

    kwargs = _get_kwargs(
        limit=limit,
        cursor=cursor,
        asset_kind=asset_kind,
        asset_type=asset_type,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    asset_kind: Union[Unset, GetAllAssetAdministrationShellDescriptorsAssetKind] = UNSET,
    asset_type: Union[Unset, str] = UNSET,
) -> Optional[Union[GetAssetAdministrationShellDescriptorsResult, Result]]:
    """Returns all Asset Administration Shell Descriptors

    Args:
        limit (Union[Unset, int]):
        cursor (Union[Unset, str]):
        asset_kind (Union[Unset, GetAllAssetAdministrationShellDescriptorsAssetKind]):
        asset_type (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetAssetAdministrationShellDescriptorsResult, Result]
    """

    return sync_detailed(
        client=client,
        limit=limit,
        cursor=cursor,
        asset_kind=asset_kind,
        asset_type=asset_type,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    asset_kind: Union[Unset, GetAllAssetAdministrationShellDescriptorsAssetKind] = UNSET,
    asset_type: Union[Unset, str] = UNSET,
) -> Response[Union[GetAssetAdministrationShellDescriptorsResult, Result]]:
    """Returns all Asset Administration Shell Descriptors

    Args:
        limit (Union[Unset, int]):
        cursor (Union[Unset, str]):
        asset_kind (Union[Unset, GetAllAssetAdministrationShellDescriptorsAssetKind]):
        asset_type (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetAssetAdministrationShellDescriptorsResult, Result]]
    """

    kwargs = _get_kwargs(
        limit=limit,
        cursor=cursor,
        asset_kind=asset_kind,
        asset_type=asset_type,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    asset_kind: Union[Unset, GetAllAssetAdministrationShellDescriptorsAssetKind] = UNSET,
    asset_type: Union[Unset, str] = UNSET,
) -> Optional[Union[GetAssetAdministrationShellDescriptorsResult, Result]]:
    """Returns all Asset Administration Shell Descriptors

    Args:
        limit (Union[Unset, int]):
        cursor (Union[Unset, str]):
        asset_kind (Union[Unset, GetAllAssetAdministrationShellDescriptorsAssetKind]):
        asset_type (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetAssetAdministrationShellDescriptorsResult, Result]
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            cursor=cursor,
            asset_kind=asset_kind,
            asset_type=asset_type,
        )
    ).parsed
