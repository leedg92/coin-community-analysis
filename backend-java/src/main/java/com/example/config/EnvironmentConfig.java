package com.example.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.PropertySource;

@Configuration
@PropertySource(value = {"file:../../.env"}, ignoreResourceNotFound = true)
public class EnvironmentConfig {
    // Spring Boot will automatically load environment variables
} 