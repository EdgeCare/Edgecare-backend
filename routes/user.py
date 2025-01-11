from fastapi import APIRouter
from schemas.user import *
from workflows.main_workflow import main_workflow

router = APIRouter()

@router.post("/userQuestion")
async def create_post(post_data: PostData):  
    question= post_data.content

    result = main_workflow(question)

    return {"multiAgentResponse": result}

# Currently not using 
@router.post("/userDocuments")
async def create_post(post_data):  

    pass

    return {"responce": True}
