package com.example.demo.repository;

import com.example.demo.model.TestMessage;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface TestMessageRepository extends JpaRepository<TestMessage, Long> {
    List<TestMessage> findBySource(String source);
} 