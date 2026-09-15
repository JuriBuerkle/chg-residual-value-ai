package com.chgmeridian.residualvalue.controller;

import com.chgmeridian.residualvalue.client.AiModelClient;
import com.chgmeridian.residualvalue.dto.AssetEvaluationRequest;
import com.chgmeridian.residualvalue.dto.AssetEvaluationResponse;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/assets")
public class AssetEvaluationController {

    private final AiModelClient aiModelClient;

    public AssetEvaluationController(AiModelClient aiModelClient) {
        this.aiModelClient = aiModelClient;
    }

    @PostMapping("/evaluate")
    public ResponseEntity<AssetEvaluationResponse> evaluateAsset(@RequestBody AssetEvaluationRequest request) {
        AssetEvaluationResponse response = aiModelClient.predictResidualValue(request);
        return ResponseEntity.ok(response);
    }
}
