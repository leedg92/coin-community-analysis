from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from typing import List
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import numpy as np
from ..database import get_db
from ..models.reddit import RedditSubmission, RedditAnalysis

router = APIRouter()

# Reddit API 설정
CLIENT_ID = 'k21vSArVWO03ppn0q2TVjg'
CLIENT_SECRET = 'E89X0gAfyC6Mt_8dVfeRyw3bMA_vfQ'
USERNAME = 'Jackuri_dev'
PASSWORD = '@dlehd2231'
USER_AGENT = 'DocumentKey6026'

# 모델 로드
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
sentiment_analyzer = pipeline("sentiment-analysis", model="finiteautomata/bertweet-base-sentiment-analysis")

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
        raise HTTPException(status_code=500, detail="Failed to get Reddit token")

def analyze_text(text):
    """텍스트를 분석하여 임베딩과 감성 점수를 반환합니다."""
    if not text:
        return [0.0] * 384, 0.0, "neutral"
    
    # 임베딩 생성
    embedding = model.encode(text).tolist()
    
    # 감성 분석
    result = sentiment_analyzer(text)[0]
    score = result['score']
    if result['label'] == 'NEU':
        label = "neutral"
    elif result['label'] == 'POS':
        label = "positive"
    else:
        label = "negative"
        score = -score
    
    return embedding, score, label

@router.get("/reddit/latest/{subreddit}")
async def get_latest_posts(subreddit: str, db: Session = Depends(get_db)):
    """특정 서브레딧의 최신 게시물을 가져오고 분석합니다."""
    try:
        # 토큰 가져오기
        token = get_reddit_token()
        
        # 게시물 가져오기
        headers = {
            'Authorization': f'Bearer {token}',
            'User-Agent': USER_AGENT
        }
        
        response = requests.get(
            f'https://oauth.reddit.com/r/{subreddit}/new',
            headers=headers,
            params={'limit': 10}
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch Reddit posts")
        
        posts = response.json()['data']['children']
        results = []
        
        for post in posts:
            post_data = post['data']
            
            # 원시 데이터 저장
            submission = RedditSubmission(
                submission_id=post_data['id'],
                subreddit=subreddit,
                title=post_data['title'],
                selftext=post_data['selftext'],
                author=post_data['author'],
                created_utc=datetime.fromtimestamp(post_data['created_utc']),
                score=post_data['score'],
                num_comments=post_data['num_comments'],
                url=post_data['url'],
                permalink=post_data['permalink'],
                collected_at=datetime.now()
            )
            db.add(submission)
            
            # 분석 수행
            title_embedding, title_sentiment, title_label = analyze_text(post_data['title'])
            selftext_embedding, selftext_sentiment, selftext_label = analyze_text(post_data['selftext'])
            
            # 분석 결과 저장
            analysis = RedditAnalysis(
                submission_id=post_data['id'],
                title_embedding=title_embedding,
                selftext_embedding=selftext_embedding,
                sentiment_score=(title_sentiment + selftext_sentiment) / 2,
                sentiment_label=title_label if abs(title_sentiment) > abs(selftext_sentiment) else selftext_label,
                analyzed_at=datetime.now()
            )
            db.add(analysis)
            
            results.append({
                "submission": submission,
                "analysis": analysis
            })
        
        db.commit()
        return results
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/reddit/analysis/{subreddit}")
async def get_subreddit_analysis(subreddit: str, db: Session = Depends(get_db)):
    """특정 서브레딧의 분석 결과를 조회합니다."""
    try:
        # 최근 24시간 데이터 조회
        cutoff_time = datetime.now() - timedelta(days=1)
        
        analysis = db.query(RedditAnalysis)\
            .join(RedditSubmission)\
            .filter(RedditSubmission.subreddit == subreddit)\
            .filter(RedditAnalysis.analyzed_at >= cutoff_time)\
            .all()
        
        return {
            "total_posts": len(analysis),
            "average_sentiment": sum(a.sentiment_score for a in analysis) / len(analysis) if analysis else 0,
            "sentiment_distribution": {
                "positive": len([a for a in analysis if a.sentiment_label == "positive"]),
                "neutral": len([a for a in analysis if a.sentiment_label == "neutral"]),
                "negative": len([a for a in analysis if a.sentiment_label == "negative"])
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 