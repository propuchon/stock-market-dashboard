from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    "owner": "me",
    "retries": 1,  #  the number of retries that should be performed before failing the task
    "retry_delay": timedelta(minutes=2),  # delay between retries
}


def greet(last_name: str, ti):
    first_name = ti.xcom_pull(task_ids="_get_firstname")
    return print(f"Hello! My name is {first_name} {last_name}")


def greet_v2(ti):
    first_name = ti.xcom_pull(task_ids="_get_fullname", key="first_name")
    last_name = ti.xcom_pull(task_ids="_get_fullname", key="last_name")
    age = ti.xcom_pull(task_ids="_get_age", key="age")
    return print(
        f"Hello! My name is {first_name} {last_name}, and I'm {age} year's old."
    )


def _get_firstname():
    return "Edward"


def _get_fullname(ti):
    ti.xcom_push(key="first_name", value="Thomas")
    ti.xcom_push(key="last_name", value="Edison")


def _get_age(ti):
    ti.xcom_push(key="age", value="50")


with DAG(
    default_args=default_args,
    dag_id="dag_python_operator_v2.5",
    description="Our first dag by using Python Operator.",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@daily",
) as dag:
    task1 = PythonOperator(
        task_id="greeting_v1", python_callable=greet, op_kwargs={"last_name": "Snowden"}
    )
    task2 = PythonOperator(
        task_id="_get_firstname",
        python_callable=_get_firstname,
    )
    task3 = PythonOperator(task_id="_get_full_name", python_callable=_get_fullname)
    task4 = PythonOperator(task_id="_get_age", python_callable=_get_age)
    task5 = PythonOperator(task_id="greeting_v2", python_callable=greet_v2)

    task2 >> task1
    [task4, task3] >> task5
