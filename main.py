from fastapi import FastAPI, HTTPException, Depends
from routes import auth, user, rag_route
from db.models import public as public_model,user as user_model
import uvicorn
from db.database import engine
from db.models.user import Base

# App setup
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "EdgeCare server is running!"}

# Include routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(user.router, prefix="/users", tags=["Users"])

if __name__ == "__main__":

    # Create db tables
    Base.metadata.create_all(bind=engine)

    # FAST API server
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
