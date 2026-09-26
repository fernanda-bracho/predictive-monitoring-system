package com.predictivo.mlsistema;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import java.util.Map;

@RestController
@RequestMapping("/api")


public class PredictionController {

    @Value("${ml.service.url:http://127.0.0.1:8000/predict}")
    private String ML_URL;

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

