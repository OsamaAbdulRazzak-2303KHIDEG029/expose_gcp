from unittest.mock import Mock, patch

import pytest
from requests import Timeout

from src.etl_service.extract_utils import extract_data_from_api

API_URL_RATING = "https://xloop-dummy.herokuapp.com/rating"
API_URL_APPOINTMENT = "https://xloop-dummy.herokuapp.com/appointment"
API_URL_COUNCILLOR = "https://xloop-dummy.herokuapp.com/councillor"
API_URL_PATIENT_COUNCILLOR = "https://xloop-dummy.herokuapp.com/patient_councillor"


def test_extract_data_from_api_successful_request():
    """
    Test the extraction of data from an API when the request is successful.

    This test ensures that the 'extract_data_from_api' function correctly retrieves data from the API
    and returns the expected data when the API request is successful (status code 200).

    The test uses the 'patch' function from the 'unittest.mock' module to mock the 'requests.get' method
    and simulate a successful API response with the expected data.

    The expected behavior is that the 'extract_data_from_api' function should return the expected data
    and make a single call to 'requests.get' with the specified API URL.

    Raises:
        AssertionError: If the result of 'extract_data_from_api' is not equal to the expected data,
            or if 'requests.get' was not called with the expected API URL.

    """
    expected_data = {"key": "value"}

    with patch("src.etl_service.extract_utils.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_data
        mock_get.return_value = mock_response

        result = extract_data_from_api(API_URL_RATING)

        assert result == expected_data
        mock_get.assert_called_once_with(API_URL_RATING)


def test_extract_data_from_api_network_error():
    """
    Test the behavior of extract_data_from_api() when a network error occurs during the API request.

    It patches the 'requests.get' method using 'mock_get' and sets the side effect to raise a ConnectionError.
    Then, it expects extract_data_from_api() to raise a ConnectionError.

    Finally, it asserts that 'requests.get' was called once with the correct API URL.
    """
    with patch("src.etl_service.extract_utils.requests.get") as mock_get:
        mock_get.side_effect = ConnectionError

        with pytest.raises(ConnectionError):
            extract_data_from_api(API_URL_RATING)

        mock_get.assert_called_once_with(API_URL_RATING)


def test_extract_data_from_api_invalid_json_response():
    """
    Test case to verify the behavior of extract_data_from_api() function when an invalid JSON response is received.

    It mocks the requests.get() function to simulate a successful API response with a status code of 200,
    but causes the json() method of the response object to raise a ValueError.

    The test expects the ValueError to be raised when calling extract_data_from_api() and checks if the
    requests.get() function was called with the correct API URL.

    Note: This test assumes the presence of the necessary imports and test framework setup.

    """
    with patch("src.etl_service.extract_utils.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError
        mock_get.return_value = mock_response

        with pytest.raises(ValueError):
            extract_data_from_api(API_URL_RATING)

        mock_get.assert_called_once_with(API_URL_RATING)


def test_extract_data_from_api_empty_response():
    """
    Test case to check if extract_data_from_api returns None when the API response is empty.

    This test uses the unittest.mock.patch decorator to temporarily replace the 'requests.get'
    function with a mock object. The mock object is configured to simulate a 200 status code
    response with an empty JSON body.

    The test asserts that the result of the 'extract_data_from_api' function is None and that
    'requests.get' was called once with the correct API URL.

    This test case ensures that the function correctly handles an empty API response and
    returns None in such cases.
    """
    with patch("src.etl_service.extract_utils.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = None
        mock_get.return_value = mock_response

        result = extract_data_from_api(API_URL_RATING)

        assert result is None
        mock_get.assert_called_once_with(API_URL_RATING)


def test_extract_data_from_api_timeout_error():
    """
    Test case for handling a Timeout error during API extraction.

    This test case mocks the 'requests.get' function to raise a Timeout error when called with the specified API URL.
    It then asserts that the 'extract_data_from_api' function raises a Timeout exception.
    Additionally, it verifies that the 'requests.get' function was called exactly once with the correct API URL.

    Raises:
        Timeout: If the 'extract_data_from_api' function does not raise a Timeout exception.

    """
    with patch("src.etl_service.extract_utils.requests.get") as mock_get:
        mock_get.side_effect = Timeout

        with pytest.raises(Timeout):
            extract_data_from_api(API_URL_RATING)

        mock_get.assert_called_once_with(API_URL_RATING)
