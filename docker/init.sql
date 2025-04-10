-- 데이터베이스 생성
CREATE DATABASE coin_community;
\c coin_community;

-- 메시지 테이블 생성
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    message TEXT NOT NULL,
    source VARCHAR(10) NOT NULL,
    created_at TIMESTAMP NOT NULL
);

-- 코인 테이블 생성
CREATE TABLE coins (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    name VARCHAR(50) NOT NULL,
    current_price DECIMAL(20,2) NOT NULL,
    market_cap DECIMAL(20,2) NOT NULL,
    volume_24h DECIMAL(20,2) NOT NULL,
    created_at TIMESTAMP NOT NULL
);

-- 게시글 테이블 생성
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    author VARCHAR(50) NOT NULL,
    views INTEGER NOT NULL DEFAULT 0,
    likes INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL
);

-- 테스트 메시지 데이터
INSERT INTO messages (message, source, created_at) VALUES
('Hello from Java Backend!', 'java', CURRENT_TIMESTAMP),
('Java Test Message 1', 'java', CURRENT_TIMESTAMP),
('Java Test Message 2', 'java', CURRENT_TIMESTAMP),
('Node.js Test Message 1', 'node', CURRENT_TIMESTAMP),
('Node.js Test Message 2', 'node', CURRENT_TIMESTAMP);

-- 코인 데이터
INSERT INTO coins (symbol, name, current_price, market_cap, volume_24h, created_at) VALUES
('BTC', 'Bitcoin', 65000.00, 1200000000000, 50000000000, CURRENT_TIMESTAMP),
('ETH', 'Ethereum', 3500.00, 400000000000, 20000000000, CURRENT_TIMESTAMP),
('SOL', 'Solana', 120.00, 50000000000, 5000000000, CURRENT_TIMESTAMP);

-- 게시글 데이터
INSERT INTO posts (title, content, author, views, likes, created_at) VALUES
('Bitcoin price prediction', 'I think BTC will reach 100k by end of year', 'crypto_expert', 100, 25, CURRENT_TIMESTAMP),
('Ethereum merge success', 'The merge was successful, what are your thoughts?', 'eth_lover', 150, 30, CURRENT_TIMESTAMP),
('Solana ecosystem growing', 'More dApps are being built on Solana', 'sol_developer', 80, 15, CURRENT_TIMESTAMP); 