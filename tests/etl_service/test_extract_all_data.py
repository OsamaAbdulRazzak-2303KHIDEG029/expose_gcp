from unittest.mock import Mock, patch

import pytest
import requests

from src.etl_service.extract_utils import extract_all_data

API_BASE_URL = "https://xloop-dummy.herokuapp.com"
API_ENDPOINTS = ["rating", "appointment", "councillor", "patient_councillor"]
API_URLS = {key: API_BASE_URL + "/" + key for key in API_ENDPOINTS}


def test_extract_all_data_integration():
    # Test the extract_all_data function with actual API calls
    data = extract_all_data(API_URLS)
    assert isinstance(data, dict)
    assert len(data) == len(API_URLS)
    for key in API_URLS:
        assert key in data


@pytest.mark.parametrize("api_url", API_URLS.values())
def test_extract_all_data_successful_requests(api_url):
    expected_data = {"key": "value"}
    with patch("src.etl_service.extract_utils.requests.get") as mock_requests_get:
        mock_response = Mock()
        mock_response.json.return_value = expected_data
        mock_requests_get.return_value = mock_response
        result = extract_all_data({api_url: api_url})
    assert result == {api_url: expected_data}


def test_extract_all_data_error_handling():
    # api_urls = API_URLS()
    with patch(
        "src.etl_service.extract_utils.extract_data_from_api"
    ) as mock_extract_data:
        mock_extract_data.side_effect = requests.exceptions.RequestException(
            "Failed to retrieve data"
        )
        with pytest.raises(requests.exceptions.RequestException) as exc_info:
            extract_all_data(API_URLS)
        expected_error_message = "Failed to retrieve data"
        assert expected_error_message in str(exc_info.value)


def test_extract_all_data_with_mock():
    with patch(
        "src.etl_service.extract_utils.extract_data_from_api"
    ) as mock_extract_data_from_api:
        mock_data = {"mock_data": "test"}
        mock_extract_data_from_api.return_value = mock_data
        data = extract_all_data(API_URLS)
        expected_data = {key: mock_data for key in API_URLS}
        assert data == expected_data
        assert mock_extract_data_from_api.call_count == len(API_URLS)
