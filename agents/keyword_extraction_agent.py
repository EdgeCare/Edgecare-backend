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

        prompt = """You are Lisa, a medical assistant designed to extract key medical terms from user conversations. Your primary role is to identify relevant medical keywords for retrieval purposes and determine whether a conversation is medical-related. You must classify user input into one of three categories:
1. Medical-related inquiry that requires snippet retrieval
2. Medical-related inquiry that does not require snippet retrieval (like a greeting, or if ask what can you do?)
3. Non-medical inquiry (unsupported)

Instructions:
1. If the conversation is medical-related and requires retrieval (UNSUPPORTED = False, RETRIEVE_SNIPPETS = True, KEYWORDS: [ python list of keywords]):

- Extract key medical concepts, conditions, symptoms, treatments, and terms.
- Include synonyms or related terms for broader retrieval effectiveness.
- Use professional medical terminology where applicable.
- Generate 5 optimized queries.
- Return the queries in a Python list format (5 queries).

2. If the conversation is medical-related but does not require retrieval (UNSUPPORTED = False, RETRIEVE_SNIPPETS = False, MESSAGE = your answer):
- Example: General medical advice like "How can you help me?" doesn't require retrieval but is still a medical conversation related to us.
- If the user greets you or asks what you do, respond with an introduction.

3. If the conversation is not medical-related (UNSUPPORTED = True, MESSAGE = "tell reason"):
- Politely inform the user that you handle only medical-related inquiries.
- Example: If the user asks about coding, writing essays, or other non-medical topics, return "UNSUPPORTED": True with a polite explanation that you are medical assistance, and tell how can you help him.

Response Format (Always JSON:
- Your can include these fields:
    {
        "UNSUPPORTED": false or true,
        "RETRIEVE_SNIPPETS": true or false,
        "MESSAGE": give a reason for unsupported or reply to greeting requests,
        "KEYWORDS": python list of extracted keywords
    }
    "UNSUPPORTED" → true if the query is non-medical; otherwise, false.
    "RETRIEVE_SNIPPETS" → true if retrieval should happen; false otherwise.
    "MESSAGE" → the reply message for the user. a polite answer. 
    "KEYWORDS" → Extracted medical queries as a Python list (if RETRIEVE_SNIPPETS = true)."""
        
        if state.chat:
            prompt += """
--------------------
Past Chat: """ + state.chat + """
""" 
        # add user question
        prompt += """
--------------------
New query from user: """ + state.user_query + """
"""

        for i in range (5):
            reply =  openaiClient.generate_response(prompt)
            extracted_json = extract_json(reply)

            if extracted_json["UNSUPPORTED"]:
                print("⚠️ Keyword Extraction Agent | UNSUPPORTED query")
                return {"answer": extracted_json["MESSAGE"] if extracted_json["MESSAGE"] else UNSUPPORTED_QUERY_DEFAULT_MESSAGE }
            
            elif extracted_json["RETRIEVE_SNIPPETS"] and len(extracted_json["KEYWORDS"]) > 0:
                print("⚠️ Keyword Extraction Agent | need to retrieve documents")
                print(f"⚠️ Keyword Extraction Agent | KEYWORDS {extracted_json['KEYWORDS']}" )
                return {"keywords": extracted_json["KEYWORDS"]}
            
            elif not extracted_json["RETRIEVE_SNIPPETS"] and extracted_json["MESSAGE"]:
                print("⚠️ Keyword Extraction Agent | no need to retrieve documents answering to the query")
                return {"answer": extracted_json["MESSAGE"] }
            
            print(f"⚠️ Keyword Extraction Agent | attempt {i} Failed! \n reply: {reply} extracted_json, {extracted_json}" )

        
        print("""⚠️ Keyword Extraction Agent | 5 attempts Failed!
              State: """, state)

        return {"answer": INTERNAL_ERROR_DEFAULT_MESSAGE}
