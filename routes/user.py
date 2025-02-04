from fastapi import APIRouter, HTTPException
from schemas.user import *
from workflows.main_workflow import compiled_graph
from workflows.mcq_questions_workflow import compiled_mcq_answer_graph
from typing import List, Optional
from pydantic import BaseModel
from utils.chatHistoryService import get_chats_by_user, get_chat_by_user_and_id,create_chat
from fastapi import Depends
from sqlalchemy.orm import Session
from db.database import get_db

router = APIRouter()

@router.post("/userQuestion", response_model=UserQuestionResponce)
async def create_post(post_data: UserQuestionRequest,db: Session = Depends(get_db)):
    question = post_data.content
    user_id=1
    chat_id=1
    chat = get_chat_by_user_and_id(db,user_id,chat_id)
    print("########====>",chat)
    new_chat_str=chat+f"\nuser: {question} \n"
        
    try:
        final_state = await compiled_graph.ainvoke({
            "user_query": question,
            "chat": chat,
            "keywords": [],
            "documents": [],
            "answer": None,
            "needs_refinement": False
        })
        new_chat_str+=f"\nsystem: {final_state["answer"]} \n"
        create_chat(db,chat_id,user_id,new_chat_str)
        return {"status": "Successful", "content": final_state["answer"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    #return {"status": "Successful","content":"done" }

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

@router.post("/userPersona")
async def save_persona(persona_data:PersonaRequest):
    print("persona_data", persona_data)
    return {"responce": True}

# Currently not using 
@router.post("/userDocuments")
async def create_post(post_data):  

    pass

    return {"responce": True}
