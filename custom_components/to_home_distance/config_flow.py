"""
Config flow for To Home Distance.
"""
from typing import Optional, Any
from collections.abc import Mapping
from homeassistant.config_entries import ConfigFlow
from homeassistant.helpers import config_validation as cv
import voluptuous as vol
from .validation import (
    validate_api_key,
    validate_domain,
    validate_mode,
    validate_update_interval
)
from .const import (
    DOMAIN,
    CONF_API_KEY,
    CONF_DEVICE_TRACKER_ENTITY_ID,
    CONF_MODE_OF_TRANSPORTATION,
    CONF_UPDATE_INTERVAL,
    CONF_DEFAULT_UPDATE_INTERVAL,
    CONF_DEFAULT_MODE_OF_TRANSPORTATION
)


CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_API_KEY): cv.string,
        vol.Required(CONF_DEVICE_TRACKER_ENTITY_ID): cv.string,
        vol.Optional(
            CONF_MODE_OF_TRANSPORTATION,
            default=CONF_DEFAULT_MODE_OF_TRANSPORTATION
        ): cv.positive_int,
        vol.Optional(
            CONF_UPDATE_INTERVAL,
            default=CONF_DEFAULT_UPDATE_INTERVAL
        ): cv.positive_int
    }
)


async def validate_input(user_input):
    """
    Validate the user input allows us to connect.
    """
    errors: dict[str, str] = {}
    device_tracker_entity_id = user_input[CONF_DEVICE_TRACKER_ENTITY_ID]
    if not validate_domain(device_tracker_entity_id):
        errors["base"] = CONF_DEVICE_TRACKER_ENTITY_ID
    mode_of_transportation = user_input[CONF_MODE_OF_TRANSPORTATION]
    if not validate_mode(mode_of_transportation):
        errors["base"] = CONF_DEFAULT_MODE_OF_TRANSPORTATION
    update_interval = user_input[CONF_UPDATE_INTERVAL]
    if not validate_update_interval(update_interval):
        errors["base"] = CONF_UPDATE_INTERVAL
    api_key = user_input[CONF_API_KEY]
    try:
        await validate_api_key(api_key)
    except ValueError:
        errors["base"] = CONF_API_KEY
    return errors


class ToHomeDistanceConfigFlow(ConfigFlow, domain=DOMAIN):
    """
    Handle a config flow for To Home Distance.
    """

    data = Optional[Mapping[str, Any]]

    async def async_step_user(self, user_input: Optional[Mapping[str, Any]] = None):
        """
        Handle the initial step.
        """
        errors: dict[str, str] = {}
        if user_input is not None:
            errors = await validate_input(user_input)
            if not errors:
                self.data = user_input
                return self.async_create_entry(
                    title="To Home Distance",
                    data=self.data
                )
        return self.async_show_form(step_id="user", data_schema=CONFIG_SCHEMA, errors=errors)
