#!/bin/bash

echo "Waiting for Kafka to be ready..."
while ! nc -z kafka 9092; do
  sleep 2
  echo "Waiting for Kafka..."
done

echo "Kafka is ready. Creating topics..."

# Create post topic
kafka-topics.sh --create \
  --bootstrap-server kafka:9092 \
  --topic reddit_raw_posts \
  --partitions 3 \
  --replication-factor 1 \
  --if-not-exists

# Create comment topic
kafka-topics.sh --create \
  --bootstrap-server kafka:9092 \
  --topic reddit_raw_comments \
  --partitions 3 \
  --replication-factor 1 \
  --if-not-exists

echo "Kafka topics created successfully!" 