package com.chgmeridian.residualvalue.client;

import com.chgmeridian.residualvalue.dto.AssetEvaluationRequest;
import com.chgmeridian.residualvalue.dto.AssetEvaluationResponse;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;

@Component
public class AiModelClient {

    private final RestClient restClient;

    public AiModelClient(@Value("${ai-service.url}") String aiServiceUrl) {
        this.restClient = RestClient.builder()
                .baseUrl(aiServiceUrl)
                .build();
    }

    public AssetEvaluationResponse predictResidualValue(AssetEvaluationRequest request) {
        return restClient.post()
                .uri("/predict-residual-value")
                .body(request)
                .retrieve()
                .body(AssetEvaluationResponse.class);
    }
}
