package com.example.model;

import jakarta.persistence.*;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@Entity
@Table(name = "coins")
public class Coin {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String symbol;

    @Column(nullable = false)
    private String name;

    @Column(name = "current_price", nullable = false)
    private BigDecimal currentPrice;

    @Column(name = "market_cap", nullable = false)
    private BigDecimal marketCap;

    @Column(name = "volume_24h", nullable = false)
    private BigDecimal volume24h;

    @Column(name = "created_at", nullable = false)
    private LocalDateTime createdAt;
} 