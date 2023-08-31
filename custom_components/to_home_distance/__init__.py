"""
This is the To Home Distance component.
"""
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform


PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """
    Set up To Home Distance from a config entry.
    """
    print(hass)
    print(entry)
    return True
