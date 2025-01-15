from fastapi import APIRouter, HTTPException
from schemas.user import *
from workflows.main_workflow import compiled_graph
from workflows.mcq_questions_workflow import compiled_mcq_answer_graph
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter()

@router.post("/userQuestion", response_model=UserQuestionResponce)
async def create_post(post_data: UserQuestionRequest):
    question = post_data.content

    try:
        final_state = await compiled_graph.ainvoke({
            "user_query": question,
            "keywords": [],
            "documents": [],
            "answer": None,
            "needs_refinement": False
        })
        return {"status": "Successful", "content": final_state["answer"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/mcqQuestion" , response_model=UserQuestionResponce)
async def create_Mcq_post(post_data: McqQuestionRequest):
    question = post_data.question
    options = post_data.options

    try:
        final_state = await compiled_mcq_answer_graph.ainvoke({
            "user_query": question,
            "keywords": [],
            "documents": [],
            "answer": None,
            "answer_options": options,
            "needs_refinement": False
        })
        return {"status": "Successful", "content": final_state["answer"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Currently not using 
@router.post("/userDocuments")
async def create_post(post_data):  

    pass

    return {"responce": True}
