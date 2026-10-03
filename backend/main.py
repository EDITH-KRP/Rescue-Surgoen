import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="RescueSurgeon API",
    description="API for RescueSurgeon Website and Mobile App",
    version="1.0.0",
)

# Allow CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase Initialization
# Make sure to set these in a .env file
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://your-project-url.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "your-supabase-anon-key")

def get_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/")
def read_root():
    return {"message": "Welcome to the RescueSurgeon API (Powered by Supabase)"}

@app.get("/api/animals")
def get_animals():
    try:
        supabase: Client = get_supabase()
        # In a real app, you would query like this:
        # response = supabase.table("animals").select("*").execute()
        # return response.data
        
        # Returning mock data until the table is created
        return [
            {
                "id": 1,
                "name": "Bruno",
                "type": "dogs",
                "status": "Recovering",
                "description": "Rescued from an accident, Bruno is showing incredible spirit."
            },
            {
                "id": 2,
                "name": "Luna",
                "type": "cats",
                "status": "Recently Rescued",
                "description": "Found abandoned, Luna is receiving urgent neonatal care."
            }
        ]
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/impact")
def get_impact():
    try:
        supabase: Client = get_supabase()
        # Example query to aggregate data:
        # animals_helped = supabase.table("rescues").select("id", count="exact").execute().count
        
        return {
            "animals_helped": 1250,
            "rescue_operations": 650,
            "medical_treatments": 420,
            "successful_recoveries": 180
        }
    except Exception as e:
        return {"error": str(e)}
