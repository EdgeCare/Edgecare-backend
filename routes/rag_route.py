from fastapi import APIRouter
from schemas.user import *
from rag.src.rag import MedRAG

router = APIRouter()

@router.post("/send")
async def create_post(post_data: PostData):  
    question= post_data.content
    medrag = MedRAG(llm_name="meta-llama/Meta-Llama-3-70B-Instruct", rag=True, retriever_name="MedCPT", corpus_name="Textbooks")
    ### MedRAG without pre-determined snippets
    answer, snippets, scores = medrag.answer(question=question, k=32)
    # print(answer)

    return {"answer": answer}