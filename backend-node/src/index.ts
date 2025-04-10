import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import communityRoutes from './routes/community';
import testRoutes from './routes/test';
import { errorHandler } from './middleware/errorHandler';
import { requestLogger } from './middleware/logger';

dotenv.config();

const app = express();
const port = process.env.PORT || 3001;

// 미들웨어 설정
app.use(cors());
app.use(express.json());
app.use(requestLogger);

// 라우트 설정
app.use('/api/community', communityRoutes);
app.use('/api/test', testRoutes);

// 기본 라우트
app.get('/', (req, res) => {
  res.json({ message: '코인 커뮤니티 분석 API 서버' });
});

// 에러 처리 미들웨어
app.use(errorHandler);

// 서버 시작
app.listen(port, () => {
  console.log(`서버가 포트 ${port}에서 실행 중입니다`);
}); 