"""
Constants for the To Home Distance integration.
"""
DOMAIN = "to_home_distance"

CONF_API_URL = "https://restapi.amap.com/v3/direction"

CONF_API_KEY = "api_key"
CONF_HOME_LONGITUDE = "home_longitude"
CONF_HOME_LATITUDE = "home_latitude"
CONF_DEVICE_TRACKER_ENTITY_ID = "device_tracker_entity_id"
CONF_UPDATE_INTERVAL = "update_interval"
CONF_MODE_OF_TRANSPORTATION = "mode_of_transportation"

CONF_DEFAULT_UPDATE_INTERVAL = 5
CONF_DEFAULT_MODE_OF_TRANSPORTATION = 1

CONF_MODE_ROUTE_KEY = "route"
CONF_MODE_DESC_KEY = "desc"
CONF_TRANSPORTATION_MODES = {
    1: {CONF_MODE_ROUTE_KEY: "walking", CONF_MODE_DESC_KEY: "步行"},
    2: {CONF_MODE_ROUTE_KEY: "transit/integrated", CONF_MODE_DESC_KEY: "公交/地铁"},
    3: {CONF_MODE_ROUTE_KEY: "driving", CONF_MODE_DESC_KEY: "驾车"},
    4: {CONF_MODE_ROUTE_KEY: "bicycling", CONF_MODE_DESC_KEY: "骑行"}
}
