-- 데이터베이스 생성
CREATE DATABASE coindb;

-- coindb 연결
\c coindb;

-- 테스트용 메시지 테이블 생성
CREATE TABLE IF NOT EXISTS test_messages (
    id SERIAL PRIMARY KEY,            -- 자동 증가하는 기본키
    message VARCHAR(255) NOT NULL,    -- 메시지 내용
    source VARCHAR(50) NOT NULL,      -- 메시지 출처 (java/node)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- 생성 시간
);

-- 코인 정보 테이블 생성 (추후 사용)
CREATE TABLE IF NOT EXISTS coin_prices (
    id SERIAL PRIMARY KEY,
    coin_symbol VARCHAR(20) NOT NULL,     -- 코인 심볼 (BTC, ETH 등)
    price DECIMAL(20, 8) NOT NULL,        -- 코인 가격
    volume DECIMAL(20, 8) NOT NULL,       -- 거래량
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 커뮤니티 게시글 테이블 생성 (추후 사용)
CREATE TABLE IF NOT EXISTS community_posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,          -- 게시글 제목
    content TEXT,                         -- 게시글 내용
    author VARCHAR(100),                  -- 작성자
    sentiment DECIMAL(3, 2),              -- 감성 분석 점수 (-1 ~ 1)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 테스트 데이터 삽입
INSERT INTO test_messages (message, source) VALUES 
    ('Hello, Database!', 'system'),
    ('테스트 메시지입니다.', 'system');
