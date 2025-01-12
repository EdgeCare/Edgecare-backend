import ast
from pydantic import BaseModel
from typing import List, Optional
from schemas.agents import AgentState
from utils.openaiClient import OpenAIClient

def extract_list_from_response(response):
    try:
        start_index = response.find("[")
        end_index = response.rfind("]") + 1
        
        list_part = response[start_index:end_index].strip()
        
        extracted_list = ast.literal_eval(list_part)
        
        if isinstance(extracted_list, list):
            return extracted_list
        else:
            raise ValueError("Extracted part is not a valid list.")
    except Exception as e:
        return f"Error extracting list: {e}"


class KeywordExtractionAgent:
    @staticmethod
    def extract_keywords(state: AgentState) -> dict:
        print("Keyword Extraction Agent Running", state)
        userQuestion = state.user_query

        prompt = f'''
        You are an expert medical knowledge assistant. Your task is to generate specific and concise queries for retrieving the most relevant medical documents based on a user’s question. 

        The generated queries should:
        1. Focus on the key medical concepts, terms, and conditions mentioned in the question.
        2. Include synonyms or related terms for broader coverage if necessary.
        3. Be formatted to maximize retrieval effectiveness from a medical document database.
        4. Use professional terminology where applicable.

        User Question: "{userQuestion}"

        Generate 3-5 optimized queries for retrieving relevant medical documents.
        Provide the queries as a Python list of strings. Ensure the list format is valid and ready for parsing directly into a Python program.
        '''

        openai_client = OpenAIClient()
        keyWords =  openai_client.generate_response(prompt)
        extracted_keywords = extract_list_from_response(keyWords)

        print(f"extracted ekywords -> {extracted_keywords}")

        state.keywords = extracted_keywords
        return state  
