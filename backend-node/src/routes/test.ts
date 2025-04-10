import express from 'express';
import { pool } from '../config/database';

const router = express.Router();

// Node 테스트 데이터 조회
router.get('/node', async (req, res) => {
  try {
    const result = await pool.query(
      'SELECT * FROM test_messages WHERE source = $1 ORDER BY created_at DESC',
      ['node']
    );
    res.json(result.rows);
  } catch (error) {
    console.error('Database query error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

export default router; 