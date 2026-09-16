package com.chgmeridian.residualvalue.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public record AssetEvaluationRequest(
    String category,
    String brand,
    @JsonProperty("initial_price_eur") Double initialPriceEur,
    @JsonProperty("age_months") Integer ageMonths,
    @JsonProperty("ram_gb") Integer ramGb,
    @JsonProperty("storage_gb") Integer storageGb,
    String grade,
    @JsonProperty("market_avg_price_eur") Double marketAvgPriceEur // Новое поле
) {}
