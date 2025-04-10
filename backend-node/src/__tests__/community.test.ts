/// <reference types="jest" />
import request from 'supertest';
import express from 'express';
import { Router } from 'express';
import { Pool } from 'pg';

// 데이터베이스 모킹
jest.mock('../config/database', () => {
  const mockPool = {
    query: jest.fn()
  };
  
  // 모의 데이터 설정
  mockPool.query.mockImplementation((query: string, params?: any[]) => {
    if (params && params[0] === 'twitter') {
      return Promise.resolve({
        rows: [
          { id: 1, platform: 'twitter', content: 'Test tweet', sentiment_score: 0.8, created_at: new Date() }
        ]
      });
    }
    return Promise.resolve({
      rows: [
        { id: 1, platform: 'twitter', content: 'Test tweet', sentiment_score: 0.8, created_at: new Date() },
        { id: 2, platform: 'reddit', content: 'Test post', sentiment_score: 0.5, created_at: new Date() }
      ]
    });
  });

  return mockPool;
});

// 라우터 임포트는 모킹 설정 후에 해야 합니다
import communityRoutes from '../routes/community';

const app = express();
app.use(express.json());
app.use('/api/community', communityRoutes);

describe('Community Routes', () => {
  it('GET /api/community should return community data', async () => {
    const response = await request(app).get('/api/community');
    expect(response.status).toBe(200);
    expect(Array.isArray(response.body)).toBe(true);
    expect(response.body.length).toBe(2);
  });

  it('GET /api/community/:platform should return platform specific data', async () => {
    const platform = 'twitter';
    const response = await request(app).get(`/api/community/${platform}`);
    expect(response.status).toBe(200);
    expect(Array.isArray(response.body)).toBe(true);
    expect(response.body.length).toBe(1);
    expect(response.body[0].platform).toBe('twitter');
  });
}); 