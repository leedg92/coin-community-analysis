FROM postgres:14

# 설정 파일 복사
COPY postgresql.conf /etc/postgresql/postgresql.conf

# 초기화 스크립트 복사
COPY init.sql /docker-entrypoint-initdb.d/

# 설정 파일 사용하도록 명령어 수정
CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"] 