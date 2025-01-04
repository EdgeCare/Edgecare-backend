from fastapi import APIRouter
from schemas.user import *

router = APIRouter()

@router.post("/userQuestion")
async def create_post(post_data: PostData):  
    question= post_data.content

    answer="dummy"

    return {"answer": answer}
