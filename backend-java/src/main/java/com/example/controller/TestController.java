package com.example.controller;

import com.example.model.Message;
import com.example.repository.MessageRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/test")
@CrossOrigin(origins = {"http://localhost:3000", "http://localhost:3002"})
public class TestController {

    @Autowired
    private MessageRepository messageRepository;

    @GetMapping("/java")
    public List<Message> getJavaMessages() {
        return messageRepository.findBySourceOrderByCreatedAtDesc("java");
    }
} 