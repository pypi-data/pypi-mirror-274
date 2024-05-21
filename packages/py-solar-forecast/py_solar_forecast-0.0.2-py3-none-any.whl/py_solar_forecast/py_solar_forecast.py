"""Asynchronous Python client for the Forecast.Solar API."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Self

from aiohttp import BasicAuth, ClientSession

from .exceptions import (
    PySolarForecastAuthenticationError,
    PySolarForecastConfigError,
    PySolarForecastConnectionError,
    PySolarForecastError,
    PySolarForecastRatelimitError,
    PySolarForecastRequestError,
)
from .models import Estimate


@dataclass
class PySolarForecast:
    """Main class for handling connections with the Forecast.Solar API."""

    base_url: str

    azimuth: float
    declination: float
    kwp: float
    latitude: float
    longitude: float

    api_key: str | None = None
    loss_factor: float = 1.0

    session: ClientSession | None = None
    _close_session: bool = False

    async def _request(
        self,
        uri: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Handle a request to the Forecast.Solar API.

        A generic method for sending/handling HTTP requests done against
        the Forecast.Solar API.

        Args:
        ----
            uri: Request URI, for example, 'estimate'

        Returns:
        -------
            A Python dictionary (JSON decoded) with the response from
            the Forecast.Solar API.

        Raises:
        ------
            PySolarForecastAuthenticationError: If the API key is invalid.
            PySolarForecastConnectionError: An error occurred while communicating
                with the Forecast.Solar API.
            PySolarForecastError: Received an unexpected response from the
                Forecast.Solar API.
            PySolarForecastRequestError: There is something wrong with the
                variables used in the request.
            PySolarForecastRatelimitError: The number of requests has exceeded
                the rate limit of the Forecast.Solar API.

        """
        # Connect as normal
        if self.session is None:
            self.session = ClientSession()
            self._close_session = True

        # Build URL
        url = self.base_url
        if self.api_key:
            url += f"/{self.api_key}"
        url += uri

        response = await self.session.request(
            "GET",
            url,
            params=params,
        )

        if response.status in (502, 503):
            raise PySolarForecastConnectionError("The Forecast.Solar API is unreachable")

        if response.status == 400:
            data = await response.json()
            raise PySolarForecastRequestError(data["message"])

        if response.status in (401, 403):
            data = await response.json()
            raise PySolarForecastAuthenticationError(data["message"])

        if response.status == 422:
            data = await response.json()
            raise PySolarForecastConfigError(data["message"])

        if response.status == 429:
            data = await response.json()
            raise PySolarForecastRatelimitError(data["message"])

        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            text = await response.text()
            raise PySolarForecastError(
                "Unexpected response from the Forecast.Solar API",
                {"Content-Type": content_type, "response": text},
            )

        return await response.json()

    async def estimate(self) -> Estimate:
        """Get solar production estimations from the Forecast.Solar API.

        Returns
        -------
            A Estimate object, with a estimated production forecast.

        """
        params = {"lossFactor": self.loss_factor}
        data = await self._request(
            f"/estimate/{self.latitude}/{self.longitude}"
            f"/{self.declination}/{self.azimuth}/{self.kwp}",
            params=params,
        )

        return Estimate.from_dict(data)

    async def close(self) -> None:
        """Close open client session."""
        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self) -> Self:
        """Async enter.

        Returns
        -------
            The PySolarForecast object.

        """
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        """Async exit.

        Args:
        ----
            _exc_info: Exec type.

        """
        await self.close()
