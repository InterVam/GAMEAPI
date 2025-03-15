# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# In main.py
from app.routes import auth_router, admin_router, player_router


app = FastAPI(
    title="Game Management API",
    description="API for managing games with device registration",
    version="1.0.0"
)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(player_router)
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["root"])
async def root():
    return {
        "message": "Welcome to the Game Management API",
        "documentation": "/docs",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)