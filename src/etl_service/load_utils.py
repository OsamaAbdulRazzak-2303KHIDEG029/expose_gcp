import json
import logging
from typing import Any, Dict, List

import redis  # type: ignore


def load_data_to_redis(
    redis_client: redis.Redis,
    specialization: str,
    avg_ratings_list: List[Dict[str, Any]],
) -> bool:
    """
    Load average ratings data to Redis.

    Args:
        redis_client (redis.Redis): Redis client object.
        specialization (str): Specialization name.
        avg_ratings_list (List[Dict[str, Any]]): List of dictionaries containing average ratings data.

    Raises:k
        TypeError: If redis_client is not a valid Redis client object.
        ValueError: If specialization is an empty string or avg_ratings_list is empty.

    Returns:
        bool: True if data is loaded successfully, False otherwise.
    """
    if not isinstance(redis_client, redis.Redis):
        raise TypeError("redis_client must be a valid Redis client object.")

    # Check if specialization is not empty
    if not specialization:
        raise ValueError("specialization cannot be an empty string.")

    # Check if avg_ratings_list is not empty
    if not avg_ratings_list:
        raise ValueError("avg_ratings_list cannot be empty.")

    # Set Redis key for average ratings

    # Store average ratings data in Redis hash
    loaded_successfully = True  # Initialize as True

    # Update loaded_successfully
    table_data = [
        {
            "id": row["id"],
            "specialization": row["specialization"],
            "average_rating": row["average_rating"],
        }
        for row in avg_ratings_list
        if row["specialization"] == specialization
    ]

    redis_table_key = f"specialization:{specialization}"
    result = redis_client.set(redis_table_key, json.dumps(table_data))
    loaded_successfully = loaded_successfully and result
    logging.info(f"Added data in Redis for specialization {specialization}")
    return loaded_successfully
