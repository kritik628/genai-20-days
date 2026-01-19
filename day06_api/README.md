## Day 06 – GenAI Backend API (FastAPI)

### Overview
This module exposes the GenAI recipe generator as a REST API using FastAPI.

### Endpoint
POST /generate-recipes

### Input
- ingredients (string)
- diet (string)

### Output
- Ranked list of structured recipes in JSON format

### Features
- Request validation using Pydantic
- Reusable GenAI engine
- Schema validation and deterministic ranking
- Clean error handling with categorized failures

### Why this matters
This API allows frontend, mobile, or other services to consume GenAI functionality in a production-ready way.
