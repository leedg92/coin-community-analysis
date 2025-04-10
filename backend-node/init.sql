CREATE TABLE IF NOT EXISTS test_messages (
  id SERIAL PRIMARY KEY,
  message TEXT NOT NULL,
  source VARCHAR(10) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 샘플 데이터 추가
INSERT INTO test_messages (message, source) VALUES
  ('Hello from Java!', 'java'),
  ('Hello from Node!', 'node'); 