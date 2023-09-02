"""
utils.py
"""
from .validation import (
    validate_longitude,
    validate_latitude
)


def format_distance(distance):
    """
    Format distance.
    """
    if distance >= 1000:
        return f"{round(distance / 1000, 2)} km"
    return f"{round(distance, 0)} m"


def format_duration(duration):
    """
    Format duration.
    """
    hours, remainder = divmod(duration, 3600)
    minutes, _ = divmod(remainder, 60)

    if hours > 0:
        return f"{hours} 小时 {minutes} 分钟"
    return f"{minutes} 分钟"


def format_and_validate_coordinates(longitude, latitude):
    """
    Format and validate coordinates.
    """
    lng = convert_and_round(longitude)
    lat = convert_and_round(latitude)
    if not is_valid_location(lng, lat):
        return None

    return combine_longitude_latitude(lng, lat)


def combine_longitude_latitude(longitude, latitude):
    """
    Combine longitude and latitude.
    """
    return f"{longitude},{latitude}"


def convert_and_round(value):
    """
    Convert and round.
    """
    return str(round(float(value), 6))


def is_valid_location(longitude, latitude):
    """
    Check if the location is valid.
    """
    return validate_longitude(longitude) and validate_latitude(latitude)
