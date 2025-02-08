from fastapi import APIRouter, HTTPException
from schemas.user import *
from workflows.main_workflow import compiled_graph
from workflows.mcq_questions_workflow import compiled_mcq_answer_graph
from typing import List, Optional
from pydantic import BaseModel
from utils.chatHistoryService import get_chats_by_user, get_chat_by_user_and_id,create_or_update_chat
from fastapi import Depends
from sqlalchemy.orm import Session
from db.database import get_db

router = APIRouter()

@router.post("/userQuestion", response_model=UserQuestionResponce)
async def create_post(post_data: UserQuestionRequest,db: Session = Depends(get_db)):

    print("post_data",post_data)

    question = post_data.content
    health_reports = post_data.healthReports
    user_id=post_data.userId
    chat_id=post_data.chatId
    chat = get_chat_by_user_and_id(db,user_id,chat_id)

    new_chat_str = chat.chat+f"\nuser: {question} \n" if chat else f"\nuser: {question} \n"
    # print(new_chat_str)
    
    try:
        final_state = await compiled_graph.ainvoke({
            "user_query": question,
            "health_reports": health_reports,
            "chat": chat.chat if chat else None,
            "keywords": [],
            "documents": [],
            "answer": None,
        })

        # update chat 
        new_chat_str += f"\nsystem: {final_state['answer']} \n"
        create_or_update_chat( db, chat_id, user_id, new_chat_str )

        return {"status": "Successful", "content": final_state["answer"]}
    
    except Exception as e:
        print(e)
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
            "answer_options": options
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
