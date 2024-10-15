# app/main.py

from fastapi import FastAPI, Depends
from app.api import locations, ride


app = FastAPI()

# Include routers
app.include_router(locations.router, prefix="/api/v1", tags=["locations"])
app.include_router(ride.router, prefix="/api/v1", tags=["ride"])



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)