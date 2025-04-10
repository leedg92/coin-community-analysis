# Coin Community Analysis

실시간 코인 가격과 커뮤니티 데이터 분석 프로젝트

## 목차
1. [프로젝트 개요](#1-프로젝트-개요)
2. [프로젝트 구조](#2-프로젝트-구조)
3. [데이터베이스 설정](#3-데이터베이스-설정)
4. [Node.js 백엔드 구현](#4-nodejs-백엔드-구현)
5. [Java 백엔드 구현](#5-java-백엔드-구현)
6. [BFF 구현](#6-bff-구현)
7. [실행 방법](#7-실행-방법)
8. [테스트](#8-테스트)
9. [Python 데이터 처리](#9-python-데이터-처리)

## 1. 프로젝트 개요

실시간 코인 커뮤니티 분석 플랫폼은 다음과 같은 기술 스택을 사용합니다:

- **프론트엔드**: Next.js (BFF 패턴)
- **백엔드**: Node.js (Express), Java (Spring Boot)
- **데이터베이스**: PostgreSQL
- **개발 도구**: Docker, TypeScript

## 2. 프로젝트 구조

```
├── frontend/          # Next.js 프론트엔드 (포트: 3002)
├── bff/              # Backend for Frontend (포트: 3000)
├── backend-node/     # Node.js 백엔드 (포트: 3001)
├── backend-java/     # Java Spring Boot 백엔드 (포트: 8080)
├── config/           # 공통 설정
└── docker/           # 데이터 처리 컴포넌트 Docker 설정
```

### 2.1 config 폴더 설정

`config` 폴더는 프로젝트의 공통 설정 파일들을 포함합니다. 이 폴더는 `.gitignore`에 포함되어 있으므로, 프로젝트를 처음 클론한 후 다음 파일들을 생성해야 합니다:

```
config/
├── .env              # 공통 환경 변수 설정
├── database.json     # 데이터베이스 연결 설정
├── api.json          # API 엔드포인트 설정
└── logging.json      # 로깅 설정
```

각 파일의 예시 내용:

```env
# .env
NODE_ENV=development
PORT=3000
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/coindb
```

```json
// database.json
{
  "host": "localhost",
  "port": 5432,
  "database": "coindb",
  "username": "postgres",
  "password": "postgres"
}
```

```json
// api.json
{
  "nodeBackend": "http://localhost:3001",
  "javaBackend": "http://localhost:8080",
  "bff": "http://localhost:3000"
}
```

```json
// logging.json
{
  "level": "info",
  "format": "json",
  "output": "file",
  "path": "./logs"
}
```

## 3. 데이터베이스 설정

### 3.1 Docker Compose 설정

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:latest
    container_name: postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: coindb
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### 3.2 데이터베이스 초기화

```sql
-- init.sql
CREATE TABLE IF NOT EXISTS test_messages (
  id SERIAL PRIMARY KEY,
  message TEXT NOT NULL,
  source VARCHAR(10) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 샘플 데이터
INSERT INTO test_messages (message, source) VALUES
  ('Hello from Java!', 'java'),
  ('Hello from Node!', 'node');
```

## 4. Node.js 백엔드 구현

### 4.1 프로젝트 초기화

```bash
mkdir backend-node
cd backend-node
npm init -y

# 의존성 설치
npm install express pg cors dotenv
npm install -D typescript @types/express @types/pg @types/cors @types/node @typescript-eslint/eslint-plugin @typescript-eslint/parser eslint ts-node-dev
```

### 4.2 TypeScript 설정

```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "es2018",
    "module": "commonjs",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### 4.3 환경 변수 설정

```env
# .env
PORT=3001
POSTGRES_USER=postgres
POSTGRES_HOST=localhost
POSTGRES_DB=coindb
POSTGRES_PASSWORD=postgres
POSTGRES_PORT=5432
```

### 4.4 데이터베이스 연결

```typescript
// src/config/database.ts
import { Pool } from 'pg';
import dotenv from 'dotenv';

dotenv.config();

const pool = new Pool({
  user: process.env.POSTGRES_USER,
  host: process.env.POSTGRES_HOST,
  database: process.env.POSTGRES_DB,
  password: process.env.POSTGRES_PASSWORD,
  port: parseInt(process.env.POSTGRES_PORT || '5432'),
});

export default pool;
```

### 4.5 API 라우터

```typescript
// src/routes/test.ts
import { Router } from 'express';
import pool from '../config/database';

const router = Router();

// Java 테스트 데이터 조회
router.get('/java', async (req, res) => {
  try {
    const result = await pool.query(
      'SELECT * FROM test_messages WHERE source = $1',
      ['java']
    );
    res.json(result.rows);
  } catch (err) {
    console.error('데이터 조회 중 오류 발생:', err);
    res.status(500).json({ error: '데이터베이스 오류' });
  }
});

// Node 테스트 데이터 조회
router.get('/node', async (req, res) => {
  try {
    const result = await pool.query(
      'SELECT * FROM test_messages WHERE source = $1',
      ['node']
    );
    res.json(result.rows);
  } catch (err) {
    console.error('데이터 조회 중 오류 발생:', err);
    res.status(500).json({ error: '데이터베이스 오류' });
  }
});

export default router;
```

### 4.6 메인 애플리케이션

```typescript
// src/index.ts
import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import testRoutes from './routes/test';

dotenv.config();

const app = express();
const port = process.env.PORT || 3001;

app.use(cors());
app.use(express.json());
app.use('/api/test', testRoutes);

app.listen(port, () => {
  console.log(`서버가 포트 ${port}에서 실행 중입니다`);
});
```

## 5. Java 백엔드 구현

### 5.1 프로젝트 설정

```xml
<!-- pom.xml -->
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>
    <dependency>
        <groupId>org.postgresql</groupId>
        <artifactId>postgresql</artifactId>
    </dependency>
</dependencies>
```

### 5.2 애플리케이션 설정

```yaml
# application.yml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/coindb
    username: postgres
    password: postgres
  jpa:
    hibernate:
      ddl-auto: none
server:
  port: 8080
```

### 5.3 엔티티 클래스

```java
// TestMessage.java
@Entity
@Table(name = "test_messages")
public class TestMessage {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String message;
    private String source;
    private LocalDateTime createdAt;
    // Getters and Setters
}
```

### 5.4 컨트롤러

```java
// TestController.java
@RestController
@RequestMapping("/api/test")
@CrossOrigin
public class TestController {
    @Autowired
    private TestMessageRepository repository;

    @GetMapping("/java")
    public List<TestMessage> getJavaMessages() {
        return repository.findBySource("java");
    }
}
```

## 6. BFF 구현

### 6.1 프로젝트 초기화

```bash
npx create-next-app@latest bff --typescript --tailwind --eslint
cd bff
```

### 6.2 메인 페이지

```typescript
// src/app/page.tsx
'use client';

import { useState } from 'react';

interface TestMessage {
  id: number;
  message: string;
  source: string;
  created_at: string;
}

export default function Home() {
  const [messages, setMessages] = useState<TestMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async (source: 'java' | 'node') => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch(`http://localhost:3001/api/test/${source}`);
      if (!response.ok) {
        throw new Error('데이터를 가져오는데 실패했습니다');
      }
      const data = await response.json();
      setMessages(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : '오류가 발생했습니다');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4">
          Hello, <span className="text-blue-500">코인 커뮤니티</span>!
        </h1>
        <p className="text-lg text-gray-600 mb-8">
          실시간 코인 커뮤니티 분석 플랫폼에 오신 것을 환영합니다
        </p>
        
        <div className="flex gap-4 justify-center mb-8">
          <button
            onClick={() => fetchData('java')}
            className="bg-green-500 text-white px-6 py-2 rounded-lg hover:bg-green-600"
          >
            Java Test
          </button>
          <button
            onClick={() => fetchData('node')}
            className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600"
          >
            Node Test
          </button>
        </div>

        {loading && <p>데이터를 불러오는 중...</p>}
        {error && <p className="text-red-500">{error}</p>}
        {messages.length > 0 && (
          <div className="border rounded-lg p-4">
            <h2 className="text-xl font-semibold mb-4">테스트 메시지</h2>
            <ul className="space-y-2">
              {messages.map((msg) => (
                <li key={msg.id} className="text-left border-b pb-2">
                  <p className="font-medium">{msg.message}</p>
                  <p className="text-sm text-gray-500">
                    출처: {msg.source} | 시간: {new Date(msg.created_at).toLocaleString()}
                  </p>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
```

## 7. 실행 방법

### 7.1 데이터베이스 실행
```bash
# PostgreSQL 컨테이너 실행
docker-compose up -d

# 데이터베이스 초기화
docker cp backend-node/init.sql postgres:/init.sql
docker exec -i postgres psql -U postgres -d coindb -f /init.sql
```

### 7.2 Node.js 백엔드 실행
```bash
cd backend-node
npm run dev
# 서버가 포트 3001에서 실행됩니다
```

### 7.3 Java 백엔드 실행
```bash
cd backend-java
./mvnw spring-boot:run
# 서버가 포트 8080에서 실행됩니다
```

### 7.4 BFF 실행
```bash
cd bff
npm run dev
# 서버가 포트 3000에서 실행됩니다
```

## 8. 테스트

1. 웹 브라우저에서 http://localhost:3000 접속

2. 버튼 테스트:
   - "Java Test" 버튼 클릭: Java 백엔드에서 데이터 조회
   - "Node Test" 버튼 클릭: Node.js 백엔드에서 데이터 조회

3. 응답 데이터 확인:
   - 메시지 내용
   - 출처 (java/node)
   - 생성 시간

4. 에러 처리:
   - 서버 연결 실패 시 에러 메시지 표시
   - 로딩 중 상태 표시

## 9. Python 데이터 처리

### 9.1 Python 환경 설정

1. 가상환경 생성 및 활성화:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

2. 의존성 설치:
```bash
pip install -r requirements.txt
```

### 9.2 주요 Python 패키지

- **데이터 처리**: pandas, numpy, scikit-learn
- **데이터베이스**: psycopg2-binary, SQLAlchemy
- **웹 크롤링**: beautifulsoup4, requests, selenium
- **데이터 스트리밍**: kafka-python, confluent-kafka
- **스파크 처리**: pyspark, delta-spark
- **워크플로우**: apache-airflow

### 9.3 개발 도구

- **코드 포맷팅**: black
- **린터**: flake8
- **타입 체크**: mypy
- **테스트**: pytest

### 9.4 Git 설정

프로젝트는 다음 파일들을 Git에서 제외합니다:

1. 환경 설정 파일:
   - `.env`, `.env.local`
   - `airflow.cfg`

2. 가상환경 및 캐시:
   - `venv/`, `__pycache__/`
   - `.pytest_cache/`

3. 빌드 결과물:
   - `dist/`, `build/`
   - `node_modules/`
   - `target/`

4. IDE 설정:
   - `.idea/`, `.vscode/`

5. 로그 및 데이터 파일:
   - `logs/`
   - `*.csv`, `*.xlsx`
   - `*.db`, `*.sqlite3`