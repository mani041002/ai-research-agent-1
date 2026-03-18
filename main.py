from fastapi import FastAPI
from agent import research  # your function

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is running"}

@app.get("/research")
def get_research(topic: str):
    result = research(topic)
    return {"research": result}