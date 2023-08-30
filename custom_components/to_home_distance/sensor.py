"""
This component provides support for AMaps To Home Distance sensor.
"""
from datetime import timedelta
import logging
import requests
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import ATTR_ATTRIBUTION
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from const import (
    DOMAIN,
    CONF_API_URL,
    CONF_API_KEY,
    CONF_HOME_LATITUDE,
    CONF_HOME_LONGITUDE,
    CONF_DEVICE_TRACKER_ENTITY_ID,
    UPDATE_INTERVAL,
    DEFAULT_UPDATE_INTERVAL
)

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_API_KEY): cv.string,
        vol.Required(CONF_HOME_LATITUDE): cv.string,
        vol.Required(CONF_HOME_LONGITUDE): cv.string,
        vol.Required(CONF_DEVICE_TRACKER_ENTITY_ID): cv.string,
        vol.Optional(
            UPDATE_INTERVAL,
            default=timedelta(minutes=DEFAULT_UPDATE_INTERVAL)
        ): cv.time_period,
    }
)


def setup_platform(hass, config, add_entities, _=None):
    """
    Set up the To Home Distance sensor.
    """
    add_entities([ToHomeDistanceSensor(hass, config)], True)


class ToHomeDistanceSensor(Entity):
    """
    To Home Distance sensor.
    """

    def __init__(self, hass, config):
        self.hass = hass
        self._api_key = config.get(CONF_API_KEY)
        self._home_location = config.get(CONF_HOME_LATITUDE), config.get(CONF_HOME_LONGITUDE)
        self._device_tracker_entity_id = config.get(CONF_DEVICE_TRACKER_ENTITY_ID)
        self._update_interval = config.get(UPDATE_INTERVAL)
        self._state = None
        self._attributes = {ATTR_ATTRIBUTION: "Service provided by AMaps"}

    @property
    def name(self):
        """
        Return the name of the sensor.
        """
        return DOMAIN

    @property
    def state(self):
        """
        Return the state of the sensor.
        """
        return self._state

    @property
    def device_state_attributes(self):
        """
        Return the state attributes.
        """
        return self._attributes

    def update(self):
        """
        Update the state of the sensor.
        """
        json_data = self._request()
        data = self._parse_data(json_data)
        self._set_state(data)
        self._set_attributes(data)

    def _request(self):
        """
        Request the data from the API.
        """
        try:
            response = requests.get(
                CONF_API_URL,
                params=self._get_request_params(),
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as error:
            _LOGGER.error("Error while retrieving data: %s", error)
            return None

    def _get_request_params(self):
        """
        Get the request params.
        """
        return {
            "key": self._api_key,
            "origins": self._origin(),
            "destination": self._destination(),
            "type": 1,
        }

    def _origin(self):
        """
        Get the origin.
        """
        return ','.join(map(str, self._get_device_tracker_location()))

    def _destination(self):
        """
        Get the origin.
        """
        return ','.join(map(str, self._home_location))

    def _get_device_tracker_location(self):
        """
        Get the location of the device tracker.
        """
        device_tracker_state = self.hass.states.get(self._device_tracker_entity_id)
        if device_tracker_state:
            attributes = device_tracker_state.attributes
            longitude, latitude = attributes.get("longitude"), attributes.get("latitude")
            if longitude is not None and latitude is not None:
                return latitude, longitude
        return None

    def _parse_data(self, data):
        """
        Parse the data.
        """
        if data is None:
            return None
        if data["status"] == "1":
            return data["results"][0]
        _LOGGER.error("Error while retrieving data: %s", data["info"])
        return None

    def _set_state(self, data):
        """
        Set the state.
        """
        self._state = data["distance"] if data else None

    def _set_attributes(self, data):
        """
        Set the attributes.
        """
        if data:
            self._attributes = {
                ATTR_ATTRIBUTION: "Service provided by AMaps",
                "duration": data["duration"],
                "origin": data["origin_id"],
                "destination": data["dest_id"],
            }
        else:
            self._attributes = None