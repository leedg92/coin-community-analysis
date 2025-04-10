CREATE TABLE IF NOT EXISTS test_messages (
    id SERIAL PRIMARY KEY,
    message TEXT NOT NULL,
    source VARCHAR(10) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 테스트 데이터 삽입
INSERT INTO test_messages (message, source) VALUES 
    ('자바 백엔드에서 보낸 테스트 메시지입니다.', 'java'),
    ('노드 백엔드에서 보낸 테스트 메시지입니다.', 'node'); 