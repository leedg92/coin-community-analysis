FROM postgres:17

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    postgresql-server-dev-17

# Clone and install pgvector
RUN git clone --branch v0.5.1 https://github.com/pgvector/pgvector.git \
    && cd pgvector \
    && make \
    && make install

# Clean up
RUN apt-get remove -y build-essential git postgresql-server-dev-17 \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /pgvector

# 설정 파일 복사
COPY postgresql.conf /etc/postgresql/postgresql.conf

# 초기화 스크립트 복사
COPY init.sql /docker-entrypoint-initdb.d/

# 설정 파일 사용하도록 명령어 수정
CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"] 