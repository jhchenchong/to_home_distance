"""
Constants for the To Home Distance integration.
"""
DOMAIN = "to_home_distance"

CONF_API_URL = "https://restapi.amap.com/v3/direction"
CONF_VALIDATE_API_KEY_URL = "https://restapi.amap.com/v3/ip?key="

CONF_API_KEY = "api_key"
CONF_HOME_LONGITUDE = "home_longitude"
CONF_HOME_LATITUDE = "home_latitude"
CONF_DEVICE_TRACKER_ENTITY_ID = "device_tracker_entity_id"
CONF_UPDATE_INTERVAL = "update_interval"
CONF_MODE_OF_TRANSPORTATION = "mode_of_transportation"

CONF_DEFAULT_UPDATE_INTERVAL = 5
CONF_DEFAULT_MODE_OF_TRANSPORTATION = 1
CONF_REQUEST_TIMEOUT = 10

CONF_MODE_ROUTE_KEY = "route"
CONF_MODE_DESC_KEY = "desc"
CONF_TRANSPORTATION_MODES = {
    1: {CONF_MODE_ROUTE_KEY: "walking", CONF_MODE_DESC_KEY: "步行"},
    2: {CONF_MODE_ROUTE_KEY: "transit/integrated", CONF_MODE_DESC_KEY: "公交/地铁"},
    3: {CONF_MODE_ROUTE_KEY: "driving", CONF_MODE_DESC_KEY: "驾车"},
    4: {CONF_MODE_ROUTE_KEY: "bicycling", CONF_MODE_DESC_KEY: "骑行"}
}
CONF_DEVICE_TRACKER = "device_tracker"

CONF_DISTANCE_KEY = "distance"
CONF_DURATION_KEY = "duration"
CONF_STATUS_KEY = "status"
CONF_ROUTE_KEY = "route"
CONF_PATHS_KEY = "paths"
CONF_STATUS_SUCCESS = "1"
CONF_INFOCODE_KEY = "infocode"
CONF_API_KEY_NOT_VALIDATED = "10001"

CONF_LONGITUDE_KEY = "longitude"
CONF_LATITUDE_KEY = "latitude"
