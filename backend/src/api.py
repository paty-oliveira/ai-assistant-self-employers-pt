import uvicorn
from fastapi import FastAPI

app = FastAPI(
    title="AI-Assistant for Self-Employeers API",
    description="API for managing AI-assisted tasks and resources for self-employed individuals.",
    version="1.0.0",
)


@app.get("/")
async def root():
    return {"message": "Welcome to the AI-Assistant for Self-Employeers API"}


@app.get("/query")
async def query():
    return {"message": "This is a placeholder for the query endpoint."}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
