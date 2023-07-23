# Capstone_Project-Group-C
# Problem Statement

Patient to provider matching. Based on a form a patient would fill in when starting to search for a practitioner, we'd suggest them providers specializing in the issue they're struggling with, ones that are successful and (maybe?) offer appointments in their area.

Project Overview

In this project, we aim to solve the problem of patient-to-provider matching by suggesting practitioners who specialize in specific issues and are successful in their practice.

The project consists of two main services:

ETL Service:

* The ETL (Extract, Transform, Load) service is responsible for extracting data from API endpoints.
* It performs necessary transformations on the data.
* The transformed data is then loaded into a Redis database.
* The ETL service is Dockerized for easy deployment and scalability.
* It includes a cron job that automatically runs at certain times to keep the data up to date.

Matching Service:

* The Matching service retrieves data from the Redis database.
* It performs matching algorithms to suggest providers based on the patient's form input.
* The matched data is then posted to an API.
* The Matching service is also Dockerized for efficient deployment.


## Installation and Setup
To set up the project locally, follow these steps:

1. Clone the repository:

```bash
   git clone https://github.com/MuzammilMeh/2303-capstone-group-C.git

```
2. Navigate to the project directory:
```bash
    cd Capstone_Project-Group-C
```
3. Build the Docker images:
```bash
    make build
```
4. Start the services:

```bash
    make up
```

This command will start the ETL Service and Matching Service containers defined in the docker-compose.yml file.

4. Monitor the logs:
```bash
    make logs
```

5. Use this command to view the logs of the running containers. You can check for any errors or monitor the progress of the services.


6. Access the services:

The services should now be up and running. You can access them using the appropriate endpoints or ports specified in the configuration.








## Environment Variables

To run this project, you will need to add the following environment variables to your .env file in both services.

`REDIS_HOST` The hostname for the Redis database. 'redis'

`REDIS_PORT` The port number for the Redis database.
'6379'




## Makefile Usage
The project includes a Makefile with several targets to simplify common tasks. Here are some useful commands:

* make build: Build the Docker images.
* make up: Start the services.
* make down: Stop the services and remove containers.
* make restart: Restart the services.
* make etl: Run the ETL script.
* make logs: Monitor the logs of the running containers.
* make shell: Open a shell in the ETL service container.
* make clean: Stop the services, remove containers, and clean up associated resources.

## Tech Stack

The technologies used in this project are:

- **Pyspark**: A powerful data processing framework for Python.
- **Redis**: An in-memory data structure store used as the database for efficient data storage and retrieval.
- **Python**: The programming language used for developing the ETL Service, Matching Service, and other components.
- **Docker**: A containerization platform used for packaging the services and their dependencies.
- **FastAPI**: A modern web framework for building APIs with Python, used for creating the API endpoints in the Matching Service.




## Authors

- [@MuzammilMehood](https://github.com/MuzammilMeh)
- [@Ali-Nasir-Dawood](https://github.com/Ali-Nasir-Dawood)
- [@MaazJavaidSiddique2303004KHIDEG](https://github.com/MaazJavaidSiddique2303004KHIDEG)
- [@OsamaAbdulRazzak](https://github.com/OsamaAbdulRazzak-2303KHIDEG029)
- [@faizagulzarahmed2303](https://github.com/faizagulzarahmed2303-001-KHI-DEG)


## License

[MIT](https://choosealicense.com/licenses/mit/)
