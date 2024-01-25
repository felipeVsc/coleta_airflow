from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from cities.rio import rio
from cities.sao_paulo import sao_paulo
from cities.curitiba import curitiba
from cities.df import df


with DAG("cities_coleta_parquet",
    start_date=datetime(2024, 1, 9),
    schedule_interval=timedelta(minutes=1),
    # schedule=timedelta(minutes=1),
    catchup=False,
    default_args={
        "email": ["datasetpibic@gmail.com"],
        "email_on_failure": True}
) as dag_novo:
    
    rio_task = PythonOperator(
    	task_id= "rio",
    	python_callable=rio,
        trigger_rule="all_done"
    )

    sp_task = PythonOperator(
    	task_id= "saopaulo",
    	python_callable=sao_paulo,
        trigger_rule="all_done"
    )

    cwb_task = PythonOperator(
            task_id= "cwb",
            python_callable=curitiba,
            trigger_rule="all_done"
        )

    df_task = PythonOperator(
            task_id= "df",
            python_callable=df,
            trigger_rule="all_done"
        )

    rio_task >> sp_task >> cwb_task >> df_task