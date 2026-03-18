from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
import sqlite3
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# Database setup
DATABASE = 'database.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS model_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        version TEXT NOT NULL,
        accuracy REAL NOT NULL
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS features (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    ''')
    # Seed data
    cursor.execute("INSERT INTO model_info (name, version, accuracy) VALUES ('Demo Model', '1.0', 0.85)")
    cursor.execute("INSERT INTO features (name) VALUES ('feature1'), ('feature2')")
    conn.commit()
    conn.close()

init_db()

# Data Models
class PredictionRequest(BaseModel):
    feature1: int
    feature2: int

class ModelInfo(BaseModel):
    name: str
    version: str
    accuracy: float

# Endpoints
@app.post("/api/predict")
async def predict(request: PredictionRequest):
    # Mock prediction logic
    prediction = request.feature1 * 0.5 + request.feature2 * 0.5
    explanation = f"Prediction is a weighted sum of feature1 and feature2."
    return {"prediction": prediction, "explanation": explanation}

@app.get("/api/model-info")
async def get_model_info():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT name, version, accuracy FROM model_info")
    row = cursor.fetchone()
    conn.close()
    if row:
        return ModelInfo(name=row[0], version=row[1], accuracy=row[2])
    raise HTTPException(status_code=404, detail="Model info not found")

@app.get("/api/features")
async def get_features():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM features")
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
