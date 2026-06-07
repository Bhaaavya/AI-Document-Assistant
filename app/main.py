from fastapi import FastAPI

from app.database import engine, Base
from app import models
from app.routes import auth_routes, document_routes


app = FastAPI(
    title="AI Document Assistant",
    description="Upload PDFs and ask questions about them using AI",
    version="1.0.0"
)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


app.include_router(auth_routes.router)
app.include_router(document_routes.router)


@app.get("/")
def root():
    return {"message": "AI Document Assistant API is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}