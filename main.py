from fastapi import FastAPI, HTTPException, Depends
from routes import user, public
from models import public as public_model,user as user_model
# from db import database
import uvicorn

# App setup
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Server is running!"}

# Include routes
app.include_router(public.router, prefix="/public", tags=["Public"])
app.include_router(user.router, prefix="/users", tags=["Users"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
