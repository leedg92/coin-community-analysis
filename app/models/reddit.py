from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class RedditSubmission(Base):
    __tablename__ = "reddit_raw_submissions"

    submission_id = Column(String(50), primary_key=True)
    subreddit = Column(String(100))
    title = Column(Text)
    selftext = Column(Text)
    author = Column(String(100))
    created_utc = Column(DateTime)
    score = Column(Integer)
    num_comments = Column(Integer)
    url = Column(Text)
    permalink = Column(Text)
    collected_at = Column(DateTime)

    analysis = relationship("RedditAnalysis", back_populates="submission", uselist=False)

class RedditAnalysis(Base):
    __tablename__ = "reddit_analysis_submissions"

    submission_id = Column(String(50), ForeignKey("reddit_raw_submissions.submission_id"), primary_key=True)
    title_embedding = Column(Text)  # JSON으로 저장
    selftext_embedding = Column(Text)  # JSON으로 저장
    sentiment_score = Column(Float)
    sentiment_label = Column(String(20))
    analyzed_at = Column(DateTime)

    submission = relationship("RedditSubmission", back_populates="analysis") 