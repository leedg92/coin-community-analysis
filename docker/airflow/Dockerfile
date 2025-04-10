FROM apache/airflow:2.5.0

USER root

# 필요한 시스템 패키지 설치
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        openjdk-11-jdk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Python 패키지 설치
COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

# Airflow 설정 파일 복사
COPY config/airflow.cfg ${AIRFLOW_HOME}/airflow.cfg 