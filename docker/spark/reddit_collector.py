from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, lit
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType
import requests
from requests.auth import HTTPBasicAuth
import json
import time
from datetime import datetime
import os

# Config 파일 로드
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'reddit_config.json')
    with open(config_path, 'r') as f:
        return json.load(f)

# Config 설정
config = load_config()
CLIENT_ID = config['client_id']
CLIENT_SECRET = config['client_secret']
USERNAME = config['username']
PASSWORD = config['password']
USER_AGENT = config['user_agent']
SUBREDDITS = config['subreddits']

def get_reddit_token():
    """레딧 API 토큰을 가져옵니다."""
    auth = HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    data = {
        'grant_type': 'password',
        'username': USERNAME,
        'password': PASSWORD
    }
    headers = {'User-Agent': USER_AGENT}
    
    response = requests.post(
        'https://www.reddit.com/api/v1/access_token',
        auth=auth,
        data=data,
        headers=headers
    )
    
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception(f"Failed to get token: {response.text}")

def fetch_subreddit_posts(subreddit, token):
    """특정 서브레딧의 최신 게시물을 가져옵니다."""
    headers = {
        'Authorization': f'Bearer {token}',
        'User-Agent': USER_AGENT
    }
    
    response = requests.get(
        f'https://oauth.reddit.com/r/{subreddit}/new',
        headers=headers,
        params={'limit': 100}
    )
    
    if response.status_code == 200:
        return response.json()['data']['children']
    else:
        print(f"Error fetching posts from {subreddit}: {response.text}")
        return []

def fetch_post_comments(subreddit, post_id, token):
    """게시물의 댓글을 가져옵니다."""
    headers = {
        'Authorization': f'Bearer {token}',
        'User-Agent': USER_AGENT
    }
    
    response = requests.get(
        f'https://oauth.reddit.com/r/{subreddit}/comments/{post_id}',
        headers=headers,
        params={'limit': 100, 'depth': 1}  # depth=1로 설정하여 직접 댓글만 가져옴
    )
    
    if response.status_code == 200:
        return response.json()[1]['data']['children']  # 두 번째 항목이 댓글 데이터
    else:
        print(f"Error fetching comments for post {post_id}: {response.text}")
        return []

def main():
    # Spark 세션 생성
    spark = SparkSession.builder \
        .appName("RedditDataCollector") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
        .getOrCreate()

    # 게시물 스키마 정의
    post_schema = StructType([
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

    # 댓글 스키마 정의
    comment_schema = StructType([
        StructField("comment_id", StringType()),
        StructField("submission_id", StringType()),
        StructField("parent_id", StringType()),
        StructField("author", StringType()),
        StructField("body", StringType()),
        StructField("created_utc", TimestampType()),
        StructField("score", IntegerType()),
        StructField("collected_at", TimestampType())
    ])

    while True:
        try:
            # 토큰 가져오기
            token = get_reddit_token()
            
            for subreddit in SUBREDDITS:
                # 게시물 가져오기
                posts = fetch_subreddit_posts(subreddit, token)
                
                # 게시물 데이터 변환
                post_data = []
                for post in posts:
                    post_data.append({
                        "submission_id": post['data']['id'],
                        "subreddit": subreddit,
                        "title": post['data']['title'],
                        "selftext": post['data']['selftext'],
                        "author": post['data']['author'],
                        "created_utc": datetime.fromtimestamp(post['data']['created_utc']),
                        "score": post['data']['score'],
                        "num_comments": post['data']['num_comments'],
                        "url": post['data']['url'],
                        "permalink": post['data']['permalink'],
                        "collected_at": datetime.now()
                    })
                
                if post_data:
                    # 게시물 DataFrame 생성 및 Kafka에 전송
                    post_df = spark.createDataFrame(post_data, post_schema)
                    post_df.selectExpr("to_json(struct(*)) AS value") \
                          .write \
                          .format("kafka") \
                          .option("kafka.bootstrap.servers", "kafka:29092") \
                          .option("topic", "reddit_raw_posts") \
                          .save()

                    # 각 게시물의 댓글 가져오기
                    for post in posts:
                        post_id = post['data']['id']
                        comments = fetch_post_comments(subreddit, post_id, token)
                        
                        # 댓글 데이터 변환
                        comment_data = []
                        for comment in comments:
                            if comment['kind'] == 't1':  # t1은 댓글 타입
                                comment_data.append({
                                    "comment_id": comment['data']['id'],
                                    "submission_id": post_id,
                                    "parent_id": comment['data']['parent_id'],
                                    "author": comment['data']['author'],
                                    "body": comment['data']['body'],
                                    "created_utc": datetime.fromtimestamp(comment['data']['created_utc']),
                                    "score": comment['data']['score'],
                                    "collected_at": datetime.now()
                                })
                        
                        if comment_data:
                            # 댓글 DataFrame 생성 및 Kafka에 전송
                            comment_df = spark.createDataFrame(comment_data, comment_schema)
                            comment_df.selectExpr("to_json(struct(*)) AS value") \
                                    .write \
                                    .format("kafka") \
                                    .option("kafka.bootstrap.servers", "kafka:29092") \
                                    .option("topic", "reddit_raw_comments") \
                                    .save()
                
                # API 제한을 고려한 대기
                time.sleep(2)
            
            # 30초 대기
            time.sleep(30)
            
        except Exception as e:
            print(f"Error: {str(e)}")
            time.sleep(60)  # 에러 발생 시 1분 대기

if __name__ == "__main__":
    main() 