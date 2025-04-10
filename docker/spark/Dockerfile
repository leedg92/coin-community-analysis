FROM bitnami/spark:3.5

USER root

# Install Java and required tools
RUN apt-get update && \
    apt-get install -y netcat-traditional wget && \
    mkdir -p /tmp/spark-events && \
    chmod 777 /tmp/spark-events

# Install Kafka tools
RUN wget https://downloads.apache.org/kafka/3.5.1/kafka_2.12-3.5.1.tgz && \
    tar -xzf kafka_2.12-3.5.1.tgz && \
    mv kafka_2.12-3.5.1/bin/* /usr/local/bin/ && \
    rm -rf kafka_2.12-3.5.1 kafka_2.12-3.5.1.tgz

# Copy scripts and config
COPY create_kafka_topics.sh /opt/spark/
COPY config/reddit_config.json /opt/spark/config/
COPY scripts/reddit_collector.py /opt/spark/
COPY scripts/reddit_processor.py /opt/spark/

RUN chmod +x /opt/spark/create_kafka_topics.sh

USER 1001

CMD ["/bin/bash", "-c", "/opt/spark/create_kafka_topics.sh && /opt/bitnami/scripts/spark/run.sh"] 