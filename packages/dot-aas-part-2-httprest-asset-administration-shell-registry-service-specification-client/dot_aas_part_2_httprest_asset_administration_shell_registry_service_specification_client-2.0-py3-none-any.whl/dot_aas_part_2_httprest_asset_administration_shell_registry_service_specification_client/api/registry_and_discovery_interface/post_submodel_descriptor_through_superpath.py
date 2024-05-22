from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_submodel_descriptor_through_superpath_aas_identifier import (
    PostSubmodelDescriptorThroughSuperpathAasIdentifier,
)
from ...models.result import Result
from ...models.submodel_descriptor import SubmodelDescriptor
from ...types import Response


def _get_kwargs(
    aas_identifier: "PostSubmodelDescriptorThroughSuperpathAasIdentifier",
    *,
    body: SubmodelDescriptor,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/shell-descriptors/{aas_identifier}/submodel-descriptors",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Result, SubmodelDescriptor]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = SubmodelDescriptor.from_dict(response.json())

        return response_201
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = Result.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = Result.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = Result.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.CONFLICT:
        response_409 = Result.from_dict(response.json())

        return response_409
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
    aas_identifier: "PostSubmodelDescriptorThroughSuperpathAasIdentifier",
    *,
    client: Union[AuthenticatedClient, Client],
    body: SubmodelDescriptor,
) -> Response[Union[Result, SubmodelDescriptor]]:
    """Creates a new Submodel Descriptor, i.e. registers a submodel

    Args:
        aas_identifier (PostSubmodelDescriptorThroughSuperpathAasIdentifier):
        body (SubmodelDescriptor):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Result, SubmodelDescriptor]]
    """

    kwargs = _get_kwargs(
        aas_identifier=aas_identifier,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    aas_identifier: "PostSubmodelDescriptorThroughSuperpathAasIdentifier",
    *,
    client: Union[AuthenticatedClient, Client],
    body: SubmodelDescriptor,
) -> Optional[Union[Result, SubmodelDescriptor]]:
    """Creates a new Submodel Descriptor, i.e. registers a submodel

    Args:
        aas_identifier (PostSubmodelDescriptorThroughSuperpathAasIdentifier):
        body (SubmodelDescriptor):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Result, SubmodelDescriptor]
    """

    return sync_detailed(
        aas_identifier=aas_identifier,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    aas_identifier: "PostSubmodelDescriptorThroughSuperpathAasIdentifier",
    *,
    client: Union[AuthenticatedClient, Client],
    body: SubmodelDescriptor,
) -> Response[Union[Result, SubmodelDescriptor]]:
    """Creates a new Submodel Descriptor, i.e. registers a submodel

    Args:
        aas_identifier (PostSubmodelDescriptorThroughSuperpathAasIdentifier):
        body (SubmodelDescriptor):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Result, SubmodelDescriptor]]
    """

    kwargs = _get_kwargs(
        aas_identifier=aas_identifier,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    aas_identifier: "PostSubmodelDescriptorThroughSuperpathAasIdentifier",
    *,
    client: Union[AuthenticatedClient, Client],
    body: SubmodelDescriptor,
) -> Optional[Union[Result, SubmodelDescriptor]]:
    """Creates a new Submodel Descriptor, i.e. registers a submodel

    Args:
        aas_identifier (PostSubmodelDescriptorThroughSuperpathAasIdentifier):
        body (SubmodelDescriptor):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Result, SubmodelDescriptor]
    """

    return (
        await asyncio_detailed(
            aas_identifier=aas_identifier,
            client=client,
            body=body,
        )
    ).parsed
