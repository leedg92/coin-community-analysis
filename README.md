# 코인 데이터 & 커뮤니티 실시간 분석 시스템

## 프로젝트 개요
실시간 코인 시세와 커뮤니티 데이터를 연계 분석하는 시스템으로, 데이터 엔지니어링 핵심 기술 스택 습득을 목표로 합니다. 업비트 코인 시세와 디시인사이드 커뮤니티 데이터를 수집하여 실시간/배치 처리가 결합된 데이터 파이프라인을 구축합니다.

## 기술 스택
- **프론트엔드**: Next.js (React)
- **인증 시스템**: Supabase Auth
- **데이터 처리 백엔드**: Java Spring Boot / Python FastAPI
- **데이터베이스**: PostgreSQL (로컬)
- **실시간 데이터 처리**: WebSocket, Apache Kafka
- **배치 처리**: Spring Batch / Apache Airflow
- **컨테이너화**: Docker, Docker Compose
- **시각화**: Recharts (React), D3.js

## 시스템 아키텍처

### 인증 시스템 (Supabase)
- 사용자 회원가입/로그인 관리
- 소셜 로그인 통합
- JWT 토큰 발급 및 관리
- 사용자 프로필 기본 정보 저장

### 데이터 수집 시스템 (자체 구현)
- **코인 데이터 수집**: 업비트 WebSocket을 통한 실시간 시세 데이터 수집 (10-20개 주요 코인)
- **커뮤니티 데이터 수집**: 디시인사이드 코인 관련 게시판 크롤링 (5분 주기)

### 데이터 처리 파이프라인
- **실시간 처리**: 코인 시세 스트리밍 처리, 1분봉 데이터 생성
- **배치 처리**: 커뮤니티 데이터 정기 수집 및 분석

### 데이터 저장소
- **PostgreSQL**: 최근 2주 데이터 저장
- **장기 저장소**: 2주 이상 데이터 (추후 AWS S3로 이식 가능)

## 구현 단계 및 일정

### 1단계: 기본 환경 설정 (1주)
- 개발 환경 구성 (Docker, PostgreSQL)
- Supabase 프로젝트 설정 및 인증 시스템 구축
- 프론트엔드 초기 설정 (Next.js)

### 2단계: 데이터 수집 시스템 구현 (2주)
- 업비트 WebSocket 연결 및 실시간 데이터 수집
- 디시인사이드 크롤러 구현
- 데이터베이스 스키마 설계 및 구현

### 3단계: 데이터 처리 및 분석 파이프라인 구축 (2주)
- 실시간 데이터 처리 로직 구현
- 배치 처리 시스템 구현
- 데이터 분석 모듈 개발

### 4단계: 프론트엔드 개발 (2주)
- 사용자 인증 UI 구현
- 대시보드 및 데이터 시각화 구현
- 실시간 업데이트 기능 구현

### 5단계: 시스템 통합 및 최적화 (1주)
- 백엔드와 프론트엔드 통합
- 성능 최적화
- 버그 수정 및 안정화

## 인증 흐름 (Supabase와 로컬 시스템 통합)

1. 사용자는 프론트엔드(Next.js)에서 Supabase Auth를 통해 로그인
2. Supabase는 인증 성공 시 JWT 토큰 발급
3. 프론트엔드는 이 토큰을 저장하고 모든 API 요청에 포함
4. 로컬 백엔드 시스템은 JWT 토큰을 검증하여 사용자 인증 확인
5. 인증된 요청에 대해 코인 데이터 및 분석 결과 제공

## 데이터 흐름

1. **코인 데이터**: 
   업비트 → WebSocket 클라이언트 → 데이터 처리 → PostgreSQL → API → 프론트엔드

2. **커뮤니티 데이터**: 
   디시인사이드 → 크롤러 → 데이터 정제 → PostgreSQL → API → 프론트엔드

3. **사용자 설정 및 환경설정**: 
   프론트엔드 → Supabase API → Supabase DB

## 시작하기

### 필수 조건
- Docker 및 Docker Compose
- Node.js 18 이상
- Java 17 / Python 3.9 이상
- PostgreSQL 14 이상

### 설치 및 실행
```bash
# 저장소 클론
git clone https://github.com/leedg92/coin-community-analysis.git
cd coin-community-analysis

# Docker 환경 실행
docker-compose up -d

# 백엔드 실행
cd backend
./gradlew bootRun  # Java의 경우
# 또는
cd backend-python
uvicorn main:app --reload  # Python FastAPI의 경우

# 프론트엔드 실행
cd frontend
npm install
npm run dev
```

### 환경 변수 설정
`.env` 파일을 생성하고 다음 변수를 설정하세요:
```
# Supabase 설정
NEXT_PUBLIC_SUPABASE_URL=your-supabase-project-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key

# 데이터베이스 설정
DB_HOST=localhost
DB_PORT=5432
DB_NAME=coindb
DB_USER=postgres
DB_PASSWORD=your-password

# API 설정
API_PORT=8080
```
