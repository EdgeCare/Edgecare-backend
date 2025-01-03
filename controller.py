from fastapi import FastAPI, HTTPException, Depends
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from datetime import datetime, timedelta
# from jose import JWTError, jwt
# from passlib.context import CryptContext
from pydantic import BaseModel

# from medrag import MedRAG


class PostData(BaseModel):
    title: str
    content: str

# App setup
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Server is running!"}


"""
##### Temp posts ##### 
### revieves the user message and feed it to the ollama server ###
@app.post("/sendMessage")
async def create_post(post_data: UserMessage):  
    print(f"post_data: {post_data}")    # remove this line later

    medrag = MedRAG(llm_name="meta-llama/Meta-Llama-3-70B-Instruct", rag=True, retriever_name="MedCPT", corpus_name="Textbooks")
    ### MedRAG without pre-determined snippets
    answer, snippets, scores = medrag.answer(question=post_data.body, k=32)

    return {
        "id": post_data.id,
        "title": "User message responce",
        "body": answer,
        "status": "Successful"
        }

### temp post to get auth key ###
@app.post("/public/login")
async def authenticate(username: str, password: str):
    return {
        "key": "ubE21-8ycl2-hnqwd-uHF#2",
        
    }

"""
    
@app.post("/send")
async def create_post(post_data: PostData):  
    question= post_data.content
    """
    medrag = MedRAG(llm_name="meta-llama/Meta-Llama-3-70B-Instruct", rag=True, retriever_name="MedCPT", corpus_name="Textbooks")
    ### MedRAG without pre-determined snippets
    answer, snippets, scores = medrag.answer(question=question, k=32)
    # print(answer)
    """
    answer="dummy"

    return {"answer": answer}




if __name__ == "__main__":
    
    import uvicorn
    uvicorn.run("controller:app", host="0.0.0.0", port=8000, reload=True)
    
    # from rag.src.rag import test
    # print(test)




