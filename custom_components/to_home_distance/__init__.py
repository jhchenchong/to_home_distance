"""
This is the To Home Distance component.
"""
import logging
from homeassistant import core
from const import (
    DOMAIN,
    CONF_API_KEY,
    CONF_HOME_LATITUDE,
    CONF_HOME_LONGITUDE,
    CONF_DEVICE_TRACKER_ENTITY_ID,
    CONF_UPDATE_INTERVAL
)


_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: core.HomeAssistant, config: dict) -> bool:
    """
    Set up the To Home Distance component.
    """
    if not config.get(CONF_API_KEY):
        _LOGGER.error("Missing api_key in configuration")
        return False

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][CONF_API_KEY] = config[CONF_API_KEY]
    hass.data[DOMAIN][CONF_HOME_LATITUDE] = config[CONF_HOME_LATITUDE]
    hass.data[DOMAIN][CONF_HOME_LONGITUDE] = config[CONF_HOME_LONGITUDE]
    hass.data[DOMAIN][CONF_DEVICE_TRACKER_ENTITY_ID] = config[CONF_DEVICE_TRACKER_ENTITY_ID]
    hass.data[DOMAIN][CONF_UPDATE_INTERVAL] = config[CONF_UPDATE_INTERVAL]
    return True
