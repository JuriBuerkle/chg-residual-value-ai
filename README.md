# CHG Residual Value AI — Enterprise Monorepo Service

An end-to-end, monorepo-based machine learning solution designed to evaluate asset residual value. The system integrates a Java Spring Boot backend acting as the API orchestrator with a Python FastAPI microservice serving ML predictions.

## 🏗 Architecture Overview

```text
[ Client / Postman ] 
        │ (HTTP POST /api/v1/assets/evaluate)
        ▼
┌─────────────────────────────────────────┐
│       Spring Boot Backend (8080)        │
│  - AssetEvaluationController            │
│  - AiModelClient (RestClient)           │
└──────────────────┬──────────────────────┘
                   │ (HTTP POST /predict-residual-value)
                   ▼
┌─────────────────────────────────────────┐
│       FastAPI ML Microservice (8000)    │
│  - Scikit-Learn Model (.pkl)            │
│  - Pydantic Validation                  │
└─────────────────────────────────────────┘

🛠 Tech Stack
Backend: Java 17, Spring Boot 3.2, RestClient, Maven

AI/ML Service: Python 3.13, FastAPI, Uvicorn, Scikit-learn, Pydantic

Architecture: Monorepo, REST API Integration

📂 Project Structure
Plaintext
chg-residual-value-ai/
├── ai-service/             # Python FastAPI ML microservice
│   ├── main.py             # FastAPI app and inference endpoints
│   ├── requirements.txt    # Python dependencies
│   └── residual_value_model.pkl # Trained Scikit-learn model
├── src/                    # Java Spring Boot application
│   └── main/java/com/chgmeridian/residualvalue/
│       ├── client/         # RestClient for inter-service communication
│       ├── controller/     # REST Endpoints
│       └── dto/            # Data Transfer Objects
└── pom.xml                 # Maven build configuration

🚀 Getting Started
1. Run Python ML Service
Bash
cd ai-service
source venv/Scripts/activate
python -m uvicorn main:app --reload --port 8000
2. Run Java Spring Boot Service
Open a new terminal tab at root:

Bash
mvn spring-boot:run
3. Test API Endpoint
Send a POST request to http://localhost:8080/api/v1/assets/evaluate:

Sample Payload:

JSON
{
  "category": "Laptop",
  "brand": "Dell",
  "initial_price_eur": 1200,
  "age_months": 24,
  "ram_gb": 16,
  "storage_gb": 512,
  "grade": "Grade B"
}
Expected Response (200 OK):

JSON
{
  "predicted_residual_value_eur": 706.18,
  "confidence_interval_lower_eur": 583.83,
  "confidence_interval_upper_eur": 850.51,
  "margin_error_percentage": 18.88
}
