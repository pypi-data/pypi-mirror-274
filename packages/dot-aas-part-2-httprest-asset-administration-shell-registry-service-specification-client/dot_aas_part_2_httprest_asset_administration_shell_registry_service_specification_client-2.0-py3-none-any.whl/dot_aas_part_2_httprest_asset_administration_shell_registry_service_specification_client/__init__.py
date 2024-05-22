"""A client library for accessing DotAAS Part 2 | HTTP/REST | Asset Administration Shell Registry Service Specification"""

from .client import AuthenticatedClient, Client

__all__ = (
    "AuthenticatedClient",
    "Client",
)
