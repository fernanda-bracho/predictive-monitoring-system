package com.predictivo.mlsistema;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import java.util.Map;

@RestController
@RequestMapping("/api")


public class PredictionController {
    private final String ML_URL = "http://127.0.0.1:8000/predict";

    @PostMapping("/predict")
    public Map<String, Object> predict(@RequestBody Map<String, Object> request) {

        RestTemplate restTemplate = new RestTemplate();

        Map response = restTemplate.postForObject(
                ML_URL,
                request,
                Map.class
        );

        return response;
    }
}

