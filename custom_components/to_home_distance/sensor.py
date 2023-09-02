"""
This component provides support for AMaps To Home Distance sensor.
"""
from typing import Any
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .amap_direction_api import AMapDirectionAPI
from .const import (
    ZONE_HOME,
    CONF_API_KEY,
    CONF_DEVICE_TRACKER_ENTITY_ID,
    CONF_MODE_OF_TRANSPORTATION,
    CONF_LONGITUDE_KEY,
    CONF_LATITUDE_KEY,
    CONF_DISTANCE_KEY,
    CONF_DURATION_KEY
)
from .validation import (
    validate_longitude,
    validate_latitude
)


async def async_setup_entry(
        _: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback
) -> None:
    """
    Setup sensors from a config entry created in the integrations UI.
    """
    config_data = config_entry.data
    sensors = [ToHomeDistanceSensor(config_data)]
    async_add_entities(sensors, True)


class ToHomeDistanceSensor(Entity):
    """
    To Home Distance sensor.
    """

    def __init__(self, config) -> None:
        self._config = config
        self._state = None
        self._attr_unique_id = "hello_demo"
        self._name = "ccdemo " + "hello_demo"
        self._state = None
        self._attrs = {}
        self._icon = "mdi:poll"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """Icon to use in the frontend."""
        return self._icon

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return self._attrs

    async def async_update(self) -> None:
        """
        Update state.
        """
        params = self._get_request_parameters()
        if params is None:
            return
        api_key, origin, destination, mode_of_transportation = params
        data = await self._fetch_distance_and_duration(
            api_key,
            origin,
            destination,
            mode_of_transportation
        )
        if data is not None:
            self._state = self.convert_distance(data[CONF_DISTANCE_KEY])
            self._attrs = {
                CONF_DISTANCE_KEY: self._state,
                CONF_DURATION_KEY: self.convert_duration(data[CONF_DURATION_KEY]),
            }

    async def _fetch_distance_and_duration(
            self,
            api_key,
            origin,
            destination,
            mode_of_transportation
    ):
        """
        Fetch distance and duration from API.
        """
        session = async_get_clientsession(self.hass)
        api = AMapDirectionAPI(session, api_key, origin, destination, mode_of_transportation)
        response = await api.perform_request()

        return api.extract_distance_and_duration(response)

    def _get_request_parameters(self):
        """
        Get request parameters.
        """
        origin = self._get_origin()
        destination = self._get_destination()
        if origin is None or destination is None:
            return None
        api_key = self._config[CONF_API_KEY]
        mode_of_transportation = self._config[CONF_MODE_OF_TRANSPORTATION]

        return api_key, origin, destination, mode_of_transportation

    def _get_origin(self):
        """
        Get origin.
        """
        entity_id = self._config[CONF_DEVICE_TRACKER_ENTITY_ID]
        return self._from_entity_state_get_location(entity_id)

    def _get_destination(self):
        """
        Get destination.
        """
        return self._from_entity_state_get_location(ZONE_HOME)

    def _from_entity_state_get_location(self, entity_id):
        """
        Get location from entity state.
        """
        state = self.hass.states.get(entity_id)
        if state is None:
            return None
        longitude = state.attributes.get(CONF_LONGITUDE_KEY)
        latitude = state.attributes.get(CONF_LATITUDE_KEY)
        return self.location(longitude, latitude)

    @staticmethod
    def location(longitude, latitude):
        """
        Location.
        """
        lng = ToHomeDistanceSensor.convert_and_round(longitude)
        lat = ToHomeDistanceSensor.convert_and_round(latitude)
        if not ToHomeDistanceSensor.is_valid_location(lng, lat):
            return None

        return ToHomeDistanceSensor.combine_longitude_latitude(lng, lat)

    @staticmethod
    def combine_longitude_latitude(longitude, latitude):
        """
        Combine longitude and latitude.
        """
        return f"{longitude},{latitude}"

    @staticmethod
    def convert_and_round(value):
        """
        Convert and round.
        """
        return str(round(float(value), 6))

    @staticmethod
    def is_valid_location(longitude, latitude):
        """
        Check if the location is valid.
        """
        return validate_longitude(longitude) and validate_latitude(latitude)

    @staticmethod
    def convert_distance(distance):
        """
        Convert distance.
        """
        return round(float(distance) / 1000, 2)

    @staticmethod
    def convert_duration(duration):
        """
        Convert duration.
        """
        return round(float(duration) / 60, 1)
