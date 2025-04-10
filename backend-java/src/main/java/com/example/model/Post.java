package com.example.model;

import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@Entity
@Table(name = "posts")
public class Post {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String title;

    @Column(nullable = false, length = 1000)
    private String content;

    @Column(nullable = false)
    private String author;

    @Column(nullable = false)
    private Integer views;

    @Column(nullable = false)
    private Integer likes;

    @Column(name = "created_at", nullable = false)
    private LocalDateTime createdAt;
} 