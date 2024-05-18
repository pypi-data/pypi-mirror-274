import requests
from swarms.utils.loguru import logger


def get_coordinates(place: str, api_key: str) -> tuple:
    """
    Retrieves the longitude and latitude of a given city or place using the OpenCage Geocoding API.

    Args:
        place (str): The name of the city or place to retrieve coordinates for.
        api_key (str): Your OpenCage Geocoding API key.

    Returns:
        tuple: A tuple containing the latitude and longitude of the place.
               Returns (None, None) if the place could not be found or an error occurred.
    """
    base_url = "https://api.opencagedata.com/geocode/v1/json"

    params = {"q": place, "key": api_key, "limit": 1}

    try:
        logger.info(
            f"Attempting to retrieve coordinates for place: {place}"
        )
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()

        if data["results"]:
            latitude = data["results"][0]["geometry"]["lat"]
            longitude = data["results"][0]["geometry"]["lng"]
            logger.info(
                f"Retrieved coordinates: (Latitude: {latitude},"
                f" Longitude: {longitude})"
            )
            return latitude, longitude
        else:
            logger.warning(f"No results found for place: {place}")
            return None, None

    except requests.RequestException as e:
        logger.error(
            "RequestException: Failed to retrieve data for place:"
            f" {place}. Error: {e}"
        )
        return None, None

    except KeyError as e:
        logger.error(
            "KeyError: Unexpected response format for place:"
            f" {place}. Error: {e}"
        )
        return None, None


# # Example usage:
# if __name__ == "__main__":
#     # Replace 'YOUR_API_KEY' with your actual OpenCage API key
#     place_name = "San Francisco"
#     api_key = "YOUR_API_KEY"
#     coords = get_coordinates(place_name, api_key)
#     print(f"Coordinates of {place_name}: {coords}")
