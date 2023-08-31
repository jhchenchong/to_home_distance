"""Config flow for To Home Distance."""
from typing import Optional, Any
from homeassistant.config_entries import ConfigFlow
from homeassistant.helpers import config_validation as cv
import voluptuous as vol
from .const import (
    DOMAIN,
    CONF_API_KEY,
    CONF_HOME_LONGITUDE,
    CONF_HOME_LATITUDE,
    CONF_DEVICE_TRACKER_ENTITY_ID,
    CONF_MODE_OF_TRANSPORTATION,
    CONF_UPDATE_INTERVAL
)

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_API_KEY): cv.string,
        vol.Required(CONF_HOME_LONGITUDE): cv.string,
        vol.Required(CONF_HOME_LATITUDE): cv.string,
        vol.Required(CONF_DEVICE_TRACKER_ENTITY_ID): cv.string,
        # vol.Optional(
        #     CONF_UPDATE_INTERVAL,
        #     default=timedelta(minutes=CONF_DEFAULT_UPDATE_INTERVAL)
        # ): cv.time_period,
        # vol.Optional(
        #     CONF_MODE_OF_TRANSPORTATION,
        #     default=CONF_DEFAULT_MODE_OF_TRANSPORTATION
        # ): cv.positive_int
    }
)


class ToHomeDistanceConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for To Home Distance."""

    async def async_step_user(self, user_input: Optional[dict[str, Any]] = None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            api_key = user_input[CONF_API_KEY]
            home_longitude = user_input[CONF_HOME_LONGITUDE]
            home_latitude = user_input[CONF_HOME_LATITUDE]
            device_tracker_entity_id = user_input[CONF_DEVICE_TRACKER_ENTITY_ID]
            mode_of_transportation = user_input[CONF_MODE_OF_TRANSPORTATION]
            update_interval = user_input[CONF_UPDATE_INTERVAL]
            return self.async_create_entry(
                title="To Home Distance",
                data={
                    CONF_API_KEY: api_key,
                    CONF_HOME_LONGITUDE: home_longitude,
                    CONF_HOME_LATITUDE: home_latitude,
                    CONF_DEVICE_TRACKER_ENTITY_ID: device_tracker_entity_id,
                    CONF_MODE_OF_TRANSPORTATION: mode_of_transportation,
                    CONF_UPDATE_INTERVAL: update_interval
                }
            )
        return self.async_show_form(step_id="user", data_schema=CONFIG_SCHEMA, errors=errors)
