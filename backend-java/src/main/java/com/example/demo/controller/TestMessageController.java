package com.example.demo.controller;

import com.example.demo.model.TestMessage;
import com.example.demo.repository.TestMessageRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/messages")
@RequiredArgsConstructor
@CrossOrigin(origins = "http://localhost:3001")
public class TestMessageController {

    private final TestMessageRepository testMessageRepository;

    @GetMapping("/java")
    public List<TestMessage> getJavaMessages() {
        return testMessageRepository.findBySource("java");
    }

    @GetMapping
    public List<TestMessage> getAllMessages() {
        return testMessageRepository.findAll();
    }
} 