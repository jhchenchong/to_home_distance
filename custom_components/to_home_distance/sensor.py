"""
This component provides support for AMaps To Home Distance sensor.
"""
from typing import Any
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change
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
from .utils import (
    format_distance,
    format_duration,
    format_and_validate_coordinates
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
        self._attr_unique_id = config[CONF_DEVICE_TRACKER_ENTITY_ID]
        self._name = "To Home Distance " + config[CONF_DEVICE_TRACKER_ENTITY_ID]
        self._state = None
        self._attrs = {}

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return self._attrs

    async def async_added_to_hass(self):
        # 在这里订阅实体状态变化事件
        async_track_state_change(
            self.hass,
            self._config[CONF_DEVICE_TRACKER_ENTITY_ID],
            self._device_tracker_state_changed
        )

    async def _device_tracker_state_changed(self, entity_id, old_state, new_state):
        """
        Callback when device tracker state changed.
        """
        device_state = new_state.state
        if device_state == "home":
            self._state = "在家"
        else:
            await self.async_update()

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
            self._state = format_distance(data[CONF_DISTANCE_KEY])
            self._attrs = {
                CONF_DISTANCE_KEY: self._state,
                CONF_DURATION_KEY: format_duration(data[CONF_DURATION_KEY]),
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
        Get origin coordinates.
        """
        entity_id = self._config[CONF_DEVICE_TRACKER_ENTITY_ID]
        return self._get_coordinates_from_entity(entity_id)

    def _get_destination(self):
        """
        Get destination coordinates for home.
        """
        return self._get_coordinates_from_entity(ZONE_HOME)

    def _get_coordinates_from_entity(self, entity_id):
        """
        Get coordinates from entity state.
        """
        state = self.hass.states.get(entity_id)
        if state is None:
            return None
        longitude = state.attributes.get(CONF_LONGITUDE_KEY)
        latitude = state.attributes.get(CONF_LATITUDE_KEY)
        return format_and_validate_coordinates(longitude, latitude)
