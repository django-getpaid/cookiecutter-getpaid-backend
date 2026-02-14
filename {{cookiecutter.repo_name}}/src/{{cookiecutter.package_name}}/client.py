"""{{ cookiecutter.gateway_name }} API client."""

import logging
from typing import Any

import httpx


logger = logging.getLogger(__name__)


class {{ cookiecutter.client_class_name }}:
    """Async HTTP client for the {{ cookiecutter.gateway_name }} API.

    Can be used as an async context manager or standalone.

    Usage::

        async with {{ cookiecutter.client_class_name }}(api_url="...") as client:
            response = await client.some_method()
    """

    def __init__(
        self,
        api_url: str,
        *,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self.api_url = api_url.rstrip("/")
        self._client = client
        self._owns_client = client is None
        self.last_response: httpx.Response | None = None

    async def __aenter__(self) -> "{{ cookiecutter.client_class_name }}":
        if self._owns_client:
            self._client = httpx.AsyncClient()
        return self

    async def __aexit__(self, *exc: Any) -> None:
        if self._owns_client and self._client is not None:
            await self._client.aclose()
            self._client = None

    @property
    def client(self) -> httpx.AsyncClient:
        """Return the underlying HTTP client, creating one if needed."""
        if self._client is None:
            self._client = httpx.AsyncClient()
            self._owns_client = True
        return self._client

    # TODO: Add gateway-specific API methods here.
    # Example:
    #
    # async def create_payment(self, **kwargs) -> dict:
    #     response = await self.client.post(
    #         f"{self.api_url}/payments",
    #         json=kwargs,
    #     )
    #     self.last_response = response
    #     response.raise_for_status()
    #     return response.json()
