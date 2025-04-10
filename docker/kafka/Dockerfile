FROM confluentinc/cp-kafka:7.3.0

# 설정 파일 복사
COPY server.properties /etc/kafka/server.properties

# Kafka 브로커 시작
CMD ["kafka-server-start", "/etc/kafka/server.properties"] 