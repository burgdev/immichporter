"""Immich API client implementation."""

import json
import logging
import httpx
from typing import Optional, List, Union

from pydantic import BaseModel

from .models import AlbumResponse

logger = logging.getLogger(__name__)


class ImmichAPIError(Exception):
    """Base exception for Immich API errors."""

    pass


class ImmichAPI:
    """A client for interacting with the Immich API.

    This is a minimal implementation that only includes the albums endpoint.
    """

    def __init__(self, base_url: str, api_key: str, verify_ssl: bool = True):
        """Initialize the Immich API client.

        Args:
            base_url: Base URL of the Immich server (e.g., 'http://localhost:2283')
                     This should be the base URL without the '/api' suffix
            api_key: API key for authentication
            verify_ssl: Whether to verify SSL certificates (default: True)
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.verify_ssl = verify_ssl
        self._client = None

    async def __aenter__(self):
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "x-api-key": self.api_key,  # Changed from x-immich-api-key to x-api-key
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            verify=self.verify_ssl,
            timeout=30.0,
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            await self._client.aclose()
        self._client = None

    async def _request(
        self,
        method: str,
        endpoint: str,
        model: Optional[type[BaseModel]] = None,
        **kwargs,
    ) -> Union[BaseModel, dict, list]:
        """Make an HTTP request to the Immich API.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint (e.g., '/album')
            model: Pydantic model to parse the response into
            **kwargs: Additional arguments to pass to the request

        Returns:
            The parsed response as the specified model, a list of models, or as a dict if no model is provided

        Raises:
            ImmichAPIError: If the request fails or returns an error
        """
        if not self._client:
            raise ImmichAPIError(
                "Client not initialized. Use 'async with ImmichAPI(...)'"
            )

        try:
            # Ensure endpoint starts with a slash
            if not endpoint.startswith("/"):
                endpoint = f"/{endpoint}"

            # Log the request details for debugging
            logger.debug(f"Making {method} request to {self.base_url}{endpoint}")
            if "json" in kwargs:
                logger.debug(f"Request body: {kwargs['json']}")

            # Make the request
            response = await self._client.request(method, endpoint, **kwargs)

            # Log the response status and headers for debugging
            logger.debug(f"Response status: {response.status_code}")
            logger.debug(f"Response headers: {dict(response.headers)}")

            # Get the response content
            try:
                content = await response.aread()
                response_text = content.decode("utf-8")
                logger.debug(f"Response text: {response_text}")

                # Parse the JSON response
                try:
                    data = json.loads(response_text) if content else None
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse JSON response: {e}")
                    logger.error(f"Response content: {response_text}")
                    raise ImmichAPIError(f"Invalid JSON response: {e}") from e
            except Exception as e:
                logger.error(f"Failed to read response content: {e}")
                raise ImmichAPIError(f"Failed to read response: {e}") from e

            # Check for errors
            try:
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                error_msg = f"HTTP error {e.response.status_code}"
                if data and isinstance(data, dict):
                    error_msg += f": {data.get('message', str(data))}"
                logger.error(error_msg)
                raise ImmichAPIError(error_msg) from e

            # Handle no content
            if response.status_code == 204 or not data:  # No content
                return None

            # If a model is provided, parse the response into it
            if model is not None:
                try:
                    if isinstance(data, list):
                        # If it's a list, validate each item
                        logger.debug(
                            f"Validating list of {len(data)} items with model {model.__name__}"
                        )
                        return [model.model_validate(item) for item in data]
                    elif hasattr(model, "__origin__") and model.__origin__ is list:
                        # If the model is List[SomeModel], validate the entire list
                        item_model = model.__args__[0]
                        logger.debug(
                            f"Validating list with item model {item_model.__name__}"
                        )
                        return [item_model.model_validate(item) for item in data]
                    else:
                        # Otherwise, validate as a single model
                        logger.debug(
                            f"Validating single item with model {model.__name__}"
                        )
                        return model.model_validate(data)
                except Exception as e:
                    logger.error(f"Failed to validate response with model {model}: {e}")
                    logger.error(f"Response data: {data}")
                    raise ImmichAPIError(f"Failed to validate response: {e}") from e

            return data

        except httpx.HTTPStatusError as e:
            error_msg = f"HTTP error {e.response.status_code}"
            if e.response.content:
                try:
                    error_data = e.response.json()
                    error_msg = f"{error_msg}: {error_data.get('message', str(e.response.content, 'utf-8', errors='replace'))}"
                    logger.error(f"Error details: {error_data}")
                except Exception as json_error:
                    error_text = str(e.response.content, "utf-8", errors="replace")
                    error_msg = f"{error_msg}: {error_text}"
                    logger.error(f"Could not parse error response: {json_error}")

            logger.error(f"Request failed: {error_msg}")
            logger.error(f"Request URL: {method} {e.request.url}")
            logger.error(f"Request headers: {dict(e.request.headers)}")

            if hasattr(e, "response") and hasattr(e.response, "headers"):
                logger.error(f"Response headers: {dict(e.response.headers)}")

            raise ImmichAPIError(error_msg) from e

        except Exception as e:
            error_msg = f"Request failed: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise ImmichAPIError(error_msg) from e

    # Album endpoints

    async def get_all_albums(self) -> List[AlbumResponse]:
        """Get all albums from the Immich server."""
        # The API returns a list of albums directly
        result = await self._request(
            "GET",
            "/api/albums",  # Correct endpoint for listing all albums
            model=AlbumResponse,  # Each item in the list will be validated against AlbumResponse
        )

        # Ensure we return a list, even if the API returns a single item
        if not isinstance(result, list):
            result = [result] if result is not None else []

        return result
