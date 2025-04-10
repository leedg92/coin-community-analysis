"""
테스트용 데이터 파이프라인 DAG
- PostgreSQL에 테스트 데이터 입력
- Kafka를 통한 메시지 전송
- Spark를 이용한 간단한 데이터 처리
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from kafka import KafkaProducer
import json
import logging

# DAG 기본 설정
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 4, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG 정의
dag = DAG(
    'test_pipeline',
    default_args=default_args,
    description='테스트용 데이터 파이프라인',
    # schedule_interval=timedelta(minutes=5),  # 5분마다 실행 (주석 처리)
    schedule_interval=None,  # 수동 실행만 가능하도록 설정
    catchup=False
)

# PostgreSQL에 데이터 입력하는 SQL
insert_java_message = PostgresOperator(
    task_id='insert_java_message',
    postgres_conn_id='postgres_default',  # Airflow UI에서 설정 필요
    sql="""
    INSERT INTO test_messages (message, source)
    VALUES ('Hello, Java!', 'java');
    """,
    dag=dag
)

insert_node_message = PostgresOperator(
    task_id='insert_node_message',
    postgres_conn_id='postgres_default',  # Airflow UI에서 설정 필요
    sql="""
    INSERT INTO test_messages (message, source)
    VALUES ('Hello, Node!', 'node');
    """,
    dag=dag
)

# Kafka에 메시지 전송하는 함수
def send_to_kafka(**context):
    """
    Kafka에 테스트 메시지를 전송하는 함수
    - producer: KafkaProducer 인스턴스 생성
    - topic: 'test_messages' 토픽에 메시지 전송
    - message: JSON 형식으로 메시지 전송
    """
    try:
        producer = KafkaProducer(
            bootstrap_servers=['kafka:9092'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        
        # 테스트 메시지 전송
        messages = [
            {'source': 'java', 'message': 'Hello, Java!'},
            {'source': 'node', 'message': 'Hello, Node!'}
        ]
        
        for msg in messages:
            producer.send('test_messages', value=msg)
            logging.info(f"Sent message to Kafka: {msg}")
            
        producer.flush()
        producer.close()
        
    except Exception as e:
        logging.error(f"Error sending message to Kafka: {e}")
        raise

# Kafka 전송 태스크
kafka_task = PythonOperator(
    task_id='send_to_kafka',
    python_callable=send_to_kafka,
    dag=dag
)

# Spark 작업 정의 (테스트용 Word Count)
spark_task = SparkSubmitOperator(
    task_id='spark_test_job',
    application='/opt/airflow/dags/spark_test_job.py',  # Spark 작업 파일 경로
    conn_id='spark_default',  # Airflow UI에서 설정 필요
    conf={
        'spark.master': 'spark://spark-master:7077',
    },
    dag=dag
)

# 태스크 순서 정의
insert_java_message >> insert_node_message >> kafka_task >> spark_task 