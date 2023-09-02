"""
Validation functions for to_home_distance.
"""
import re
from .const import (
    CONF_DEVICE_TRACKER,
    CONF_VALIDATE_API_KEY_URL,
    CONF_INFOCODE_KEY,
    CONF_API_KEY_NOT_VALIDATED
)


async def validate_api_key(session, api_key):
    """
    Validate the API key.
    """
    try:
        api_url = f"{CONF_VALIDATE_API_KEY_URL}{api_key}"
        async with session.get(api_url) as resp:
            json_data = await resp.json()
            if json_data[CONF_INFOCODE_KEY] == CONF_API_KEY_NOT_VALIDATED:
                raise ValueError
    except Exception as exc:
        raise ValueError from exc


def validate_longitude(longitude_string):
    """
    Validate the longitude.
    """
    return _validate_coordinate(longitude_string, 'lng')


def validate_latitude(latitude_string):
    """
    Validate the latitude.
    """
    return _validate_coordinate(latitude_string, 'lat')


def validate_domain(entity_id):
    """
    Validate the domain.
    """
    domain = entity_id.split('.')[0]
    return domain == CONF_DEVICE_TRACKER


def validate_mode(mode):
    """
    Validate the mode.
    """
    return mode in [1, 2, 3, 4]


def validate_update_interval(interval):
    """
    Validate the update interval.
    """
    return interval > 0


def _validate_coordinate(coordinate_string, mode):
    if mode not in ('lng', 'lat'):
        raise ValueError("Invalid mode. Mode must be 'lng' or 'lat'.")

    patterns = {
        'lng': r"^\s*([-+]?\d{1,3}(?:\.\d{1,6})?)\s*$",
        'lat': r"^\s*([-+]?\d{1,2}(?:\.\d{1,6})?)\s*$",
    }

    pattern = re.compile(patterns[mode])
    match = pattern.match(coordinate_string)
    if match:
        value = float(match.group(1))
        if -180 <= value <= 180 if mode == 'lng' else -90 <= value <= 90:
            return True
    return False
