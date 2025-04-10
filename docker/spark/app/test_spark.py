from pyspark.sql import SparkSession

# Spark 세션 생성
spark = SparkSession.builder \
    .appName("TestSparkJob") \
    .getOrCreate()

# 의도적으로 에러 발생시키기
try:
    # 존재하지 않는 Kafka 토픽에서 데이터 읽기 시도
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:9092") \
        .option("subscribe", "non_existent_topic") \
        .load()
    
    # 스트림 쿼리 시작
    query = df.writeStream \
        .format("console") \
        .start()
    
    query.awaitTermination()

except Exception as e:
    print(f"의도된 에러 발생: {str(e)}")
    
finally:
    spark.stop() 