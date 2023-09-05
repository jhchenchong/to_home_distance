"""AMap Direction API"""
from enum import Enum
import logging
import requests

_LOGGER = logging.getLogger(__name__)

BASE_URL = 'https://restapi.amap.com'


class TransportationMode(Enum):
    """
    Transportation mode.
    1: walking
    2: transit/integrated
    3: driving
    4: bicycling
    """
    WALKING = 1
    TRANSIT_INTEGRATED = 2
    DRIVING = 3
    BICYCLING = 4


class ApiVersion(Enum):
    """API version."""
    V3 = 'v3'
    V4 = 'v4'


class SuccessCode(Enum):
    """Success code."""
    V3 = '1'
    V4 = '0'


class SuccessKey(Enum):
    """Success key."""
    V3 = 'status'
    V4 = 'errorcode'


class ResponseKey(Enum):
    """Response key."""
    V3 = 'route'
    V4 = 'data'


class Location:
    """Location."""

    def __init__(self, longitude, latitude) -> None:
        self._longitude = longitude
        self._latitude = latitude

    @property
    def longitude(self):
        """Return the longitude."""
        return self._longitude

    @property
    def latitude(self):
        """Return the latitude."""
        return self._latitude


class RoutePlanningParameters:
    """Route planning parameters."""

    def __init__(
        self, api_key: str, origin: Location, destination: Location, mode: TransportationMode
    ) -> None:
        self._api_key = api_key
        self._origin = origin
        self._destination = destination
        self._mode = mode

    @property
    def api_key(self):
        """Return the API key."""
        return self._api_key

    @property
    def origin(self):
        """Return the origin."""
        return self._origin

    @property
    def destination(self):
        """Return the destination."""
        return self._destination

    @property
    def mode(self):
        """Return the mode."""
        return self._mode


class AMapDirectionAPI:
    """AMap Direction API"""

    def __init__(self, params: RoutePlanningParameters) -> None:
        self.params = params

    def parse_data(self, data):
        """Parse the data."""
        api_version = self.api_version()
        success_key = SuccessKey.V3 if api_version == ApiVersion.V3 else SuccessKey.V4
        success_code = SuccessCode.V3 if api_version == ApiVersion.V3 else SuccessCode.V4
        data_key = ResponseKey.V3 if api_version == ApiVersion.V3 else ResponseKey.V4
        if data is None or data.get(success_key.value) != success_code.value:
            return None
        res = data[data_key.value][0]
        distance, duration = res['distance'], res['duration']
        return {'distance': distance, 'duration': duration}

    def get_request_url(self):
        """Get the request url."""
        mode_route = self.params.mode
        api_version = self.api_version()
        url = (
            f"{BASE_URL}/"
            f"{api_version.value}/"
            f"direction/"
            f"{mode_route.name.replace('_', '/').lower()}"
        )
        return url

    def api_version(self):
        """Get the API version."""
        return ApiVersion.V3 if self.params.mode != TransportationMode.BICYCLING else ApiVersion.V4

    def get_request_params(self):
        """Get the request parameters."""
        key = self.params.api_key
        origin = f"{self.params.origin.longitude},{self.params.origin.latitude}"
        destination = f"{self.params.destination.longitude},{self.params.destination.latitude}"
        return {'key': key, 'origin': origin, 'destination': destination}

    def perform_request(self):
        """Perform the request."""
        url = self.get_request_url()
        params = self.get_request_params()
        try:
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as error:
            _LOGGER.error("Error fetching data: %s failed with %s", url, error)
            return None

    def extract_distance_duration(self, data):
        """Extract distance and duration from data."""
        return self.parse_data(data)
