from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from .config import settings


def register_cors(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )