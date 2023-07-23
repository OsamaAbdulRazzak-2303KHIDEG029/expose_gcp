import logging
from typing import Any, Dict

import logging_config
import requests  # type: ignore
from decouple import config
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from process_data import process_councillors_ratings
from redis.exceptions import RedisError  # type: ignore
from redis_connector import get_redis_client

app = FastAPI()

# Connect to Redis
redis_host = config("REDIS_HOST")
redis_port = config("REDIS_PORT")
redis_client = get_redis_client(redis_host, redis_port)

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Call the function from the log_config module to configure the console handler
logging_config.configure_logging()


@app.exception_handler(HTTPException)
async def handle_http_exception(exc: HTTPException) -> JSONResponse:
    """
    Global exception handler for HTTPException.
    Returns a proper HTTP response with the corresponding status code and detail.
    """
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


def get_report_content(report_id: int) -> Dict[str, Any]:
    base_url = "https://xloop-dummy.herokuapp.com"
    url = f"{base_url}/report/{report_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred during the request: {e}")
        raise
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}")
        raise


@app.get("/top-councillors/{report_id}")
async def get_top_councillors(report_id: int) -> Dict[str, Any]:
    """
    Retrieves top councillors based on the given report ID.

    Args:
        report_id (int): ID of the report.

    Returns:
        Dict[str, Any]: Result of the councillor rating processing.
    """
    try:
        report_json: Dict[str, Any] = get_report_content(report_id)
        logger.info("Received report: %s", report_json)
        if (specialization := report_json.get("category")) is None:
            raise HTTPException(
                status_code=400, detail="Category is missing in the report."
            )
        result = process_councillors_ratings(redis_client, specialization)
        return {"result": result}  # Ensure the response is a dictionary

    except HTTPException as http_exc:
        logger.exception(f"Error processing the report: {str(http_exc)}")
        raise

    except RedisError as redis_exc:
        logger.exception(f"Error connecting to Redis: {str(redis_exc)}")
        raise HTTPException(
            status_code=500, detail="Error connecting to Redis."
        ) from redis_exc


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
