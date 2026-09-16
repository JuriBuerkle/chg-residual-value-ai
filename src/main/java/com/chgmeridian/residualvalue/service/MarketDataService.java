package com.chgmeridian.residualvalue.service;

import org.springframework.stereotype.Service;

@Service
public class MarketDataService {

    public Double fetchCurrentMarketPrice(String category, Double initialPrice, Integer ageMonths) {
        // Имитация вызова внешнего REST API (eBay / BackMarket)
        // В реальном продакшене здесь вызов RestClient к внешнему API
        double depreciationFactor = Math.max(0.2, 1.0 - (ageMonths * 0.025));
        return Math.round(initialPrice * depreciationFactor * 100.0) / 100.0;
    }
}
