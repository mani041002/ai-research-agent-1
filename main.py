from fastapi import FastAPI
from agent import research

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI Research Agent Running"}

@app.get("/research")
def do_research(topic: str):
    result = research(topic)
    return {"research": result}