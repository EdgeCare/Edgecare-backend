from fastapi import APIRouter, HTTPException
from schemas.user import *
from workflows.main_workflow import compiled_graph
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter()

@router.post("/userQuestion")
async def create_post(post_data: PostData):
    question = post_data.content

    try:
        final_state = await compiled_graph.ainvoke({
            "user_query": question,
            "keywords": [],
            "documents": [],
            "answer": None,
            "needs_refinement": False
        })
        return final_state
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Currently not using 
@router.post("/userDocuments")
async def create_post(post_data):  

    pass

    return {"responce": True}
