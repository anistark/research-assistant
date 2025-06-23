"""
Research Assistant API - Main application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from .config import HOST, PORT, FRONTEND_URL
from .routes import upload, search, journals, stats

app = FastAPI(title="Research Assistant API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(search.router, prefix="/api", tags=["search"])
app.include_router(stats.router, prefix="/api", tags=["statistics"])
app.include_router(journals.router, prefix="/api", tags=["journals"])

@app.get("/")
async def root():
    return {"message": "Research Assistant API", "version": "1.0.0"}

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
