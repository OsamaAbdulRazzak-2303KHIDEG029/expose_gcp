import logging

import requests  # type: ignore

logger = logging.getLogger(__name__)


def extract_data_from_api(api_url: str) -> dict:
    """
    Extracts data from an API endpoint.

    Args:
        api_url (str): The URL of the API endpoint.

    Returns:
        dict: The extracted data in JSON format.

    Raises:
        requests.HTTPError: If the API request fails with a non-200 status code.
    """
    response = requests.get(api_url)
    if response.status_code != 200:
        logger.error(f"Failed to fetch data from {api_url}")
        response.raise_for_status()
    return response.json()


def extract_all_data(api_urls: dict) -> dict:
    """
    Extracts data from multiple API endpoints.

    Args:
        api_urls (dict): A dictionary mapping keys to API URLs.

    Returns:
        dict: A dictionary mapping keys to the extracted data from each API endpoint.
    """
    data = {}
    for key, url in api_urls.items():
        data[key] = extract_data_from_api(url)
    return data
