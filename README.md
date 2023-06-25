<h1> Stock Market piepline </h1>

Educational purpose to pipeline the data

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Objective](#objective)
- [Initialize Airflow Project](#initialize-airflow-project)
- [Reference](#reference)

## Objective
- To study the pipeline to get the data via API.
- To set schedule to collect the data in our database.
- Send the dataset to Google Sheets in order to visualize it on Looker Studio.
- Make developer more understandable to use a Docker.

## Initialize Airflow Project

- **Fetching `docker-compose.yaml`**
    ```
    curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.6.1/docker-compose.yaml'
    ```
- **Initialize Environment**
    ```ssh
    mkdir -p ./dags ./logs ./plugins ./config
    echo -e "AIRFLOW_UID=$(id -u)" > .env
    ```
- **Initialize the database**
    ```
    docker compose up airflow-init
    ```
- **Running Airflow**
    ```ssh
    docker compose up
    ```
1. Edit the image in `docker-compose.yaml` to setup our environment.
2. Use a command `docker build -t <image-name>:<tag> .` to create a image.
3. write a job in `dags` folders.

---


## Reference
- [Running Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#special-case-adding-dependencies-via-requirements-txt-file)
- [Docker command](https://codenotary.com/blog/extremely-useful-docker-commands#:~:text=docker%20stop%20stops%20one%20or,q)