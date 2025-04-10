"""
테스트용 Spark 작업
- PostgreSQL에서 데이터 읽기
- 간단한 데이터 처리
- 결과를 다시 PostgreSQL에 저장
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count

def create_spark_session():
    """
    Spark 세션 생성
    - PostgreSQL JDBC 드라이버 설정 포함
    - 애플리케이션 이름 설정
    """
    return SparkSession.builder \
        .appName("TestSparkJob") \
        .config("spark.jars.packages", "org.postgresql:postgresql:42.2.18") \
        .getOrCreate()

def read_from_postgres(spark):
    """
    PostgreSQL에서 데이터 읽기
    - JDBC를 통해 test_messages 테이블 읽기
    - DataFrame으로 변환
    """
    return spark.read \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/coindb") \
        .option("dbtable", "test_messages") \
        .option("user", "postgres") \
        .option("password", "postgres") \
        .option("driver", "org.postgresql.Driver") \
        .load()

def process_data(df):
    """
    데이터 처리
    - source별 메시지 수 집계
    - 결과를 새로운 DataFrame으로 반환
    """
    return df.groupBy("source") \
        .agg(count("*").alias("message_count"))

def write_to_postgres(df, table_name):
    """
    처리된 데이터를 PostgreSQL에 저장
    - JDBC를 통해 결과 테이블에 저장
    - 기존 데이터 덮어쓰기 (mode="overwrite")
    """
    df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/coindb") \
        .option("dbtable", table_name) \
        .option("user", "postgres") \
        .option("password", "postgres") \
        .option("driver", "org.postgresql.Driver") \
        .mode("overwrite") \
        .save()

def main():
    """
    메인 실행 함수
    - Spark 세션 생성
    - 데이터 읽기
    - 데이터 처리
    - 결과 저장
    """
    try:
        # Spark 세션 생성
        spark = create_spark_session()
        
        # 데이터 읽기
        df = read_from_postgres(spark)
        
        # 데이터 처리
        result_df = process_data(df)
        
        # 결과 저장
        write_to_postgres(result_df, "message_counts")
        
    finally:
        # Spark 세션 종료
        spark.stop()

if __name__ == "__main__":
    main() 