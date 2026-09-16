package com.chgmeridian.residualvalue.controller;

import com.chgmeridian.residualvalue.client.AiModelClient;
import com.chgmeridian.residualvalue.dto.AssetEvaluationRequest;
import com.chgmeridian.residualvalue.dto.AssetEvaluationResponse;
import com.chgmeridian.residualvalue.service.MarketDataService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/assets")
public class AssetEvaluationController {

    private final AiModelClient aiModelClient;
    private final MarketDataService marketDataService;

    public AssetEvaluationController(AiModelClient aiModelClient, MarketDataService marketDataService) {
        this.aiModelClient = aiModelClient;
        this.marketDataService = marketDataService;
    }

    @PostMapping("/evaluate")
    public ResponseEntity<AssetEvaluationResponse> evaluateAsset(@RequestBody AssetEvaluationRequest request) {
        // 1. Обогащаем запрос данными с рынка, если они не переданы
        Double marketPrice = request.marketAvgPriceEur() != null 
            ? request.marketAvgPriceEur() 
            : marketDataService.fetchCurrentMarketPrice(request.category(), request.initialPriceEur(), request.ageMonths());

        AssetEvaluationRequest enrichedRequest = new AssetEvaluationRequest(
            request.category(), request.brand(), request.initialPriceEur(),
            request.ageMonths(), request.ramGb(), request.storageGb(),
            request.grade(), marketPrice
        );

        // 2. Отправляем обогащенный запрос в ML-сервис
        AssetEvaluationResponse response = aiModelClient.predictResidualValue(enrichedRequest);
        return ResponseEntity.ok(response);
    }
}
