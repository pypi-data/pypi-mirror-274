from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_submodel_descriptor_by_id_through_superpath_aas_identifier import (
    GetSubmodelDescriptorByIdThroughSuperpathAasIdentifier,
)
from ...models.get_submodel_descriptor_by_id_through_superpath_submodel_identifier import (
    GetSubmodelDescriptorByIdThroughSuperpathSubmodelIdentifier,
)
from ...models.result import Result
from ...models.submodel_descriptor import SubmodelDescriptor
from ...types import Response


def _get_kwargs(
    aas_identifier: "GetSubmodelDescriptorByIdThroughSuperpathAasIdentifier",
    submodel_identifier: "GetSubmodelDescriptorByIdThroughSuperpathSubmodelIdentifier",
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/shell-descriptors/{aas_identifier}/submodel-descriptors/{submodel_identifier}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Result, SubmodelDescriptor]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = SubmodelDescriptor.from_dict(response.json())

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
) -> Response[Union[Result, SubmodelDescriptor]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    aas_identifier: "GetSubmodelDescriptorByIdThroughSuperpathAasIdentifier",
    submodel_identifier: "GetSubmodelDescriptorByIdThroughSuperpathSubmodelIdentifier",
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Result, SubmodelDescriptor]]:
    """Returns a specific Submodel Descriptor

    Args:
        aas_identifier (GetSubmodelDescriptorByIdThroughSuperpathAasIdentifier):
        submodel_identifier (GetSubmodelDescriptorByIdThroughSuperpathSubmodelIdentifier):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Result, SubmodelDescriptor]]
    """

    kwargs = _get_kwargs(
        aas_identifier=aas_identifier,
        submodel_identifier=submodel_identifier,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    aas_identifier: "GetSubmodelDescriptorByIdThroughSuperpathAasIdentifier",
    submodel_identifier: "GetSubmodelDescriptorByIdThroughSuperpathSubmodelIdentifier",
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Result, SubmodelDescriptor]]:
    """Returns a specific Submodel Descriptor

    Args:
        aas_identifier (GetSubmodelDescriptorByIdThroughSuperpathAasIdentifier):
        submodel_identifier (GetSubmodelDescriptorByIdThroughSuperpathSubmodelIdentifier):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Result, SubmodelDescriptor]
    """

    return sync_detailed(
        aas_identifier=aas_identifier,
        submodel_identifier=submodel_identifier,
        client=client,
    ).parsed


async def asyncio_detailed(
    aas_identifier: "GetSubmodelDescriptorByIdThroughSuperpathAasIdentifier",
    submodel_identifier: "GetSubmodelDescriptorByIdThroughSuperpathSubmodelIdentifier",
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Result, SubmodelDescriptor]]:
    """Returns a specific Submodel Descriptor

    Args:
        aas_identifier (GetSubmodelDescriptorByIdThroughSuperpathAasIdentifier):
        submodel_identifier (GetSubmodelDescriptorByIdThroughSuperpathSubmodelIdentifier):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Result, SubmodelDescriptor]]
    """

    kwargs = _get_kwargs(
        aas_identifier=aas_identifier,
        submodel_identifier=submodel_identifier,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    aas_identifier: "GetSubmodelDescriptorByIdThroughSuperpathAasIdentifier",
    submodel_identifier: "GetSubmodelDescriptorByIdThroughSuperpathSubmodelIdentifier",
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Result, SubmodelDescriptor]]:
    """Returns a specific Submodel Descriptor

    Args:
        aas_identifier (GetSubmodelDescriptorByIdThroughSuperpathAasIdentifier):
        submodel_identifier (GetSubmodelDescriptorByIdThroughSuperpathSubmodelIdentifier):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Result, SubmodelDescriptor]
    """

    return (
        await asyncio_detailed(
            aas_identifier=aas_identifier,
            submodel_identifier=submodel_identifier,
            client=client,
        )
    ).parsed
