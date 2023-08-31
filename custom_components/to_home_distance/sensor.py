# """
# This component provides support for AMaps To Home Distance sensor.
# """
# from datetime import timedelta
# from collections.abc import Callable
# from homeassistant.helpers.typing import (
#     ConfigType,
#     DiscoveryInfoType,
#     HomeAssistantType,
# )
# import logging
# import requests
# import voluptuous as vol
# from homeassistant.components.sensor import PLATFORM_SCHEMA
# from homeassistant.const import ATTR_ATTRIBUTION
# import homeassistant.helpers.config_validation as cv
# from homeassistant.helpers.entity import Entity
# from const import (
#     DOMAIN,
#     CONF_API_URL,
#     CONF_API_KEY,
#     CONF_HOME_LONGITUDE,
#     CONF_HOME_LATITUDE,
#     CONF_DEVICE_TRACKER_ENTITY_ID,
#     CONF_MODE_OF_TRANSPORTATION,
#     CONF_DEFAULT_MODE_OF_TRANSPORTATION,
#     CONF_UPDATE_INTERVAL,
#     CONF_DEFAULT_UPDATE_INTERVAL,
#     CONF_TRANSPORTATION_MODES,
#     CONF_MODE_ROUTE_KEY,
#     CONF_MODE_DESC_KEY,
#     CONF_REQUEST_TIMEOUT
# )
# from custom_components.to_home_distance.core.amap_api import AMapAPI

# _LOGGER = logging.getLogger(__name__)


# async def async_setup_platform(
#         hass: HomeAssistantType,
#         config: ConfigType,
#         async_add_entities: Callable,
#         discovery_info: DiscoveryInfoType | None = None
# ):
#     """
#     Set up the To Home Distance sensor.
#     """
#     async_add_entities([ToHomeDistanceSensor(config)], True)


# class ToHomeDistanceSensor(Entity):
#     """
#     To Home Distance sensor.
#     """

#     def __init__(self, api: AMapAPI):
#         self.api = api
#         self._state = None
#         self._attributes = {ATTR_ATTRIBUTION: "Service provided by AMaps"}

#     @property
#     def name(self):
#         """
#         Return the name of the sensor.
#         """
#         return DOMAIN

#     @property
#     def state(self):
#         """
#         Return the state of the sensor.
#         """
#         return self._state

#     @property
#     def device_state_attributes(self):
#         """
#         Return the state attributes.
#         """
#         return self._attributes

#     def update(self):
#         """
#         Update the state of the sensor.
#         """
#         json_data = self._request()
#         data = self._parse_data(json_data)
#         self._set_state(data)
#         self._set_attributes(data)

#     def _request(self):
#         """
#         Request the data from the API.
#         """
#         try:
#             response = requests.get(
#                 self._get_request_url(),
#                 params=self._get_request_params(),
#                 timeout=CONF_REQUEST_TIMEOUT
#             )
#             response.raise_for_status()
#             return response.json()
#         except requests.exceptions.RequestException as error:
#             _LOGGER.error("Error while retrieving data: %s", error)
#             return None

#     def _get_request_url(self):
#         """
#         Get the request url.
#         """
#         mode_route = CONF_TRANSPORTATION_MODES[self._mode_of_transportation][CONF_MODE_ROUTE_KEY]
#         if mode_route is not None:
#             return '/'.join([CONF_API_URL, mode_route])
#         return None

#     def _get_request_params(self):
#         """
#         Get the request params.
#         """
#         return {
#             "key": self._api_key,
#             "origins": self._origin(),
#             "destination": self._destination()
#         }

#     def _origin(self):
#         """
#         Get the origin.
#         """
#         return ','.join(map(str, self._get_device_tracker_location()))

#     def _destination(self):
#         """
#         Get the destination.
#         """
#         return ','.join(map(str, self._home_location))

#     def _get_device_tracker_location(self):
#         """
#         Get the location of the device tracker.
#         """
#         device_tracker_state = self.hass.states[self._device_tracker_entity_id]
#         if device_tracker_state:
#             attributes = device_tracker_state.attributes
#             longitude, latitude = attributes["longitude"], attributes["latitude"]
#             if longitude is not None and latitude is not None:
#                 return longitude, latitude
#         return None

#     def _parse_data(self, data):
#         """
#         Parse the data.
#         """
#         if data is None:
#             return None
#         if data["status"] == "1":
#             res = data["route"]["paths"][0]
#             distance, duration = res["distance"], res["duration"]
#             return {
#                 "distance": distance,
#                 "duration": duration
#             }
#         _LOGGER.error("Error while retrieving data: %s", data["info"])
#         return None

#     def _set_state(self, data):
#         """
#         Set the state.
#         """
#         self._state = data["distance"] if data else None

#     def _set_attributes(self, data):
#         """
#         Set the attributes.
#         """
#         if data:
#             self._attributes = {
#                 ATTR_ATTRIBUTION: "Service provided by AMaps",
#                 "duration": data["duration"],
#                 "mode": self._cover_mode_of_transportation()
#             }
#         else:
#             self._attributes = None

#     def _cover_mode_of_transportation(self):
#         """
#         Cover the mode of transportation.
#         """
#         return CONF_TRANSPORTATION_MODES[self._mode_of_transportation][CONF_MODE_DESC_KEY]
