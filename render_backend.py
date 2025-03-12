from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CMS_API_KEY = os.getenv("CMS_API_KEY")
CMS_BASE_URL = "https://developer.cms.gov/marketplace-api/api-spec"

class QuoteRequest(BaseModel):
    zip_code: str
    income: float
    age: int
    household_size: int
    health_conditions: list[str]

@app.post("/get-quotes/")
def get_quotes(request: QuoteRequest):
    headers = {"Authorization": f"Bearer {CMS_API_KEY}"}
    params = {
        "zip": request.zip_code,
        "income": request.income,
        "age": request.age,
        "householdSize": request.household_size,
        "conditions": ",".join(request.health_conditions)
    }
    response = requests.get(f"{CMS_BASE_URL}/plans", headers=headers, params=params)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    
    return response.json()

@app.get("/")
def home():
    return {"message": "Quoting API is running!"}
