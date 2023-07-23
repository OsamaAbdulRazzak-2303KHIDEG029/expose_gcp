import json
import logging
from typing import List, Tuple

from pyspark.sql import SparkSession
from pyspark.sql.functions import avg


def transform_data(
    spark: SparkSession,
    data: dict,
    rating_key: str,
    appointment_key: str,
    councillor_key: str,
    patient_councillor_key: str,
) -> Tuple[List[dict], List[str]]:
    """
    Transform data using Spark DataFrame operations.

    Args:
        spark (SparkSession): SparkSession object.
        data (dict): Dictionary containing data from different api endpoints.
        rating_key (str): Key to access the rating data in the `data` dictionary.
        appointment_key (str): Key to access the appointment data in the `data` dictionary.
        councillor_key (str): Key to access the councillor data in the `data` dictionary.
        patient_councillor_key (str): Key to access the patient-councillor data in the `data` dictionary.

    Returns:
        Tuple[List[dict], List[str]]: A tuple containing the average ratings list and distinct specializations.

    Raises:
        ValueError: If any required data field is missing or empty in the `data` dictionary.
    """

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    validate_data(data)  # Validate the input data

    # Read rating data
    logger.info("Reading rating data .")

    rating = spark.read.json(
        spark.sparkContext.parallelize([json.dumps(data[rating_key])])
    )

    # Read appointment data
    logger.info("Reading appointment data.")

    appointment = spark.read.json(
        spark.sparkContext.parallelize([json.dumps(data[appointment_key])])
    )

    # Read councillor data
    logger.info("Reading councillor data.")

    councillor = spark.read.json(
        spark.sparkContext.parallelize([json.dumps(data[councillor_key])])
    )

    # Read patient-councillor data
    logger.info("Reading patient-councillor data.")

    patient_councillor = spark.read.json(
        spark.sparkContext.parallelize([json.dumps(data[patient_councillor_key])])
    )

    # Perform necessary joins on the dataframes
    logger.info("Performing joins on the dataframes.")

    joined_df = (
        rating.join(appointment, rating["appointment_id"] == appointment["id"])
        .join(
            patient_councillor,
            patient_councillor["patient_id"] == appointment["patient_id"],
        )
        .join(councillor, councillor["id"] == patient_councillor["councillor_id"])
    )

    # Calculate average ratings grouped by councillor id and specialization
    logger.info("Calculating average ratings.")

    avg_ratings_df = joined_df.groupby(
        councillor["id"], councillor["specialization"]
    ).agg(avg(rating["value"]).alias("average_rating"))

    # Collect the average ratings as a list
    avg_ratings_list = avg_ratings_df.collect()

    # Extract the distinct specializations
    logger.info("Extracting distinct specializations.")

    specializations = (
        avg_ratings_df.select("specialization")
        .distinct()
        .rdd.flatMap(lambda x: x)
        .collect()
    )

    return avg_ratings_list, specializations


def validate_data(data: dict) -> None:
    required_fields = ["rating", "appointment", "councillor", "patient_councillor"]
    for field in required_fields:
        if field not in data or not data[field]:
            raise ValueError(f"Missing or empty data for field: {field}")
