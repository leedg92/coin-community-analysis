FROM bitnami/spark:3.3.0

# 설정 파일 복사
COPY spark-defaults.conf /opt/bitnami/spark/conf/spark-defaults.conf

# 필요한 Java 패키지 설치
USER root
RUN apt-get update && apt-get install -y openjdk-11-jdk
USER 1001

# Spark 환경 변수 설정
ENV SPARK_HOME=/opt/bitnami/spark
ENV PATH=$PATH:$SPARK_HOME/bin 