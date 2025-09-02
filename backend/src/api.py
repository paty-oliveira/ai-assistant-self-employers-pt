import logging
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .llama_cloud_service import LlamaCloudService
from .rag import query_documents

load_dotenv()


class QueryRequest(BaseModel):
    query: str
    index_name: str


class QueryResponse(BaseModel):
    response: str
    query: str
    index_used: str
    service_used: str


external_service = None
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    global external_service

    try:
        api_key = os.getenv("LLAMA_CLOUD_API_KEY")
        if not api_key:
            raise ValueError("LLAMA_CLOUD_API_KEY environment variable is not set.")
        external_service = LlamaCloudService(api_key=api_key)

        # This yield is what makes it an async generator
        yield

    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise
    finally:
        # Cleanup code
        external_service = None


app = FastAPI(
    title="AI-Assistant for Self-Employeers API",
    description="API for managing AI-assisted tasks and resources for self-employed individuals.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
async def root():
    return {"message": "Welcome to the AI-Assistant for Self-Employeers API"}


@app.get("/query")
async def query(request: QueryRequest) -> QueryResponse:
    try:
        if not external_service:
            raise HTTPException(status_code=503, detail="Service not available")

        response = query_documents(
            query_text=request.query,
            index_name=request.index_name,
            external_service=external_service,
        )

        return QueryResponse(
            response=response,
            query=request.query,
            index_used=request.index_name,
            service_used="Llama Cloud Service",
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")
