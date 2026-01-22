# AI Grading Service

This project provides an automatic grading service for paragraph-based
exam questions using semantic similarity powered by Sentence
Transformers.

The service is exposed as a REST API and is designed to be consumed by a
backend application (e.g., PHP) and a mobile frontend (e.g., Flutter).

------------------------------------------------------------------------

## Features

-   Automatic grading of paragraph answers
-   Semantic similarity using `all-MiniLM-L6-v2`
-   Stateless REST API
-   Fast response time (model loaded once)
-   JSON input / JSON output
-   Easy integration with any backend technology

------------------------------------------------------------------------

## Tech Stack

-   Python 3.10+
-   FastAPI
-   Uvicorn
-   sentence-transformers
-   PyTorch (CPU)

------------------------------------------------------------------------

## Project Structure

    ai-grading-service
    ├── api.py
    ├── grading_model.py
    ├── requirements.txt
    └── README.md

------------------------------------------------------------------------

## Included Examples

-   Sample exam specs live in `data/exams/` (e.g., `Biology.json`,
    `English.json`, `Math.json`).
-   Sample student answers live in `data/students/<Subject>/` (e.g.,
    `data/students/Biology/Ahmed.json`).
-   Sample grading outputs live in `data/results/<Subject>/` (e.g.,
    `data/results/Biology/Ahmed_results.json`).
-   You can hit the `/grade` endpoint using the provided `exam_name` and
    `student_name` from the examples above (e.g., `Biology` / `Ahmed`) to
    reproduce the sample results.

------------------------------------------------------------------------

## Setup Instructions

### 1. Create and activate a virtual environment

**Windows**

``` bash
python -m venv venv
venv\Scripts\activate
```

------------------------------------------------------------------------

### 2. Install dependencies

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

### 3. Run the API server

``` bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

The API will be available at:

    http://localhost:8000

Swagger (interactive API documentation):

    http://localhost:8000/docs

------------------------------------------------------------------------

## API Usage

### Endpoint

    POST /grade

------------------------------------------------------------------------

### Request Body (JSON)

``` json
{
  "exam_name": "Biology",
  "student_name": "Ahmed",
  "questions": {
    "q1": {
      "type": "paragraph",
      "answer": "Photosynthesis is the process by which plants make food.",
      "points": 10
    }
  },
  "student_answers": {
    "q1": "Plants make food using sunlight"
  }
}
```

------------------------------------------------------------------------

### Response Body (JSON)

``` json
{
  "exam": "Biology",
  "student": "Ahmed",
  "scores": {
    "q1": 8
  },
  "total": 8,
  "max_total": 10
}
```

------------------------------------------------------------------------

## Notes for Backend Integration

-   The API is stateless (no file read/write).
-   Designed to be called via HTTP from any backend (PHP, Node.js,
    etc.).
-   The model is loaded once at startup for performance.
-   API access is protected using an API key sent via request headers.
-   Runs on CPU; GPU is optional but not required.

------------------------------------------------------------------------

## Deployment Notes

-   Recommended to run the service as a standalone microservice.
-   Can be containerized using Docker if needed.
-   Ensure the server has sufficient RAM (2GB or more recommended).

------------------------------------------------------------------------

