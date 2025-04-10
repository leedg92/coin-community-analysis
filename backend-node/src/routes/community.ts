import express from 'express';
import { pool } from '../config/database';
import { CommunityData } from '../types';

const router = express.Router();

// 전체 커뮤니티 데이터 조회
router.get('/', async (req, res) => {
  try {
    const result = await pool.query<CommunityData>(
      'SELECT * FROM community_data ORDER BY created_at DESC LIMIT 100'
    );
    res.json(result.rows);
  } catch (err) {
    console.error('데이터 조회 중 오류 발생:', err);
    res.status(500).json({ error: '데이터베이스 오류' });
  }
});

// 플랫폼별 데이터 조회
router.get('/:platform', async (req, res) => {
  try {
    const { platform } = req.params;
    const result = await pool.query<CommunityData>(
      'SELECT * FROM community_data WHERE platform = $1 ORDER BY created_at DESC LIMIT 50',
      [platform]
    );
    res.json(result.rows);
  } catch (err) {
    console.error('데이터 조회 중 오류 발생:', err);
    res.status(500).json({ error: '데이터베이스 오류' });
  }
});

export default router; 