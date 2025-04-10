const express = require('express');
const { Pool } = require('pg');
const cors = require('cors');

const app = express();
const port = 4000;

// PostgreSQL 연결 설정
const pool = new Pool({
    user: 'postgres',
    host: 'localhost',
    database: 'coindb',
    password: 'postgres',
    port: 5432,
});

// 미들웨어 설정
app.use(cors({
    origin: 'http://localhost:3000'
}));
app.use(express.json());

// Node.js 메시지 조회 API
app.get('/messages/node', async (req, res) => {
    try {
        const result = await pool.query(
            'SELECT * FROM test_messages WHERE source = $1',
            ['node']
        );
        res.json(result.rows);
    } catch (err) {
        console.error('Error executing query', err);
        res.status(500).json({ error: 'Database error' });
    }
});

// 전체 메시지 조회 API
app.get('/messages', async (req, res) => {
    try {
        const result = await pool.query('SELECT * FROM test_messages');
        res.json(result.rows);
    } catch (err) {
        console.error('Error executing query', err);
        res.status(500).json({ error: 'Database error' });
    }
});

// 서버 시작
app.listen(port, () => {
    console.log(`Node.js server running at http://localhost:${port}`);
}); 