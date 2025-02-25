from pydantic import BaseModel
from typing import List, Optional
from schemas.agents import AgentState
from utils.openaiClient import openaiClient
from utils.extractContent import extract_list, extract_json


UNSUPPORTED_QUERY_DEFAULT_MESSAGE = "Sorry. I can only support for medical inqueries. Please share only medical concerns."
INTERNAL_ERROR_DEFAULT_MESSAGE = "Sorry, Internal server error."

class KeywordExtractionAgent:
    @staticmethod
    def extract_keywords(state: AgentState) -> dict:
        print("🤖 Keyword Extraction Agent Running")

#         prompt = f'''You are an expert medical knowledge assistant. Your task is to generate specific and concise queries for retrieving the most relevant medical documents based on a user's question. 

# The generated queries should:
# 1. Focus on the key medical concepts, terms, and conditions mentioned in the question.
# 2. Include synonyms or related terms for broader coverage if necessary.
# 3. Be formatted to maximize retrieval effectiveness from a medical document database.
# 4. Use professional terminology where applicable.


# User Question: "{state.user_query}"

# Generate 3-5 optimized queries for retrieving relevant medical documents. 
# Provide the queries as a Python list of strings. Ensure the list format is valid and ready for parsing directly into a Python program.
# Do not give any query if the user question is not about a medical condition. Just give an empty list instead.
# '''

        prompt = """You are Lisa, a medical assistant designed to extract key medical terms from user conversations. Your primary role is to identify relevant medical keywords for retrieval purposes and determine whether a conversation is medical-related. You must classify user input into one of two categories:
1. Medical-related inquiry that requires snippet retrieval
2. Inquiry that does not require snippet retrieval (like a greeting, or if ask what can you do?)

Instructions:
1. If the conversation is medical-related and requires retrieval (RETRIEVE_SNIPPETS = True, KEYWORDS: [ python list of keywords]):

- Extract key medical concepts, conditions, symptoms, treatments, and terms.
- Include synonyms or related terms for broader retrieval effectiveness.
- Use professional medical terminology where applicable.
- Generate 5 optimized queries.
- Return the queries in a Python list format (5 queries). 
- Do no provide more than 5 queries.

2. If the question is like a greeting, or if ask what can you do? that does not require retrieval (RETRIEVE_SNIPPETS = False, MESSAGE = your answer):
- Example: General medical advice like "How can you help me?" doesn't require retrieval but is still a medical conversation related to us.
- If the user greets you or asks what you do, respond with an introduction.

Response Format (Always JSON:
- Your can include these fields:
    {
        "RETRIEVE_SNIPPETS": true or false,
        "MESSAGE": polite reply to the user,
        "KEYWORDS": python list of extracted keywords
    }
    "RETRIEVE_SNIPPETS" → true if retrieval should happen; false otherwise.
    "MESSAGE" → the reply message for the user. a polite answer. 
    "KEYWORDS" → Extracted medical queries as a Python list (if RETRIEVE_SNIPPETS = true)."""
        
        if state.chat:
            prompt += """ Read the both Past Chat and New query to provide answer
--------------------
Past Chat: """ + state.chat + """
""" 
        # add user question
        prompt += """

New query from user: """ + state.user_query + """
"""

        for i in range (5):
            try:
                reply =  openaiClient.generate_response(prompt)
                print(prompt)
                extracted_json = extract_json(reply)

                # if extracted_json["UNSUPPORTED"]:
                #     print("⚠️ Keyword Extraction Agent | UNSUPPORTED query")
                #     return {"answer": extracted_json["MESSAGE"] if extracted_json["MESSAGE"] else UNSUPPORTED_QUERY_DEFAULT_MESSAGE }
                
                if extracted_json["RETRIEVE_SNIPPETS"] and len(extracted_json["KEYWORDS"]) > 0:
                    print("⚠️ Keyword Extraction Agent | need to retrieve documents")
                    print(f"⚠️ Keyword Extraction Agent | KEYWORDS {extracted_json['KEYWORDS']}" )
                    if len(extracted_json["KEYWORDS"]) < 5:
                        return {"keywords": extracted_json["KEYWORDS"] + [state.chat+state.user_query]}
                    return {"keywords": extracted_json["KEYWORDS"]}

                elif not extracted_json["RETRIEVE_SNIPPETS"] and extracted_json["MESSAGE"]:
                    print("⚠️ Keyword Extraction Agent | no need to retrieve documents answering to the query")
                    return {"answer": extracted_json["MESSAGE"] }
                
                print(f"⚠️ Keyword Extraction Agent | attempt {i} Failed! \n reply: {reply} extracted_json, {extracted_json}" )
            except:
                pass

        print("""⚠️ Keyword Extraction Agent | 5 attempts Failed!
              State: """, state)
        return {"keywords": [state.chat+state.user_query]}
