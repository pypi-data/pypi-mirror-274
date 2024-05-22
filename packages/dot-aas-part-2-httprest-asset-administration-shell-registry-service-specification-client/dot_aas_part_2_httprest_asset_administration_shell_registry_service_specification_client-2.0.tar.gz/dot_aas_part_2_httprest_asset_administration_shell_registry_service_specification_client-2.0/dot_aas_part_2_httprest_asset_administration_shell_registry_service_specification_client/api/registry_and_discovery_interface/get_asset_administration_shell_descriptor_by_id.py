from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.asset_administration_shell_descriptor import AssetAdministrationShellDescriptor
from ...models.get_asset_administration_shell_descriptor_by_id_aas_identifier import (
    GetAssetAdministrationShellDescriptorByIdAasIdentifier,
)
from ...models.result import Result
from ...types import Response


def _get_kwargs(
    aas_identifier: "GetAssetAdministrationShellDescriptorByIdAasIdentifier",
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/shell-descriptors/{aas_identifier}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[AssetAdministrationShellDescriptor, Result]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = AssetAdministrationShellDescriptor.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = Result.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = Result.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = Result.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = Result.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[AssetAdministrationShellDescriptor, Result]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    aas_identifier: "GetAssetAdministrationShellDescriptorByIdAasIdentifier",
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[AssetAdministrationShellDescriptor, Result]]:
    """Returns a specific Asset Administration Shell Descriptor

    Args:
        aas_identifier (GetAssetAdministrationShellDescriptorByIdAasIdentifier):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AssetAdministrationShellDescriptor, Result]]
    """

    kwargs = _get_kwargs(
        aas_identifier=aas_identifier,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    aas_identifier: "GetAssetAdministrationShellDescriptorByIdAasIdentifier",
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[AssetAdministrationShellDescriptor, Result]]:
    """Returns a specific Asset Administration Shell Descriptor

    Args:
        aas_identifier (GetAssetAdministrationShellDescriptorByIdAasIdentifier):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AssetAdministrationShellDescriptor, Result]
    """

    return sync_detailed(
        aas_identifier=aas_identifier,
        client=client,
    ).parsed


async def asyncio_detailed(
    aas_identifier: "GetAssetAdministrationShellDescriptorByIdAasIdentifier",
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[AssetAdministrationShellDescriptor, Result]]:
    """Returns a specific Asset Administration Shell Descriptor

    Args:
        aas_identifier (GetAssetAdministrationShellDescriptorByIdAasIdentifier):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AssetAdministrationShellDescriptor, Result]]
    """

    kwargs = _get_kwargs(
        aas_identifier=aas_identifier,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    aas_identifier: "GetAssetAdministrationShellDescriptorByIdAasIdentifier",
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[AssetAdministrationShellDescriptor, Result]]:
    """Returns a specific Asset Administration Shell Descriptor

    Args:
        aas_identifier (GetAssetAdministrationShellDescriptorByIdAasIdentifier):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AssetAdministrationShellDescriptor, Result]
    """

    return (
        await asyncio_detailed(
            aas_identifier=aas_identifier,
            client=client,
        )
    ).parsed
