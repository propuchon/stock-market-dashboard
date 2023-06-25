FROM apache/airflow:latest-python3.9

USER airflow

COPY requirements.txt .

RUN pip install -r requirements.txt