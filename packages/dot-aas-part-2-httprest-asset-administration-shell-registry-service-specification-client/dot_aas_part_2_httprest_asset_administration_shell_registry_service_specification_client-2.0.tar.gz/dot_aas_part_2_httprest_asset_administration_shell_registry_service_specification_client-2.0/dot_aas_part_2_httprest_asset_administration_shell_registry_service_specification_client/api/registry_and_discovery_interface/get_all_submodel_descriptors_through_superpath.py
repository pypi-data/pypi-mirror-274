from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_all_submodel_descriptors_through_superpath_aas_identifier import (
    GetAllSubmodelDescriptorsThroughSuperpathAasIdentifier,
)
from ...models.get_submodel_descriptors_result import GetSubmodelDescriptorsResult
from ...models.result import Result
from ...types import UNSET, Response, Unset


def _get_kwargs(
    aas_identifier: "GetAllSubmodelDescriptorsThroughSuperpathAasIdentifier",
    *,
    limit: Union[Unset, int] = UNSET,
    cursor: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["limit"] = limit

    params["cursor"] = cursor

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/shell-descriptors/{aas_identifier}/submodel-descriptors",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GetSubmodelDescriptorsResult, Result]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetSubmodelDescriptorsResult.from_dict(response.json())

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
) -> Response[Union[GetSubmodelDescriptorsResult, Result]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    aas_identifier: "GetAllSubmodelDescriptorsThroughSuperpathAasIdentifier",
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = UNSET,
    cursor: Union[Unset, str] = UNSET,
) -> Response[Union[GetSubmodelDescriptorsResult, Result]]:
    """Returns all Submodel Descriptors

    Args:
        aas_identifier (GetAllSubmodelDescriptorsThroughSuperpathAasIdentifier):
        limit (Union[Unset, int]):
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetSubmodelDescriptorsResult, Result]]
    """

    kwargs = _get_kwargs(
        aas_identifier=aas_identifier,
        limit=limit,
        cursor=cursor,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    aas_identifier: "GetAllSubmodelDescriptorsThroughSuperpathAasIdentifier",
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = UNSET,
    cursor: Union[Unset, str] = UNSET,
) -> Optional[Union[GetSubmodelDescriptorsResult, Result]]:
    """Returns all Submodel Descriptors

    Args:
        aas_identifier (GetAllSubmodelDescriptorsThroughSuperpathAasIdentifier):
        limit (Union[Unset, int]):
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetSubmodelDescriptorsResult, Result]
    """

    return sync_detailed(
        aas_identifier=aas_identifier,
        client=client,
        limit=limit,
        cursor=cursor,
    ).parsed


async def asyncio_detailed(
    aas_identifier: "GetAllSubmodelDescriptorsThroughSuperpathAasIdentifier",
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = UNSET,
    cursor: Union[Unset, str] = UNSET,
) -> Response[Union[GetSubmodelDescriptorsResult, Result]]:
    """Returns all Submodel Descriptors

    Args:
        aas_identifier (GetAllSubmodelDescriptorsThroughSuperpathAasIdentifier):
        limit (Union[Unset, int]):
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetSubmodelDescriptorsResult, Result]]
    """

    kwargs = _get_kwargs(
        aas_identifier=aas_identifier,
        limit=limit,
        cursor=cursor,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    aas_identifier: "GetAllSubmodelDescriptorsThroughSuperpathAasIdentifier",
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = UNSET,
    cursor: Union[Unset, str] = UNSET,
) -> Optional[Union[GetSubmodelDescriptorsResult, Result]]:
    """Returns all Submodel Descriptors

    Args:
        aas_identifier (GetAllSubmodelDescriptorsThroughSuperpathAasIdentifier):
        limit (Union[Unset, int]):
        cursor (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetSubmodelDescriptorsResult, Result]
    """

    return (
        await asyncio_detailed(
            aas_identifier=aas_identifier,
            client=client,
            limit=limit,
            cursor=cursor,
        )
    ).parsed
