from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.put_submodel_descriptor_by_id_through_superpath_aas_identifier import (
    PutSubmodelDescriptorByIdThroughSuperpathAasIdentifier,
)
from ...models.put_submodel_descriptor_by_id_through_superpath_submodel_identifier import (
    PutSubmodelDescriptorByIdThroughSuperpathSubmodelIdentifier,
)
from ...models.result import Result
from ...models.submodel_descriptor import SubmodelDescriptor
from ...types import Response


def _get_kwargs(
    aas_identifier: "PutSubmodelDescriptorByIdThroughSuperpathAasIdentifier",
    submodel_identifier: "PutSubmodelDescriptorByIdThroughSuperpathSubmodelIdentifier",
    *,
    body: SubmodelDescriptor,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "put",
        "url": f"/shell-descriptors/{aas_identifier}/submodel-descriptors/{submodel_identifier}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Result]]:
    if response.status_code == HTTPStatus.NO_CONTENT:
        response_204 = cast(Any, None)
        return response_204
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
) -> Response[Union[Any, Result]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    aas_identifier: "PutSubmodelDescriptorByIdThroughSuperpathAasIdentifier",
    submodel_identifier: "PutSubmodelDescriptorByIdThroughSuperpathSubmodelIdentifier",
    *,
    client: Union[AuthenticatedClient, Client],
    body: SubmodelDescriptor,
) -> Response[Union[Any, Result]]:
    """Updates an existing Submodel Descriptor

    Args:
        aas_identifier (PutSubmodelDescriptorByIdThroughSuperpathAasIdentifier):
        submodel_identifier (PutSubmodelDescriptorByIdThroughSuperpathSubmodelIdentifier):
        body (SubmodelDescriptor):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Result]]
    """

    kwargs = _get_kwargs(
        aas_identifier=aas_identifier,
        submodel_identifier=submodel_identifier,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    aas_identifier: "PutSubmodelDescriptorByIdThroughSuperpathAasIdentifier",
    submodel_identifier: "PutSubmodelDescriptorByIdThroughSuperpathSubmodelIdentifier",
    *,
    client: Union[AuthenticatedClient, Client],
    body: SubmodelDescriptor,
) -> Optional[Union[Any, Result]]:
    """Updates an existing Submodel Descriptor

    Args:
        aas_identifier (PutSubmodelDescriptorByIdThroughSuperpathAasIdentifier):
        submodel_identifier (PutSubmodelDescriptorByIdThroughSuperpathSubmodelIdentifier):
        body (SubmodelDescriptor):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Result]
    """

    return sync_detailed(
        aas_identifier=aas_identifier,
        submodel_identifier=submodel_identifier,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    aas_identifier: "PutSubmodelDescriptorByIdThroughSuperpathAasIdentifier",
    submodel_identifier: "PutSubmodelDescriptorByIdThroughSuperpathSubmodelIdentifier",
    *,
    client: Union[AuthenticatedClient, Client],
    body: SubmodelDescriptor,
) -> Response[Union[Any, Result]]:
    """Updates an existing Submodel Descriptor

    Args:
        aas_identifier (PutSubmodelDescriptorByIdThroughSuperpathAasIdentifier):
        submodel_identifier (PutSubmodelDescriptorByIdThroughSuperpathSubmodelIdentifier):
        body (SubmodelDescriptor):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Result]]
    """

    kwargs = _get_kwargs(
        aas_identifier=aas_identifier,
        submodel_identifier=submodel_identifier,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    aas_identifier: "PutSubmodelDescriptorByIdThroughSuperpathAasIdentifier",
    submodel_identifier: "PutSubmodelDescriptorByIdThroughSuperpathSubmodelIdentifier",
    *,
    client: Union[AuthenticatedClient, Client],
    body: SubmodelDescriptor,
) -> Optional[Union[Any, Result]]:
    """Updates an existing Submodel Descriptor

    Args:
        aas_identifier (PutSubmodelDescriptorByIdThroughSuperpathAasIdentifier):
        submodel_identifier (PutSubmodelDescriptorByIdThroughSuperpathSubmodelIdentifier):
        body (SubmodelDescriptor):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Result]
    """

    return (
        await asyncio_detailed(
            aas_identifier=aas_identifier,
            submodel_identifier=submodel_identifier,
            client=client,
            body=body,
        )
    ).parsed
