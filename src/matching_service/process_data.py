import json
import logging
from typing import Dict, List

import redis  # type: ignore
from redis.exceptions import RedisError  # type: ignore

logger = logging.getLogger(__name__)


def process_councillors_ratings(
    redis_client: redis.Redis, specialization: str
) -> List[Dict[str, object]]:
    """
    Retrieves counselor ratings based on the given specialization.

    Args:
        redis_client (redis.Redis): Redis client object.
        specialization (str): Specialization/category to retrieve ratings for.

    Returns:
        List[Dict[str, Union[str, float]]]: List of counselor ratings (counselor_id, rating).
        If the Redis key is not found or unavailable, raises a KeyError.
    """
    redis_key = f"specialization:{specialization}"

    try:
        if not redis_client.exists(redis_key):
            raise KeyError(f"Redis key not found or unavailable: {redis_key}")

        counselor_ratings_json = redis_client.get(redis_key)
        counselor_ratings_list = json.loads(counselor_ratings_json)

        ratings: Dict[str, float] = {}

        for row in counselor_ratings_list:
            counselor_id = str(row["id"])
            rating = float(row["average_rating"])
            ratings[counselor_id] = rating

        sorted_ratings = sorted(ratings.items(), key=lambda x: x[1], reverse=True)
        top_counselors = sorted_ratings[:10]

        result = [
            {"counselor_id": counselor_id, "rating": rating}
            for counselor_id, rating in top_counselors
        ]

        return result
    except RedisError as e:
        error_message = f"Error processing counselor ratings: {str(e)}"
        logger.exception(error_message)
        raise
