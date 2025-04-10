from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'reddit_data_pipeline',
    default_args=default_args,
    description='Reddit 데이터 수집 및 처리 파이프라인',
    schedule_interval='*/30 * * * * *',  # 30초마다 실행
    catchup=False
)

# 데이터 수집 Spark Job
collect_data = BashOperator(
    task_id='collect_reddit_data',
    bash_command='spark-submit --master spark://spark-master:7077 /opt/spark/reddit_collector.py',
    dag=dag
)

# 데이터 처리 Spark Job
process_data = BashOperator(
    task_id='process_reddit_data',
    bash_command='spark-submit --master spark://spark-master:7077 /opt/spark/reddit_processor.py',
    dag=dag
)

# 작업 순서 정의
collect_data >> process_data 