from datetime import datetime, timedelta

from airflow.decorators import dag, task

default_args = {
    "owner": "me",
    "retries": 1,  #  the number of retries that should be performed before failing the task
    "retry_delay": timedelta(minutes=2),  # delay between retries
}


@dag(
    default_args=default_args,
    dag_id="dag_task_flow_api_v1.5",
    description="Write as task flows decorators is reduce the line more.",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@daily",
    catchup=False,  # if 'True' run backwards from the start date.
)
def greeting_etl():
    @task(multiple_outputs=True)
    def get_name():
        return {"firstname": "Jerry", "lastname": "Frimen"}

    @task()
    def get_age():
        return 19

    @task()
    def greet(firstname, lastname, age):
        print(f"My name is {firstname} {lastname} and I am {age} years old.")

    name = get_name()
    age = get_age()
    greet(firstname=name["firstname"], lastname=name["lastname"], age=age)


greet_age = greeting_etl()
