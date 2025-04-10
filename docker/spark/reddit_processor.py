from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, lit, udf
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType, FloatType
import json
from datetime import datetime
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import numpy as np

# 모델 로드
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
sentiment_analyzer = pipeline("sentiment-analysis", model="finiteautomata/bertweet-base-sentiment-analysis")

def get_embedding(text):
    """텍스트를 임베딩 벡터로 변환합니다."""
    if not text:
        return [0.0] * 384
    return model.encode(text).tolist()

def analyze_sentiment(text):
    """텍스트의 감성을 분석합니다."""
    if not text:
        return 0.0, "neutral"
    result = sentiment_analyzer(text)[0]
    score = result['score']
    if result['label'] == 'NEU':
        return score, "neutral"
    elif result['label'] == 'POS':
        return score, "positive"
    else:
        return -score, "negative"

def main():
    # Spark 세션 생성
    spark = SparkSession.builder \
        .appName("RedditDataProcessor") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.postgresql:postgresql:42.7.1") \
        .getOrCreate()

    # 스키마 정의
    schema = StructType([
        StructField("submission_id", StringType()),
        StructField("subreddit", StringType()),
        StructField("title", StringType()),
        StructField("selftext", StringType()),
        StructField("author", StringType()),
        StructField("created_utc", TimestampType()),
        StructField("score", IntegerType()),
        StructField("num_comments", IntegerType()),
        StructField("url", StringType()),
        StructField("permalink", StringType()),
        StructField("collected_at", TimestampType())
    ])

    # Kafka에서 데이터 읽기
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:29092") \
        .option("subscribe", "reddit_raw_data") \
        .option("startingOffsets", "latest") \
        .load()

    # JSON 파싱
    parsed_df = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

    # 임베딩과 감성 분석을 위한 UDF 등록
    get_embedding_udf = udf(get_embedding, ArrayType(FloatType()))
    analyze_sentiment_udf = udf(analyze_sentiment, StructType([
        StructField("score", FloatType()),
        StructField("label", StringType())
    ]))

    # 데이터 처리
    processed_df = parsed_df \
        .withColumn("title_embedding", get_embedding_udf(col("title"))) \
        .withColumn("selftext_embedding", get_embedding_udf(col("selftext"))) \
        .withColumn("sentiment", analyze_sentiment_udf(col("selftext"))) \
        .select(
            "submission_id",
            "title_embedding",
            "selftext_embedding",
            "sentiment.score",
            "sentiment.label",
            lit(datetime.now()).alias("analyzed_at")
        )

    # PostgreSQL에 저장
    def write_to_postgres(batch_df, batch_id):
        batch_df.write \
            .format("jdbc") \
            .option("url", "jdbc:postgresql://postgres:5432/coin_community") \
            .option("dbtable", "reddit_analysis_submissions") \
            .option("user", "postgres") \
            .option("password", "postgres") \
            .option("driver", "org.postgresql.Driver") \
            .mode("append") \
            .save()

    # 스트리밍 시작
    query = processed_df.writeStream \
        .foreachBatch(write_to_postgres) \
        .outputMode("append") \
        .start()

    query.awaitTermination()

if __name__ == "__main__":
    main() 