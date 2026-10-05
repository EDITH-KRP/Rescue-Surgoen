import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from dotenv import load_dotenv

load_dotenv()

# Use the provided Supabase connection string
# Usually it requires the 'postgres' user
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:Ammapappais1@db.alvokjnbpptkdgomgpws.supabase.co:5432/postgres")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class Animal(Base):
    __tablename__ = "animals"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String)
    status = Column(String)
    description = Column(Text)

class Impact(Base):
    __tablename__ = "impact_stats"
    id = Column(Integer, primary_key=True, index=True)
    animals_helped = Column(Integer, default=0)
    rescue_operations = Column(Integer, default=0)
    medical_treatments = Column(Integer, default=0)
    successful_recoveries = Column(Integer, default=0)

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="RescueSurgeon API",
    description="API for RescueSurgeon Website and Mobile App",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the RescueSurgeon API (Powered by Supabase PostgreSQL)"}

@app.get("/api/animals")
def get_animals(db: Session = Depends(get_db)):
    animals = db.query(Animal).all()
    if not animals:
        # Return mock data if DB is empty
        return [
            {"id": 1, "name": "Bruno", "type": "dogs", "status": "Recovering", "description": "Rescued from an accident, Bruno is showing incredible spirit."},
            {"id": 2, "name": "Luna", "type": "cats", "status": "Recently Rescued", "description": "Found abandoned, Luna is receiving urgent neonatal care."}
        ]
    return animals

@app.get("/api/impact")
def get_impact(db: Session = Depends(get_db)):
    impact = db.query(Impact).first()
    if not impact:
        # Return mock data if DB is empty
        return {
            "animals_helped": 1250,
            "rescue_operations": 650,
            "medical_treatments": 420,
            "successful_recoveries": 180
        }
    return impact

