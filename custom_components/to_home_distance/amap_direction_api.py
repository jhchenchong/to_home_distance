"""
高德地图路径规划API
"""
import httpx
from .const import (
    CONF_API_URL,
    CONF_REQUEST_TIMEOUT,
    CONF_TRANSPORTATION_MODES,
    CONF_MODE_ROUTE_KEY,
    CONF_DISTANCE_KEY,
    CONF_DURATION_KEY,
    CONF_STATUS_KEY,
    CONF_ROUTE_KEY,
    CONF_PATHS_KEY,
    CONF_STATUS_SUCCESS
)


class AMapDirectionAPI:
    """
    高德地图路径规划API
    """

    def __init__(self, api_key, origin, destination, mode_of_transportation) -> None:
        self._api_key = api_key
        self._origin = origin
        self._destination = destination
        self._mode_of_transportation = mode_of_transportation

    async def perform_request(self):
        """
        Perform the request asynchronously.
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self._get_request_url(),
                params=self._get_request_params(),
                timeout=CONF_REQUEST_TIMEOUT
            )
            return response.json()

    def extract_distance_and_duration(self, data):
        """
        Extract distance and duration from data.
        """
        if data is None or data[CONF_STATUS_KEY] != CONF_STATUS_SUCCESS:
            return None
        res = data[CONF_ROUTE_KEY][CONF_PATHS_KEY][0]
        distance, duration = res[CONF_DISTANCE_KEY], res[CONF_DURATION_KEY]
        return {
            CONF_DISTANCE_KEY: distance,
            CONF_DURATION_KEY: duration
        }

    def _get_request_url(self):
        """
        Get the request url.
        """
        mode_route = CONF_TRANSPORTATION_MODES[self._mode_of_transportation][CONF_MODE_ROUTE_KEY]
        if mode_route is not None:
            return '/'.join([CONF_API_URL, mode_route])
        return None

    def _get_request_params(self):
        """
        Get the request params.
        """
        return {
            "key": self._api_key,
            "origin": self._origin,
            "destination": self._destination
        }
