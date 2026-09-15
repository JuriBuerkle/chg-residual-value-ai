package com.chgmeridian.residualvalue.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.math.BigDecimal;

public record AssetEvaluationResponse(
        @JsonProperty("predicted_residual_value_eur") BigDecimal predictedResidualValueEur,
        @JsonProperty("confidence_interval_lower_eur") BigDecimal confidenceIntervalLowerEur,
        @JsonProperty("confidence_interval_upper_eur") BigDecimal confidenceIntervalUpperEur,
        @JsonProperty("margin_error_percentage") BigDecimal marginErrorPercentage
) {}
