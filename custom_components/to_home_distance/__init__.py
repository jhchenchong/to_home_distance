"""
The to_home_distance component.
"""
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """
    Setup sensors from a config entry created in the integrations UI.
    """
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(config_entry, Platform.SENSOR)
    )
    return True
