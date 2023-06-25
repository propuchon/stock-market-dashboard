from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="dag_bash_operator_v2.4",
    description="Our first dag by using Bash Operator.",
    start_date=datetime(2023, 1, 1),
    schedule_interval="0 8 * * *",
) as dag:
    task1 = BashOperator(
        task_id="first_task_with_bash",
        bash_command="echo hello word, this is first task.",
    )
    task2 = BashOperator(
        task_id="second_task_with_bash",
        bash_command="echo hello world, this is second task will be running after first task.",
    )
    task3 = BashOperator(
        task_id="third_task_with_bash",
        bash_command="echo hello word, this is third task will be running after first task.",
    )
    task4 = BashOperator(
        task_id="fourth_task_with_bash",
        bash_command="echo hello word, this is third task will be running after third task.",
    )

    # Task Dependency method 1
    # task1.set_downstream(task2)
    # task1.set_downstream(task3)
    # task3.set_downstream(task4)

    # Task Dependency method 2
    # task1 >> task2
    # task1 >> task3 >> task4

    # Task Dependency method 3
    # task1 >> [task2, task3] >> task4
    # P.S. the sequence is not the same method 1, 2 it should write like this
    task1 >> [task2, task3]
    task3 >> task4
