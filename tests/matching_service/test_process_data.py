import unittest
from unittest import mock

import redis  # type: ignore
from redis.exceptions import RedisError

from src.matching_service.process_data import process_councillors_ratings


class TestProcessCouncillorsRatings(unittest.TestCase):
    def setUp(self):
        """Set up the test case."""
        # Create a mock Redis client
        self.redis_client = mock.Mock(spec=redis.Redis)
        self.specialization = "test_specialization"
        self.redis_key = f"specialization:{self.specialization}"

    def test_process_councillors_ratings(self):
        """Test the process_councillors_ratings function when Redis key exists."""
        # Mock the Redis response
        self.redis_client.exists.return_value = True
        self.redis_client.get.return_value = (
            '[{"id": "1", "average_rating": 4.5}, {"id": "2", "average_rating": 3.8}]'
        )

        result = process_councillors_ratings(self.redis_client, self.specialization)

        expected_result = [
            {"counselor_id": "1", "rating": 4.5},
            {"counselor_id": "2", "rating": 3.8},
        ]

        self.assertEqual(result, expected_result)

    def test_process_councillors_ratings_key_not_found(self):
        """Test the process_councillors_ratings function when Redis key is not found."""
        # Mock the Redis client's 'exists' method to return False
        self.redis_client.exists.return_value = False

        # Call the function under test and assert that it raises a KeyError
        with self.assertRaises(KeyError):
            process_councillors_ratings(self.redis_client, self.specialization)

        # Assert that the Redis client method was called with the correct argument
        self.redis_client.exists.assert_called_once_with(self.redis_key)

    def test_process_councillors_ratings_redis_error(self):
        """Test the process_councillors_ratings function when Redis connection error occurs."""
        # Mock the Redis client's 'exists' method to raise a RedisError
        self.redis_client.exists.side_effect = RedisError("Redis connection error")

        # Call the function under test and assert that it raises a RedisError
        with self.assertRaises(RedisError):
            process_councillors_ratings(self.redis_client, self.specialization)

        # Assert that the Redis client method was called with the correct argument
        self.redis_client.exists.assert_called_once_with(self.redis_key)

    def test_process_councillors_ratings_sorted_order(self):
        """Test sorting counselors in descending order of average ratings."""
        # Mock the Redis response
        redis_response = '[{"id": "1", "average_rating": 4.5}, \
        {"id": "2", "average_rating": 3.8}, {"id": "3", "average_rating": 4.2}]'

        self.redis_client.exists.return_value = True
        self.redis_client.get.return_value = redis_response

        # Call the function under test
        result = process_councillors_ratings(self.redis_client, self.specialization)

        # Expected result with counselor IDs sorted in descending order of average ratings
        expected_result = [
            {"counselor_id": "1", "rating": 4.5},
            {"counselor_id": "3", "rating": 4.2},
            {"counselor_id": "2", "rating": 3.8},
        ]

        # Assert that the result matches the expected result
        self.assertEqual(result, expected_result)

    def test_process_councillors_ratings_empty_ratings(self):
        """Test the process_councillors_ratings function when the ratings are empty."""
        # Mock the Redis response
        redis_response = "[]"
        self.redis_client.exists.return_value = True
        self.redis_client.get.return_value = redis_response

        # Call the function under test
        result = process_councillors_ratings(self.redis_client, self.specialization)

        # Expected result should be an empty list
        expected_result = []

        # Assert that the result matches the expected result
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
