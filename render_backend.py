import requests
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class QuoteRequest(BaseModel):
    zip_code: str
    income: float
    age: int
    household_size: int
    health_conditions: List[str]

CMS_API_KEY = os.getenv("CMS_API_KEY")
CMS_BASE_URL = "https://developer.cms.gov/marketplace-api/api-spec"

@app.post("/get-quotes/")
def get_quotes(request: QuoteRequest):
    try:
        headers = {"Authorization": f"Bearer {CMS_API_KEY}"}
        params = {
            "zip": request.zip_code,
            "income": request.income,
            "age": request.age,
            "householdSize": request.household_size,
            "conditions": ",".join(request.health_conditions),
        }

        # Debug: Print response before parsing
        response = requests.get(f"{CMS_BASE_URL}/plans", headers=headers, params=params)
        print("Raw Response:", response.text)  # Log the raw response

        if response.status_code != 200:
            return {"error": response.status_code, "message": response.text}  # Return raw response as a message

        return response.json()

    except Exception as e:
        return {"error": "Internal Server Error", "details": str(e)}
