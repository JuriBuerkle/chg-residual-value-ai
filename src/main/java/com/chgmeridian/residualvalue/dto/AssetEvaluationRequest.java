package com.chgmeridian.residualvalue.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.math.BigDecimal;

public record AssetEvaluationRequest(
        String category,
        String brand,
        @JsonProperty("initial_price_eur") BigDecimal initialPriceEur,
        @JsonProperty("age_months") Integer ageMonths,
        @JsonProperty("ram_gb") Integer ramGb,
        @JsonProperty("storage_gb") Integer storageGb,
        String grade
) {}
