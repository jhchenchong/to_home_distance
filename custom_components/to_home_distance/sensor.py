"""
This component provides support for AMaps To Home Distance sensor.
"""
import logging
from collections.abc import Callable
from typing import Union
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import (
    ConfigType,
    HomeAssistantType,
)
from homeassistant.helpers.entity import Entity
from .amap_direction_api import AMapDirectionAPI
from .const import (
    DOMAIN,
    CONF_API_KEY,
    CONF_HOME_LONGITUDE,
    CONF_HOME_LATITUDE,
    CONF_DEVICE_TRACKER_ENTITY_ID,
    CONF_MODE_OF_TRANSPORTATION,
    CONF_LONGITUDE_KEY,
    CONF_LATITUDE_KEY
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: Callable
) -> None:
    """
    Setup sensors from a config entry created in the integrations UI.
    """
    await setup_sensors(hass, config_entry, async_add_entities)


async def async_setup_platform(
        hass: HomeAssistantType,
        config: ConfigType,
        async_add_entities: Callable,
) -> None:
    """
    Set up the sensor platform.
    """
    await setup_sensors(hass, config, async_add_entities)


async def setup_sensors(
        hass: HomeAssistantType,
        config: Union[ConfigEntry, ConfigType],
        async_add_entities: Callable
) -> None:
    """
    Common setup function for both entry and platform setup.
    """
    config_data = config if isinstance(config, dict) else hass.data[DOMAIN][config.entry_id]
    device_tracker_entity_id = config_data[CONF_DEVICE_TRACKER_ENTITY_ID]
    device_tracker_state = hass.states.get(device_tracker_entity_id)

    if device_tracker_state:
        attributes = device_tracker_state.attributes
        longitude, latitude = attributes.get(CONF_LONGITUDE_KEY), attributes.get(CONF_LATITUDE_KEY)

        if longitude and latitude:
            origin = combine_longitude_latitude(longitude, latitude)
            home_location = config_data[CONF_HOME_LONGITUDE], config_data[CONF_HOME_LATITUDE]
            destination = combine_longitude_latitude(home_location[0], home_location[1])
            mode = config_data[CONF_MODE_OF_TRANSPORTATION]

            api = AMapDirectionAPI(
                config_data[CONF_API_KEY],
                origin,
                destination,
                mode
            )

            sensors = [ToHomeDistanceSensor(api, mode)]
            async_add_entities(sensors, True)


def combine_longitude_latitude(longitude, latitude):
    """
    Combine longitude and latitude.
    """
    return ','.join([longitude, latitude])


class ToHomeDistanceSensor(Entity):
    """
    To Home Distance sensor.
    """

    def __init__(self, api: AMapDirectionAPI, mode) -> None:
        self._api = api
        self._mode = mode
        self._state = None
